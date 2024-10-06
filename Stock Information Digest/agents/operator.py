from agents.agent import Agent
from tools.stockretriever import get_current_info
from models.portfolio import Portfolio
import re


class OperatorAgent(Agent):
    def __init__(self, portfolio):
        super().__init__()
        self.portfolio = portfolio

    def parse_recommendation(self, recommendation_text):
        """
        Parses the recommendation text into a triplet of (ticker symbol, quantity, buy/sell action).

        :param recommendation_text: The text containing the recommendation, e.g., "Buy 100 shares of AAPL"
        :return: A list of parsed recommendations [(symbol, volume, action)]
        """
        prompt = f"""
                You are an investment operator. You will be given a text containing stock recommendations in natural language.
                Your job is to extract the following details in the exact format:
                (TICKER, quantity, action)

                Here is the recommendation text: {recommendation_text}

                Please return the parsed result in the exact format: (TICKER, quantity, action)
                """

        # Call OpenAI API
        response = self.call_openai_api("Parse stock recommendation", prompt)

        # Use regex to extract the triplets (TICKER, quantity, action)
        # Regex Explanation: Matches (symbol, quantity, action)
        # Example match: (AAPL, 100, buy)
        pattern = r'\((\w+),\s*(\d+),\s*(buy|sell)\)'
        matches = re.findall(pattern, response)

        # Convert matches into a list of tuples (symbol, quantity, action)
        parsed_recommendations = [(match[0], int(match[1]), match[2]) for match in matches]
        print(parsed_recommendations)

        return parsed_recommendations

    def execute_recommendation(self, parsed_recommendations):
        """
        Executes parsed stock recommendations by calling the appropriate portfolio functions.

        :param parsed_recommendations: A list of parsed recommendations [(symbol, volume, action)]
        """
        for symbol, quantity, action in parsed_recommendations:
            current_price = self.get_current_price(symbol)
            if action == 'buy':
                try:
                    self.portfolio.buy_stock(symbol, quantity, current_price)
                    print(f"Executed: Bought {quantity} shares of {symbol} at ${current_price}")
                except ValueError as e:
                    print(f"Failed to execute buy for {symbol}: {e}")
            elif action == 'sell':
                try:
                    self.portfolio.sell_stock(symbol, quantity, current_price)
                    print(f"Executed: Sold {quantity} shares of {symbol} at ${current_price}")
                except ValueError as e:
                    print(f"Failed to execute sell for {symbol}: {e}")

    def get_current_price(self, symbol):
        """
        Retrieves the current stock price using the stockretriever's functionality.
        This function could be replaced with a real API call or a mock for testing.

        :param symbol: The stock ticker symbol.
        :return: The current price of the stock.
        """
        return get_current_info([symbol])[0]['currentPrice']