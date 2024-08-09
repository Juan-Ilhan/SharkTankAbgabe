import json
from scrapegraphai.graphs import SmartScraperGraph


class ScrapeGraphAgent:
    def __init__(self, api_key):
        self.api_key = api_key

    def search_web(self, query):
        graph_config = {
            "llm": {
                "api_key": self.api_key,
                "model": "gpt-4o-mini",
            },
            "verbose": True,
            "headless": True,
        }

        smart_scraper_graph = SmartScraperGraph(
            prompt=f"Find information about: {query}",
            source=f"https://www.google.com/search?q={query.replace(' ', '+')}",
            config=graph_config
        )

        result = smart_scraper_graph.run()
        return result

    def scrape_feedback(self):
        graph_config = {
            "llm": {
                "api_key": self.api_key,
                "model": "gpt-4o-mini",
            },
            "verbose": True,
            "headless": True,
        }

        feedback_scraper = SmartScraperGraph(
            prompt="Extract customer feedback, reviews, and one detailed review about Hampton Adams athletic tape from this page.",
            source="https://hamptonadams.com/products/hampton-adams-32-pack-white-bulk-athletic-tape-1-5-x-45-feet-per-roll-no-sticky-residue-easy-to-tear-perfect-for-sports-athletes",
            config=graph_config
        )

        result = feedback_scraper.run()
        return result

    def analyze_results(self, search_results, feedback_results=None):
        if not search_results:
            return "No relevant information found from web search."

        combined_text = " ".join(f"{key}: {value}" for key, value in search_results.items())

        if feedback_results:
            feedback_text = " ".join(f"{key}: {value}" for key, value in feedback_results.items())
            return combined_text + "\n\nCustomer Feedback:\n" + feedback_text

        return combined_text
