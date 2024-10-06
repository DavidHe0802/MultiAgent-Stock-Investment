from openai import OpenAI

API_KEY = "Your_OpenAI_API_Key"

class Agent:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY)

    def call_openai_api(self, instruction, prompt):
        """
        This function calls the OpenAI API to generate a response based on the given instruction and prompt.
        """
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": instruction},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response = completion.choices[0].message.content
        # print(response)
        # Extract the content correctly from the response
        return response