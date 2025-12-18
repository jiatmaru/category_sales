# common/bq_utils.py
from google.cloud import bigquery
import pandas as pd
import matplotlib
from matplotlib import font_manager

# ===== 日本語フォント設定関数 =====
def set_jp_font(verbose: bool = False):
    """日本語フォントを自動検出して設定する"""
    candidates = [
        "Yu Gothic", "Yu Gothic UI", "Meiryo", "Hiragino Sans",
        "Hiragino Kaku Gothic ProN", "Noto Sans CJK JP",
        "IPAGothic", "IPAexGothic", "MS Gothic"
    ]
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            matplotlib.rcParams["font.family"] = name
            matplotlib.rcParams["axes.unicode_minus"] = False
            if verbose:
                print(f"[INFO] 日本語フォント設定: {name}")
            return name
    if verbose:
        print("[WARN] 日本語フォントが見つかりませんでした。デフォルトフォントを使用します。")
    return None


def query_to_dataframe(sql: str, params: dict = None, project_id: str = None) -> pd.DataFrame:
    """BigQueryのSQLを直接DataFrameに読み込む共通関数"""
    client = bigquery.Client(project=project_id)

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(k, "STRING", v) for k, v in (params or {}).items()
        ]
    )

    query_job = client.query(sql, job_config=job_config)
    df = query_job.to_dataframe(create_bqstorage_client=True)

    return df

