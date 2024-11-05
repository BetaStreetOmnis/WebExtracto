from googlesearch import search

class GoogleSearchEngine:
    def __init__(self, keyword, max_results=10):
        self.keyword = keyword
        self.max_results = max_results

    def search_keyword_by_google(self):
        try:
            results = []
            for result in search(self.keyword, num_results=self.max_results, advanced=True):
                print(112233, result.url, result.title, result.description)
                results.append({
                    'url': result.url,
                    'title': result.title,
                    'description': result.description
                })
            print(444444, results)
            return results
        except Exception as e:
            print(f"Error fetching {e}")
            return []

    def search(self):
        return self.search_keyword_by_google()

# if __name__ == "__main__":
#     search_engine = GoogleSearchEngine("cloudwalk")
#     soup = search_engine.google_search()
#     print(soup)
