import os

# 簡易的にPythonのグローバル変数を使ったキャッシュ例
# 実際には、streamlitの session_state やファイル/DBを使うなど拡張可能
_CACHED_URLS = set()

def filter_ai_articles(articles, keywords=["AI", "ChatGPT"]):
    """
    タイトルに任意のキーワードが含まれる記事だけを返す
    """
    filtered = []
    for art in articles:
        title_lower = art["title"].lower()
        if any(k.lower() in title_lower for k in keywords):
            filtered.append(art)
    return filtered

def is_cached(url):
    """ すでに要約済みURLか判定 """
    return url in _CACHED_URLS

def mark_cached(url):
    """ 要約済みURLをキャッシュに登録 """
    _CACHED_URLS.add(url)
