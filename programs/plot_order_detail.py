# plot_order_detail.py
import json
import pandas as pd
import matplotlib.pyplot as plt
from common import bq_utils

# ===== フォント設定 =====
bq_utils.set_jp_font(verbose=True)

# ===== データ読み込み =====
json_path = "/mnt/c/Users/ta_sakai/projects/category_sales/json/order_details_2025Q3"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)
df["sum_price"] = df["sum_price"].astype(float)
df["billing_count"] = df["billing_count"].astype(int)

# ===== 可視化 =====
plt.figure(figsize=(10, 6))
plt.scatter(df["billing_count"], df["sum_price"], s=100, alpha=0.7, label="受注別合計金額")
plt.title("2025-Q3 適性検査カテゴリの受注別金額分布", fontsize=14)
plt.xlabel("請求書数（billing_count）", fontsize=12)
plt.ylabel("売上合計金額（円）", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.5)

# 重複関係の可視化補助線
for _, row in df.iterrows():
    plt.text(row["billing_count"] + 0.05, row["sum_price"],
             f"order {row['order_id']}", fontsize=8, color="gray")

plt.tight_layout()
plt.savefig("./.output/order_detail_plot.png", dpi=160)
print("✅ 図を保存しました: ./.output/order_detail_plot.png")
