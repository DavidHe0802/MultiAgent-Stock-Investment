from agents.agent import Agent
import re

class CEOAgent(Agent):
    def __init__(self):
        super().__init__()

    def review_and_assign_tasks(self, performance_report):
        """
        Ingests the portfolio performance report and generates tasks for Warren Buffet to execute.

        :param performance_report: A structured performance report containing portfolio performance and key metrics.
        :return: A set of tasks/objectives for Warren Buffet agent to execute.
        """
        # Define the system instruction for the CEO to critically assess the report and state objectives
        system_instruction = """
        You are a seasoned CEO of an investment firm. 
        Based on the performance report provided, critically assess the current portfolio performance.
        Identify the strengths, weaknesses, and areas of concern, and think carefully about how to improve the portfolio's future performance.
        Generate a clear set of objectives and tasks for Warren Buffet to execute, including reviewing specific stocks, adjusting strategies, 
        and suggesting new investment opportunities if necessary. 
        Be specific and prioritize based on importance.
        """

        # Use the OpenAI API to generate tasks based on the performance report
        tasks_prompt = f"""
        Performance Report: 
        {performance_report}

        Based on this performance report, what objectives and tasks should be assigned to Warren Buffet to improve the portfolio?
        """

        tasks = self.call_openai_api(system_instruction, tasks_prompt)

        # Return the generated tasks
        return tasks

    def evaluate_recommendations(self, recommendations, performance_review):
        """
        Evaluate Buffet's recommendation by using the OpenAI API to simulate the CEO's thought process.
        The evaluation is based on a detailed rubric and will return 'approve' or 'revise' depending on the score.

        :param recommendations: Buffet's recommendations for buy/sell/hold decisions.
        :return: 'approve' or 'revise' based on the evaluation score.
        """
        # System instruction for OpenAI
        rubric_prompt = f"""
        You are a seasoned CEO of a major investment firm. Your role is to critically evaluate the recommendations 
        provided by Warren Buffet, based on the following rubric:

        Rubric:
        1. **Alignment with Long-term Strategy (30 points)**: Does the recommendation align with the company's 
           long-term strategic goals?
        2. **Risk Assessment (25 points)**: Is the recommendation appropriately risk-averse or well-justified 
           based on current market conditions?
        3. **Market Timing (15 points)**: Does the recommendation demonstrate good timing in the context of the 
           current market conditions?
        4. **Financial Analysis (20 points)**: Is the financial analysis and valuation sound and does it justify 
           the recommendation?
        5. **Past Performance (10 points)**: Does the recommendation take into account the past performance of 
           the stock or similar strategies?

        You will score the recommendation from 0 to 100, with each category weighted as described above. 
        A score above 90 indicates approval, while any score below 90 requires revision.

        Use the following data to guide your evaluation:
        1. Buffet's Recommendations: {recommendations}
        2. Performance Review: {performance_review}

        Based on the rubric, please score the recommendation in the first line of your response and nothing else.
        Provide detailed reasoning for each score category, including specific references to the recommended stocks.
        """

        # Call OpenAI API to evaluate the recommendation based on the rubric
        evaluation = self.call_openai_api(rubric_prompt, recommendations)

        # Extract score and approval decision from the API's response
        score_match = re.search(r'\b\d{1,3}\b', evaluation)
        if score_match:
            score = int(score_match.group(0))
        else:
            raise ValueError("No score found in the evaluation response.")

        # Decision-making based on the score
        if score > 88:
            print(f"Recommendation approved with a score of {score}")
            return 'approve', evaluation
        else:
            print(f"Recommendation requires revision with a score of {score}")
            return 'revise', evaluation