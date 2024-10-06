import datetime
from agents.ceo import CEOAgent
from agents.warren_buffet import WarrenBuffetAgent
from agents.analyst import AnalystAgent
from agents.secretary import SecretaryAgent
from agents.MarketResearchAgent import MarketResearchAgent
from agents.operator import OperatorAgent
from models.portfolio import Portfolio
import time

class OfficeSimulation:
    def __init__(self, the_portfolio):
        self.portfolio = the_portfolio
        self.ceo = CEOAgent()
        self.buffet = WarrenBuffetAgent()
        self.analyst = AnalystAgent()
        self.research_agent = MarketResearchAgent()
        self.secretary = SecretaryAgent()
        self.operator = OperatorAgent(self.portfolio)

    def run_daily_cycle(self):
        """
        Executes the daily cycle of stock investment, logging each step in the process.
        """

        today = datetime.date.today().strftime('%Y-%m-%d')
        print(f"""Today is {today}, let's make some money!""")

        # 1. CEO reviews performance and outlines tasks
        print("CEO is reviewing portfolio performance and outlining tasks!")
        performance_review = self.portfolio.get_performance_report()
        tasks = self.ceo.review_and_assign_tasks(performance_review)
        meeting_notes = []

        while True:

            print(f"\n*** Stock investment meeting round {len(meeting_notes) + 1} ***")

            # 2. Buffet raises market questions based on the tasks
            print("Buffett is thinking about market information!")
            market_questions = self.buffet.raise_market_questions(tasks)

            # 3. Research agent fetches market information
            print("Market Research Agent is gathering market information!")
            market_info = self.research_agent.fetch_market_information(market_questions)

            # 4. Buffet reviews market info and decides which stock trends to investigate
            print("Buffett is deciding which stocks to investigate further!")
            stock_trend_request = self.buffet.decide_stocks_for_trend_analysis(market_info)

            # 5. Research agent retrieves stock trend data
            print("Market Research Agent is retrieving stock trend data!")
            price_trends = self.research_agent.get_stock_price_history(stock_trend_request)

            # 6. Analyst agent analyzes the stock price trends and provides a report
            print("Analyst is analyzing the stock price trends!")
            analysis_report = self.analyst.analyze_stock_data(price_trends)

            # 7. Buffet makes final decisions based on the analysis report
            print("Buffett is making final decisions based on the analysis report!")
            recommendations = self.buffet.make_final_decision(performance_review, market_questions, price_trends,
                                                              stock_trend_request, market_info)

            # 8. CEO evaluates recommendations
            print("CEO is evaluating Buffett's recommendations!")
            decision, feedback = self.ceo.evaluate_recommendations(recommendations, performance_review)

            # 9. Secretary takes notes
            print("Secretary is generating meeting notes!")
            meeting_note = self.secretary.generate_meeting_notes(tasks, market_questions, market_info,
                                                                 stock_trend_request, analysis_report,
                                                                 recommendations, feedback)
            meeting_notes.append(meeting_note)

            if decision == 'approve':
                # 10. Update portfolio based on approved recommendations
                print("CEO approved recommendations!")
                print("Generating the daily report with all meeting notes!")
                daily_report = self.generate_daily_report(meeting_notes)
                print("Operator is executing the approved recommendations!")
                execution = self.operator.parse_recommendation(recommendations)
                self.operator.execute_recommendation(execution)
                break

            # if len(meeting_notes) > 5:
            #     # 10. Update portfolio based on approved recommendations
            #     print("Enough time for today's meeting, let's just go from there!")
            #     print("Generating the daily report with all meeting notes!")
            #     daily_report = self.generate_daily_report(meeting_notes)
            #     execution = self.operator.parse_recommendation(recommendations)
            #     self.operator.execute_recommendation(execution)
            #     break

            # Loop with the updated tasks based on meeting notes
            tasks = f"""
            Your recent stock recommendation has been reviewed by the CEO of the investment firm, 
            and feedback has been provided for revision. 
            You need to change the stock choice/ stock quantity in your portfolio.

            Original Recommendation:
            {recommendations}
            
            CEO's Feedback:
            {feedback}
            """

        # 11. Generate daily report
        ledger_report = self.portfolio.generate_ledger_report()
        return ledger_report

    def generate_daily_report(self, meeting_notes):
        """
        Generate a daily report (meeting notes) and save it to a txt file with today's date.
        :param meeting_notes: The compiled meeting notes (string) from the SecretaryAgent.
        """
        # Get today's date to use in the filename
        today = datetime.date.today().strftime('%Y-%m-%d')

        # Define the filename using today's date
        filename = f"meeting_notes_{today}.txt"

        # Write the meeting notes to the file
        for meeting_note in meeting_notes:
            with open(filename, 'a') as file:
                file.write(meeting_note)

        print(f"Meeting notes saved as {filename}")

# Main execution
# this runs forever
if __name__ == "__main__":
    portfolio = Portfolio()
    office = OfficeSimulation(portfolio)
    while True:
        daily_report = office.run_daily_cycle()
        print(daily_report)
        # Wait for next day (you might want to implement a proper scheduling mechanism)
        time.sleep(80400)