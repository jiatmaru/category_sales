# =============================================
# plot_id716_1.py
# 適性検査カテゴリ (category_id=716) の売上推移グラフ
# =============================================

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from common import bq_utils  # ← 日本語フォント設定関数を利用

# ===== パス設定 =====
BASE_DIR = "/mnt/c/Users/ta_sakai/projects/category_sales"
JSON_PATH = os.path.join(BASE_DIR, "json", "id716_3")

# ===== データ読み込み =====
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# BigQuery結果（JSON）の想定構造に合わせて DataFrame 化
df = pd.DataFrame(data)
# 数値カラムを数値型に変換
df["revenue_jpy"] = pd.to_numeric(df["revenue_jpy"])
df["orders"] = pd.to_numeric(df["orders"])

# カラム名がクエリ結果に依存するため、念のため確認
print("[INFO] カラム一覧:", df.columns.tolist())


# 想定： "quarter"（例: '2025-Q3'）と "revenue_jpy" が存在
if "quarter" not in df.columns or "revenue_jpy" not in df.columns:
    raise ValueError("JSONに 'quarter' または 'revenue_jpy' カラムが見つかりません。")

# 四半期順に並べ替え
df = df.sort_values("quarter")

# ===== フォント設定 =====
bq_utils.set_jp_font(verbose=True)

# ===== プロット =====
plt.figure(figsize=(10, 6))
plt.plot(df["quarter"], df["revenue_jpy"], marker="o", linewidth=2)
plt.title("カテゴリ716（適性検査）の四半期別売上推移", fontsize=14)
plt.xlabel("四半期", fontsize=12)
plt.ylabel("売上金額（円）", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.6)

# 売上金額の単位を分かりやすく（万円表示など）
ymax = df["revenue_jpy"].max()
if ymax > 1_000_000:
    plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x/1_000_000:.1f}M"))

# 軸ラベルの重なり防止
plt.xticks(rotation=45, ha="right")

# ===== 出力 =====
os.makedirs(os.path.join(BASE_DIR, ".output"), exist_ok=True)
out_path = os.path.join(BASE_DIR, ".output", "id716_3_quarterly_sales.png")
plt.tight_layout()
plt.savefig(out_path, dpi=160)
print(f"✅ 画像を保存しました: {out_path}")
plt.show()
