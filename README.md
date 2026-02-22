# 🏢 Vendor Performance Analytics Dashboard

## 📌 Project Overview

This project presents an end-to-end **Vendor Performance Analytics solution**, combining:

- 📊 Interactive Power BI dashboard
- 🛠️ Python-based ETL pipeline
- 🗄️ SQLite database modelling
- 📈 Profitability & procurement analytics

The goal is to analyse **vendor sales, purchases, profitability, freight costs, and performance contribution**, enabling procurement and finance teams to make data-driven supplier decisions.

---

## 🎯 Business Objectives

- Measure total sales vs purchase performance
- Identify high- and low-performing vendors
- Analyse gross profit and profit margins
- Understand brand-level contribution
- Monitor vendor concentration risk
- Support procurement optimisation decisions

---

## 📊 Key KPIs

| Metric | Value |
|--------|--------|
| **Total Sales** | $441.41M |
| **Total Purchase** | $307.34M |
| **Gross Profit** | $134.07M |
| **Profit Margin** | 38.7% |
| **Unsold Capital** | $2.71M |

---

## 🧠 Key Insights

- A small number of vendors contribute a large portion of total revenue.
- DIAGEO NORTH AMERICA leads in vendor sales performance.
- Profitability varies significantly across vendors and brands.
- Several vendors show low profit margin relative to total sales.
- Vendor concentration highlights potential supplier dependency risk.
- Some brands generate strong sales but weaker margins.

---

## 📸 Dashboard Preview

<img src="https://github.com/EileenIp/Vendor-Performance-Analytics-Dashboard/blob/main/Vendor%20Performance%20Dashboard.png">
---

## 🖥️ Dashboard Features

### 🔹 Vendor Overview
- Total Sales, Purchase, Gross Profit, Profit Margin
- Unsold Capital analysis
- Vendor contribution breakdown

### 🔹 Top Performers
- Top 10 Vendors by Sales
- Top 10 Brands by Sales

### 🔹 Risk & Underperformance
- Lowest Performing Vendors
- Low Margin Brand Scatter Analysis
- Vendor-level profit margin comparison

---

## 🛠️ Technical Architecture

This project includes a **Python ETL pipeline** that:

1. Loads raw CSV data into SQLite
2. Performs SQL joins across:
   - Purchases
   - Sales
   - Freight
   - Pricing tables
3. Creates a consolidated `vendor_sales_summary` table
4. Calculates additional KPIs:
   - Gross Profit
   - Profit Margin
   - Stock Turnover
   - Sales-to-Purchase Ratio

---

## 📂 Data Engineering Workflow

### 🔹 Dataset Ingestion
Custom ingestion function writes data into SQLite:

```python
df.to_sql(table_name, con=engine, if_exists='replace', index=False)
