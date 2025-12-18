import matplotlib.pyplot as plt
import pandas as pd
import json
from common import bq_utils

bq_utils.set_jp_font(verbose=True)

# ===== データ読み込み =====
json_path = "/mnt/c/Users/ta_sakai/projects/category_sales/json/order_details_2025Q3"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df["sum_price"] = df["sum_price"].astype(float)

# ===== 棒グラフ描画 =====
plt.figure(figsize=(10, 6))
plt.bar(df["order_id"].astype(str), df["sum_price"])
plt.xticks(rotation=90)
plt.title("2025-Q3 適性検査カテゴリの注文別売上金額", fontsize=14)
plt.xlabel("注文ID", fontsize=12)
plt.ylabel("売上金額（円）", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.6)

plt.tight_layout()
plt.savefig("./.output/order_detail_bar.png", dpi=160)
print("✅ 画像保存: ./.output/order_detail_bar.png")
plt.show()
