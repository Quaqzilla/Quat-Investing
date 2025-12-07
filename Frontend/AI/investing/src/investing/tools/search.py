from firecrawl import FirecrawlApp

firecrawl = FirecrawlApp(api_key="fc-YOUR-API-KEY")

def search():
    results = firecrawl.search(
        query = "Recent financial news for ",
        limit = 5,
        tbs="qdr:m",
    )

    return results