from tools.stockretriever import get_historical_info
from agents.agent import Agent
import requests
from datetime import datetime, timedelta

NEWS_API_KEY = 'YourNewsAPIKey'

class MarketResearchAgent(Agent):
    def __init__(self):
        super().__init__()

    def fetch_market_information(self, questions):
        """
                Ingests multiple questions raised by Buffet, generates search strings,
                and retrieves news information for each. Summarizes each search result
                and compiles the findings together.

                :param questions: Questions raised by Warren Buffet in need of market information.
                :return: Compiled summary of market information for each question.
                """
        # Instruction to generate search strings for each question
        search_instruction = """
                You are a market research expert. Based on the following questions, generate a search string 
                for each question that can be used to look for relevant news or market information.
                Make sure to return one search string per question.
                """

        # Generate search strings using the OpenAI API for each question
        search_strings = self.call_openai_api(search_instruction, questions)

        # Split the search strings into a list (assuming one search string per line or comma-separated)
        search_terms = search_strings.split(",") if ',' in search_strings else search_strings.split("\n")

        # Summarize the news for each search term
        compiled_summary = []
        for search_term in search_terms:
            market_news = self.fetch_news_from_api(search_term)
            summary_instruction = """
                    You are a financial expert. Summarize the following news articles and information:
                    """
            summarized_market_info = self.call_openai_api(summary_instruction, market_news)
            compiled_summary.append(f"Results for '{search_term}':\n{summarized_market_info}\n")

        # Return the compiled summary of all search results
        return "\n".join(compiled_summary)

    def fetch_news_from_api(self, search_strings):

        """
        Fetches news articles from an external API based on search strings and summarizes the results.

        :param search_strings: Search terms generated based on Buffet's questions.
        :return: Summarized news information as a string.
        """
        api_key = NEWS_API_KEY
        base_url = "https://newsapi.org/v2/everything"

        summarized_news = []

        # Iterate over each search string and fetch relevant news
        for search_term in search_strings.split(","):
            params = {
                'q': search_term + " public traded company",
                'apiKey': api_key,
                'language': 'en',
                'sortBy': 'relevancy',
                'pageSize': 5  # Fetch top 5 articles for each search term
            }

            try:
                response = requests.get(base_url, params=params)
                response.raise_for_status()  # Raise error for bad responses
                articles = response.json().get('articles', [])

                # Summarize fetched articles
                if articles:
                    for article in articles:
                        summary = f"Title: {article['title']}\nDescription: {article['description']}\nURL: {article['url']}\n"
                        summarized_news.append(summary)
                else:
                    summarized_news.append(f"No relevant articles found for {search_term}.")

            except Exception as e:
                summarized_news.append(f"Error fetching news for {search_term}: {e}")

        # Return summarized news as a single string
        return "\n\n".join(summarized_news)

    def get_stock_price_history(self, stock_trend_request):
        """
        Retrieves stock price history for specific tickers.
        """
        # Instruction to retrieve stock price history
        trend_instruction = """
        Parse the input information and output only ticket number in the text, seperated by comma.
        """

        tickers = self.call_openai_api(trend_instruction, stock_trend_request)
        print(f"Those are the stocks Warren Buffett recommends her to look at: {tickers}")

        # Call DBManager or external API to get historical price data
        price_data = {}
        for ticker in tickers.split(","):
            end_date = datetime.now()
            start_date = end_date - timedelta(days=120)
            # Assuming start_date and end_date are provided elsewhere or within the prompt
            price_data[ticker] = get_historical_info(ticker.strip(), start_date, end_date)

        return price_data
