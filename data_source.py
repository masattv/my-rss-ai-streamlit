import feedparser

def fetch_rss_articles(feed_urls):
    """
    複数のRSSフィードURLを順にパースし、タイトル・リンク・要約(summary)などをまとめて返す
    """
    articles = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # RSSのentryによりフィールドが違う場合があるので安全に取得
            title = getattr(entry, "title", "")
            link = getattr(entry, "link", "")
            summary = getattr(entry, "summary", "")  # 記事の要約や冒頭文が入ることが多い
            published = getattr(entry, "published", "")
            articles.append({
                "title": title,
                "link": link,
                "summary": summary,
                "published": published
            })
    return articles
