from google.cloud import bigquery
import pandas as pd

client = bigquery.Client(project="gcp-innovation-data-prod")

query = """
WITH quarters AS (
  SELECT
    FORMAT_TIMESTAMP('%Y-Q%d', TIMESTAMP_TRUNC(DATE_ADD(CURRENT_DATE(), INTERVAL -n QUARTER), QUARTER), EXTRACT(QUARTER FROM DATE_ADD(CURRENT_DATE(), INTERVAL -n QUARTER))) AS quarter,
    DATE_TRUNC(DATE_ADD(CURRENT_DATE(), INTERVAL -n QUARTER), QUARTER) AS quarter_start
  FROM UNNEST(GENERATE_ARRAY(0, 11)) AS n
)
SELECT
  q.quarter,
  COALESCE(SUM(CAST(ob.price AS NUMERIC)), 0) AS revenue_jpy,
  COUNT(DISTINCT o.id) AS orders
FROM quarters q
LEFT JOIN `gcp-innovation-data-prod.master_ittrend.orders` o
  ON DATE_TRUNC(o.created_at, QUARTER) = q.quarter_start
LEFT JOIN `gcp-innovation-data-prod.master_ittrend.order_products` op
  ON op.order_id = o.id
LEFT JOIN `gcp-innovation-data-prod.master_ittrend.order_billings` ob
  ON ob.order_id = o.id
LEFT JOIN `gcp-innovation-data-prod.master_ittrend.products` p
  ON op.product_id = p.id
LEFT JOIN `gcp-innovation-data-prod.master_ittrend.categories` ca
  ON p.category_id = ca.id
LEFT JOIN `gcp-innovation-data-prod.master_ittrend.order_product_invalid_types` iv
  ON op.invalid_type_id = iv.id
WHERE
  ca.id = 716
  AND iv.id IS NULL
GROUP BY q.quarter, q.quarter_start
ORDER BY q.quarter_start
"""

df = client.query(query).to_dataframe()
df.head()
