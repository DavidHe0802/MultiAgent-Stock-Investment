import numpy as np
import pandas as pd
from agents.agent import Agent


class AnalystAgent(Agent):
    def __init__(self):
        super().__init__()

    def analyze_stock_data(self, price_data):
        """
        Analyzes stock price history and generates a report with quantitative analysis and predictions.

        :param price_data: Dictionary containing stock price history for multiple tickers.
        :return: An analysis report with predictions and suggestions.
        """
        analysis_report = []

        for ticker, data in price_data.items():
            analysis_prompt = f"""
            You are a financial analyst specializing in quantitative finance, financial modeling, 
            and financial engineering. Analyze the historical price data for {ticker}, and create 
            an analysis report. Include trends, statistical insights, and make a prediction for the next quarter.

            Historical Data (Sample):
            {data}
            """

            # Call OpenAI API to generate the analysis report for each ticker
            report = self.call_openai_api("Financial analysis expert", analysis_prompt)
            analysis_report.append(f"Analysis Report for {ticker}:\n{report}\n")

        return "\n".join(analysis_report)