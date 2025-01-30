# ai_summarizer.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL", "")

def short_summary(text, max_length=100):
    """単一記事の要約を生成する"""
    if not GEMINI_API_KEY or not GEMINI_BASE_URL:
        return "（Gemini設定が未完了です）"
    
    endpoint = f"{GEMINI_BASE_URL}?key={GEMINI_API_KEY}"

    prompt = f"""
以下の記事を日本語で{max_length}文字程度に要約してください。
要約は簡潔で分かりやすい日本語にしてください。

記事:
{text}
"""

    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }

    headers = {"Content-Type": "application/json"}

    try:
        resp = requests.post(endpoint, json=data, headers=headers)
        if resp.status_code == 200:
            return resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "要約データが取得できませんでした。")
        else:
            return f"要約失敗: {resp.status_code} {resp.text}"
    except Exception as e:
        return f"(要約失敗: {str(e)})"

def batch_summary(texts, max_articles=10, max_length=100):
    """複数記事の要約を生成する"""
    if not texts:
        return []
    
    # 指定された件数まで記事を制限
    texts = texts[:max_articles]
    
    # 各記事を要約
    summaries = []
    for text in texts:
        summary = short_summary(text, max_length)
        summaries.append(summary)
    
    return summaries
