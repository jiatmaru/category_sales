# dately_sales_plot.py
import matplotlib.pyplot as plt
import pandas as pd
import json
from common import bq_utils

# ===== 日本語フォント設定 =====
bq_utils.set_jp_font(verbose=True)

# ===== データ読み込み =====
json_path = "/mnt/c/Users/ta_sakai/projects/category_sales/json/dately_sales_2025_04_10.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# 数値型へ変換
df["revenue_jpy"] = df["revenue_jpy"].astype(float)

# 月順に並べ替え（YYYY-MM 文字列 → datetime）
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

# ===== 折れ線グラフ描画 =====
plt.figure(figsize=(10, 6))
plt.plot(df["date"], df["revenue_jpy"], marker="o")

plt.title("適性検査カテゴリ（716）月別売上推移", fontsize=14)
plt.xlabel("月", fontsize=12)
plt.ylabel("売上金額（円）", fontsize=12)

plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(rotation=45)

plt.tight_layout()

# 保存場所は outputs/ に合わせる
output_path = "/mnt/c/Users/ta_sakai/projects/category_sales/.output/dately_sales_2025_04_10.png"
plt.savefig(output_path, dpi=160)

print(f"✅ 画像保存: {output_path}")
plt.show()
