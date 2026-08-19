# Databricks notebook source
# MAGIC %sql
# MAGIC -- Gold #1: daily revenue, completed orders only, one row per day
# MAGIC CREATE OR REPLACE TABLE shopstream.core.gold_daily_revenue AS
# MAGIC SELECT
# MAGIC   DATE(order_ts) AS order_date,
# MAGIC   COUNT(DISTINCT order_id) AS orders,
# MAGIC   SUM(quantity) AS units_sold,
# MAGIC   ROUND(SUM(line_revenue), 2) AS revenue
# MAGIC FROM shopstream.core.silver_orders
# MAGIC WHERE status = 'completed'
# MAGIC GROUP BY DATE(order_ts);
# MAGIC
# MAGIC SELECT * FROM shopstream.core.gold_daily_revenue ORDER BY order_date LIMIT 7
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Gold #2: category performance, what actually makes money
# MAGIC CREATE OR REPLACE TABLE shopstream.core.gold_category_performance AS
# MAGIC SELECT
# MAGIC   p.category,
# MAGIC   COUNT(DISTINCT o.order_id) AS orders,
# MAGIC   SUM(o.quantity) AS units_sold,
# MAGIC   ROUND(SUM(o.line_revenue), 2) AS revenue,
# MAGIC   ROUND(SUM(o.quantity * p.unit_margin), 2) AS gross_margin
# MAGIC FROM shopstream.core.silver_orders o
# MAGIC JOIN shopstream.core.silver_products p USING (product_id)
# MAGIC WHERE o.status = 'completed'
# MAGIC GROUP BY p.category;
# MAGIC
# MAGIC SELECT * FROM shopstream.core.gold_category_performance ORDER BY revenue DESC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Gold #3: customer lifetime value, who the best customers are
# MAGIC CREATE OR REPLACE TABLE shopstream.core.gold_customer_ltv AS
# MAGIC SELECT
# MAGIC   c.customer_id,
# MAGIC   c.name,
# MAGIC   c.country,
# MAGIC   c.signup_channel,
# MAGIC   COUNT(DISTINCT o.order_id) AS lifetime_orders,
# MAGIC   ROUND(SUM(o.line_revenue), 2) AS lifetime_revenue
# MAGIC FROM shopstream.core.silver_orders o
# MAGIC JOIN shopstream.core.silver_customers c USING (customer_id)
# MAGIC WHERE o.status = 'completed'
# MAGIC GROUP BY c.customer_id, c.name, c.country, c.signup_channel;
# MAGIC
# MAGIC SELECT * FROM shopstream.core.gold_customer_ltv ORDER BY lifetime_revenue DESC LIMIT 10
# MAGIC