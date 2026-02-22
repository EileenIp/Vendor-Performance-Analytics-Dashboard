# Dataset.py
"""
Vendor Performance Analysis - Dataset Ingestion and Processing
""" 

# Load Libraries
import pandas as pd
import os
from sqlalchemy import create_engine
import time
import sqlite3

def ingest_db(df, table_name, engine):
    """
    Function to ingest data into the database
    
    :param df: Description
    :param table_name: Description
    :param engine: Description
    """
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

def load_raw_data(engine):
    """
    Load raw data from CSV files in the 'data' directory and ingest it into the database.
    """
    for file in os.listdir('data'):
        if '.csv' in file:
            df = pd.read_csv(os.path.join('data', file))
            ingest_db(df, file[:-4], engine)

def create_vendor_summary(conn):
    """
    Create a vendor sales summary by joining multiple data sources.
    
    :param conn: Description
    """
    vendor_sales_summary = pd.read_sql_query("""WITH FreightSummary AS (
    SELECT 
        VendorNumber, 
        SUM(Freight) as FreightCost 
    FROM vendor_invoice 
    GROUP BY VendorNumber
    ),
        PurchasesSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price as ActualPrice,
            pp.Volume,
            SUM(p.Quantity) as TotalPurchaseQuantity,
            SUM(p.Dollars) as TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
        ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice, pp.Price, pp.Volume
    ),
        
    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            Description,
            SUM(SalesDollars) as TotalSalesDollars,
            SUM(SalesPrice) as TotalSalesPrice,
            SUM(SalesQuantity) as TotalSalesQuantity,
            SUM(ExciseTax) as TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )

    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalSalesQuantity,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchasesSummary ps
    LEFT JOIN SalesSummary ss
    ON ps.VendorNumber = ss.VendorNo AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    """, conn)
    return vendor_sales_summary

def clean_data(df):
    """
    Clean and preprocess the vendor sales summary data by performing various 
    transformations.
    
    :param df: Description
    """
    # Convert Volume to numeric, coercing errors to NaN
    df['Volume'] = df['Volume'].astype('float64')

    # Fill NaN values with 0
    df.fillna(0, inplace=True)

    # Strip leading and trailing whitespace from VendorName
    df['VendorName'] = df['VendorName'].str.strip()

    # Calculate additional metrics
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']
    df['ProfitMargin'] = (df['GrossProfit'] / df['TotalSalesDollars']) * 100
    df['StockTurnover'] = df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    df['SalestoPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']

    return df

def main():
    # Create database engine
    engine = create_engine('sqlite:///inventory.db')

    # Load raw data into the database
    load_raw_data(engine)

    # Create a connection to the SQLite database
    conn = sqlite3.connect('inventory.db')

    # Create vendor sales summary
    vendor_sales_summary = create_vendor_summary(conn)
    vendor_sales_summary = clean_data(vendor_sales_summary)

    # Load the cleaned vendor sales summary back into the database
    ingest_db(vendor_sales_summary, 'vendor_sales_summary', engine)