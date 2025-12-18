import matplotlib.pyplot as plt
import pandas as pd
import json
from common import bq_utils

# 日本語フォント設定
bq_utils.set_jp_font(verbose=True)

# ===== JSON 読み込み =====
json_path = "/mnt/c/Users/ta_sakai/projects/category_sales/json/id716_10185.json"

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# 数値変換
df["total_sales"] = df["total_sales"].astype(float)

# 四半期ラベルをソート可能な形に整備
df["year"] = df["year_quarter"].str.slice(0, 4).astype(int)
df["q"] = df["year_quarter"].str.slice(5).str.replace("Q", "").astype(int)

df = df.sort_values(["year", "q"])

# プロット用ラベル
df["label"] = df["year"].astype(str) + "-Q" + df["q"].astype(str)

# ===== グラフ描画 =====
plt.figure(figsize=(14, 6))
plt.bar(df["label"], df["total_sales"])

plt.xticks(rotation=60, ha="right")
plt.title("ミキワメ 適性検査　 四半期売上推移（直近5年）", fontsize=16)
plt.xlabel("四半期", fontsize=12)
plt.ylabel("売上金額（円）", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig("./.output/id716_10185_quarterly_sales.png", dpi=160)
print("✅ 保存しました → ./.output/id716_10185_quarterly_sales.png")

plt.show()
