from agents.agent import Agent


class SecretaryAgent(Agent):
    def __init__(self):
        super().__init__()

    def generate_meeting_notes(self, original_tasks, market_questions, market_info, stock_trend_request,
                               analysis_report, previous_recommendation, ceo_feedback):
        """
        Generates a summary of the entire process and outputs it as meeting notes for Buffet to review.
        """
        meeting_notes_prompt = f"""
        You are a secretary tasked with creating a detailed meeting summary for Warren Buffet. 
        Here are the elements you need to summarize:

        1. **Original Tasks from CEO**: {original_tasks}
        2. **Market Questions Raised by Buffet**: {market_questions}
        3. **Market Information Gathered**: {market_info}
        4. **Stock Trend Requests**: {stock_trend_request}
        5. **Analysis Report from Analyst**: {analysis_report}
        6. **Previous Recommendations from Buffet**: {previous_recommendation}
        7. **CEO's Feedback**: {ceo_feedback}

        Create a cohesive and detailed meeting summary, highlighting all key points for Buffet to review.
        """

        # Use OpenAI to generate a clean, structured meeting note
        meeting_notes = self.call_openai_api("Secretary", meeting_notes_prompt)

        return meeting_notes