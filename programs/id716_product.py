import matplotlib.pyplot as plt
import pandas as pd
import json
from common import bq_utils

bq_utils.set_jp_font(verbose=True)

# ===== データ読み込み =====
json_path = "/mnt/c/Users/ta_sakai/projects/category_sales/json/id716_5.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# 数値に変換
df["price"] = df["price"].astype(float)

# ===== 製品別売上集計 =====
product_sales = (
    df.groupby(["product_id", "product_name"])["price"]
      .sum()
      .reset_index()
      .sort_values("price", ascending=False)
)

print(product_sales)

# ===== グラフ描画 =====
plt.figure(figsize=(12, 6))
plt.bar(product_sales["product_name"], product_sales["price"])

plt.xticks(rotation=60, ha="right")
plt.title("2025-Q3 適性検査カテゴリ 製品別売上", fontsize=16)
plt.xlabel("製品名", fontsize=12)
plt.ylabel("売上金額（円）", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("./.output/id716_product_sales.png", dpi=160)
print("✅ 保存しました → ./.output/id716_product_sales.png")

plt.show()
