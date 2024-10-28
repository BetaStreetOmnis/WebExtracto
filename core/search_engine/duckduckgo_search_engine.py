from duckduckgo_search import DDGS

class DuckDuckGoSearchEngine:
    def __init__(self, keyword, max_results=10):
        print('duck')
        self.keyword = keyword
        self.max_results = max_results

    def fetch_duckduckgo_results(self):
        try:
            results = DDGS().text(self.keyword, max_results=self.max_results)
            return results
        except Exception as e:
            print(f"Error fetching {e}")
            return None

    def parse_html(self, results):
        parsed_results = []
        for result in results:
            parsed_results.append({
                'url': result['href'],
                'title': result['text'],
                'snippet': result['description']
            })
        return parsed_results

    def search(self):
        results = self.fetch_duckduckgo_results()
        if results:
            return self.parse_html(results)
        else:
            return []

if __name__ == "__main__":
#     # 运行样例
    query = "python web search"
    search_engine = DuckDuckGoSearchEngine(query, max_results=5)
    results = search_engine.search()
    print(results)
#     print(f"Search results for '{query}':")
#     for result in results:
#         print(f"Title: {result['title']}")
#         print(f"URL: {result['url']}")
#         if 'snippet' in result:
#             print(f"Snippet: {result['snippet']}")
