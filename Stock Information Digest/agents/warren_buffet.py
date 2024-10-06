from agents.agent import Agent


BUFFET_PHILOSOPHY = """
        You are Warren Buffet, a legendary investor who follows a value-investing philosophy. 
        You focus on buying companies that are undervalued, with strong fundamentals and a long-term outlook.
        You prefer quality businesses with a strong competitive moat, consistent earnings, and low debt. 
        You avoid short-term market volatility and prioritize patience and discipline in all investment decisions.
        Your goal is to identify opportunities that align with your value investing principles.
        """

class WarrenBuffetAgent(Agent):
    def __init__(self):
        super().__init__()

    def raise_market_questions(self, tasks):
        """
        Buffet raises questions based on the tasks assigned by the CEO.
        """

        task_prompt = f"""
                Tasks from CEO:
                {tasks}

                Based on these tasks, use your knowledge, think carefully and raise some questions about the specific markets.
                What are some markets you would like to know more about companies in it?
                """
        questions_for_research = self.call_openai_api(BUFFET_PHILOSOPHY, task_prompt)
        return questions_for_research

    def decide_stocks_for_trend_analysis(self, market_info):
        """
        Based on market information, Buffet decides which stock symbols to investigate further.
        """
        buffet_philosophy = """
                You are Warren Buffet, a legendary investor who follows a value-investing philosophy. 
                You focus on buying companies that are undervalued, with strong fundamentals and a long-term outlook.
                You prefer quality businesses with a strong competitive moat, consistent earnings, and low debt. 
                You avoid short-term market volatility and prioritize patience and discipline in all investment decisions.
                Your goal is to identify opportunities that align with your value investing principles.
                """
        analysis_prompt = f"""
                Based on the following market information:
                {market_info}

                Which stock symbols (tickers) do you want to investigate further? 
                Provide a rationale for each ticker and ask for price trends.
                """
        stock_trend_request = self.call_openai_api(BUFFET_PHILOSOPHY, analysis_prompt)
        return stock_trend_request

    def make_final_decision(self, performance_review, market_question, price_trends, stock_question, market_info):
        """
        Buffet makes a final decision based on the stock trend analysis and market information.
        """
        final_decision_prompt = f"""
                Based on your thought flow:
                
                0, current portfolio performance and cash available
                {performance_review}

                1, query the market information
                {market_question}

                2, obtained the market information
                {market_info}

                3, query the specific stocks
                {stock_question}

                4, obtained the stock trend
                {price_trends}

                Make a final recommendation on whether to buy, sell, or hold for each stock. 
                Be very specific about what stock ticket you want to buy or sell, and how much will you buy or sell.
                Explain the reasoning for each decision.
                
                At the end of your recommendation, you should provide your recommended actions like a triplet:
                (TICKER, quantity, sell/buy)
                """
        final_recommendation = self.call_openai_api(BUFFET_PHILOSOPHY, final_decision_prompt)

        return final_recommendation