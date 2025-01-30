import streamlit as st

from data_source import fetch_rss_articles
from filter_and_cache import filter_ai_articles, is_cached, mark_cached
from ai_summarizer import batch_summary

# RSSフィードのURL。テスト用にAI系ニュースサイトなどを指定
RSS_URLS = [
    "https://business.nikkei.com/rss/sns/nb.rdf",
    "https://www.businessinsider.jp/feed/index.xml",
    "https://xtech.nikkei.com/rss/xtech-it.rdf",
    "https://rss.itmedia.co.jp/rss/2.0/aiplus.xml",
    "https://b.hatena.ne.jp/hotentry/it.rss",
    "https://b.hatena.ne.jp/q/ai?users=5&mode=rss&sort=recent",
    "https://zenn.dev/topics/機械学習/feed",
    "https://zenn.dev/topics/ai/feed",
    "https://zenn.dev/topics/生成ai/feed",
    "https://zenn.dev/topics/deeplearning/feed",
    "https://zenn.dev/topics/llm/feed",
    "https://zenn.dev/topics/nlp/feed",
    "https://zenn.dev/topics/python/feed",
    "https://zenn.dev/topics/googlecloud/feed",
    "https://cloudblog.withgoogle.com/rss/",
    "https://cloudblog.withgoogle.com/ja/rss/",
    "https://blog.g-gen.co.jp/feed",
    "https://jamesg.blog/2024/05/23/hf-papers-rss/",
    "https://www.techno-edge.net/rss20/index.rdf"
]

def main():
    st.title("AIニュースまとめ (Streamlit版)")

    st.write("""
        ボタンを押すとRSSフィードを取得して、タイトルに「AI」「ChatGPT」が含まれる記事だけを抽出し、
        Gemini APIで簡単に要約して表示します。
        """)

    # 記事数を選択するセレクトボックス
    num_articles = st.selectbox(
        "要約する記事数を選択してください",
        options=[5, 10, 50],
        index=0
    )

    if st.button("最新記事を要約する"):
        articles = fetch_rss_articles(RSS_URLS)
        st.write(f"取得した記事数: {len(articles)}")

        # フィルタ
        filtered = filter_ai_articles(articles, keywords=["AI","ChatGPT"])
        
        # キャッシュされていない記事のみを処理
        articles_to_summarize = []
        all_articles = []
        
        for art in filtered[:num_articles]:
            link = art["link"]
            if not is_cached(link):
                # タイトル + 既存summary を要約対象に追加
                text_for_ai = f"{art['title']}\n{art['summary']}"
                articles_to_summarize.append({
                    "text": text_for_ai,
                    "article": art
                })
            mark_cached(link)

        # 一括要約
        if articles_to_summarize:
            texts = [item["text"] for item in articles_to_summarize]
            summaries = batch_summary(texts, max_articles=num_articles, max_length=100)
            
            # 要約結果と元の記事情報をマッチング
            for i, summary in enumerate(summaries):
                art = articles_to_summarize[i]["article"]
                all_articles.append({
                    "title": art["title"],
                    "link": art["link"],
                    "published": art["published"],
                    "summary": summary
                })

        # 表示
        if all_articles:
            st.subheader(f"要約されたAI関連ニュース（{len(all_articles)}件）")
            for item in all_articles:
                st.markdown(f"### [{item['title']}]({item['link']})")
                st.write(f"**要約**: {item['summary']}")
                st.write(f"_公開日: {item['published']}_")
                st.write("---")
        else:
            st.write("新たに要約すべきAI関連ニュースはありません。")

if __name__ == "__main__":
    main()
