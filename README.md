# 🛍️ ShopStream Lakehouse — End-to-End Data Engineering Project using Databricks

This project demonstrates the development of a scalable end-to-end data pipeline for processing and reporting retail order data using Databricks Cloud services, Delta Lake architecture, and production-grade data engineering patterns.

## 🚀 Project Overview

The project automates data ingestion, transformation, and analysis for an e-commerce system. The final output is made available for downstream analytics and dashboards.

The architecture leverages:

- **Databricks & Delta Lake**: For creating multi-layered data pipelines (Bronze, Silver, Gold) using SQL and PySpark
- **COPY INTO**: For idempotent batch ingestion from CSV files
- **Auto Loader**: For exactly-once streaming ingestion from JSON events
- **Databricks SQL Dashboard**: For reporting and visualization
- **GitHub**: As version control and portfolio showcase
- **Jobs & Orchestration**: For scheduled pipeline execution with task dependencies

## 🗺️ Architecture

```
CSV Files (Historical Data)
    ↓
[COPY INTO - Idempotent Batch Loading]
    ↓
Bronze Layer (13,717 raw order rows)
    ↓
[Deduplication, Type Casting, Normalization]
    ↓
Silver Layer (11,061 clean order rows)
    ↓
[Aggregation & Business Logic]
    ↓
Gold Layer (Business Metrics)
    ↓
Databricks SQL Dashboard
```

**Parallel Streaming Path:**

```
JSON Events (Live Orders)
    ↓
[Auto Loader + Checkpoints]
    ↓
Bronze Streaming Table
    ↓
Shared Silver & Gold Tables
    ↓
Real-time Dashboard Updates
```

## 🔁 Pipeline Workflow

The Databricks workflow is orchestrated as shown below:

**Scheduled Job:** `shopstream_daily_batch`

```
bronze_ingestion (Load CSVs)
    ↓
silver_layer (Clean & Transform)
    ↓
gold_layer (Aggregate Metrics)
    ↓
Dashboard (Visualization)
```

## 🔹 Stages in the Pipeline

| Layer | Description | Row Count | Key Operations |
|---|---|---|---|
| Lookup | Initial lookup data load (Products, Customers, Regions) | 197, 1,000 | Type casting, categorization |
| Bronze | Raw ingestion using COPY INTO and Auto Loader | 13,717 | No transformation, preserve original data |
| Silver | Cleansed and filtered data tables (Orders, Customers, Products) | 11,061 | Deduplication (234 rows), drop bad data (259 rows), normalization |
| Gold | Curated business-ready dimension and fact tables | ~180–847 | Aggregation, JOINs, business metrics |
| Fact | Star schema constructed for analytical reporting | 11,061 | Order fact table with foreign keys to dimensions |

## 📂 Project Structure

The notebooks follow the medallion architecture:

```
shopstream-lakehouse/
├── README.md
├── SETUP_GUIDE.md
├── GITHUB_GUIDE.md
├── .gitignore
│
├── notebooks/
│   ├── 01_bronze_batch_ingestion.sql
│   ├── 02_silver_layer.sql
│   ├── 03_gold_layer.sql
│   ├── 04_stream_events.py
│   └── 05_streaming_bronze.py
│
├── pipelines/
│   ├── pipe_events_bronze.py
│   └── pipe_daily_revenue.py
│
├── jobs/
│   └── shopstream_daily_batch.md
│
├── docs/
│   └── data_quality_rules.md
│
└── data/
    └── gold_sample_queries.sql
```

## 🧪 Technologies Used

| Component | Technology | Purpose |
|---|---|---|
| Ingestion (Batch) | COPY INTO | Idempotent CSV loading |
| Ingestion (Streaming) | Auto Loader | Exactly-once JSON event processing |
| Transformation | Databricks SQL & PySpark | Data cleaning, deduplication, aggregation |
| Storage | Delta Lake | ACID transactions, time travel, versioning |
| Orchestration | Databricks Jobs | Scheduled execution with task dependencies |
| Pipelines | Lakeflow (Delta Live Tables) | Declarative data transformations |
| Visualization | Databricks SQL Dashboard | Business metric reporting |
| Version Control | GitHub | CI/CD and portfolio showcase |
| Compute | Serverless Spark | Auto-scaling, no cluster management |

## 📊 Output

The final Gold Layer tables (`gold_daily_revenue`, `gold_category_performance`, `gold_customer_ltv`) are published via Databricks SQL Dashboard for analysis. The star schema ensures performance optimization for downstream consumers and reporting tools.

**Gold Layer Outputs:**
- `gold_daily_revenue`: Daily revenue metrics (orders, units sold, revenue)
- `gold_category_performance`: Revenue and gross margin by product category
- `gold_customer_ltv`: Customer lifetime value and segmentation
