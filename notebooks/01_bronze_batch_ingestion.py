# Databricks notebook source
# MAGIC %sql
# MAGIC -- Peek at the raw orders file before loading anything
# MAGIC SELECT * FROM read_files(
# MAGIC   '/Volumes/shopstream/core/raw/orders_2026_h1.csv',
# MAGIC   format => 'csv',
# MAGIC   header => true
# MAGIC )
# MAGIC LIMIT 10
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Bronze orders: create once, then load with COPY INTO (idempotent)
# MAGIC CREATE TABLE IF NOT EXISTS shopstream.core.bronze_orders;
# MAGIC
# MAGIC COPY INTO shopstream.core.bronze_orders
# MAGIC FROM '/Volumes/shopstream/core/raw/orders_2026_h1.csv'
# MAGIC FILEFORMAT = CSV
# MAGIC FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true', 'mergeSchema' = 'true')
# MAGIC COPY_OPTIONS ('mergeSchema' = 'true')
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Same pattern for the two dimension files
# MAGIC CREATE TABLE IF NOT EXISTS shopstream.core.bronze_customers;
# MAGIC
# MAGIC COPY INTO shopstream.core.bronze_customers
# MAGIC FROM '/Volumes/shopstream/core/raw/customers.csv'
# MAGIC FILEFORMAT = CSV
# MAGIC FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true', 'mergeSchema' = 'true')
# MAGIC COPY_OPTIONS ('mergeSchema' = 'true');
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS shopstream.core.bronze_products;
# MAGIC
# MAGIC COPY INTO shopstream.core.bronze_products
# MAGIC FROM '/Volumes/shopstream/core/raw/products.csv'
# MAGIC FILEFORMAT = CSV
# MAGIC FORMAT_OPTIONS ('header' = 'true', 'inferSchema' = 'true', 'mergeSchema' = 'true')
# MAGIC COPY_OPTIONS ('mergeSchema' = 'true');
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- The bronze layer is in. Three tables, raw shapes preserved.
# MAGIC SELECT 'bronze_orders' AS table_name, COUNT(*) AS row_count FROM shopstream.core.bronze_orders
# MAGIC UNION ALL
# MAGIC SELECT 'bronze_customers', COUNT(*) FROM shopstream.core.bronze_customers
# MAGIC UNION ALL
# MAGIC SELECT 'bronze_products', COUNT(*) FROM shopstream.core.bronze_products