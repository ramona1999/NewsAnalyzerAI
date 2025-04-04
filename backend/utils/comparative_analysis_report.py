import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


class ComparativeAnalysis:
    """
    A wrapper to generate a comparative analysis report based on articles' sentiment, keywords, and summaries using Groq API.
    """

    def __init__(self, model="llama3-70b-8192", api_key=groq_api_key):
        """
        Initializes the ComparativeAnalysis class with Groq API.

        Args:
            model (str): The model name to use (default: 'gemma2-9b-it').
            api_key (str): API key for Groq API.
        """
        self.model = model
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY is missing. Set it in environment variables."
            )

        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)

    def prepare_comparison_prompt(self, data):
        """
        Prepares the prompt by iterating through the dataframe and extracting necessary fields for comparison.

        Args:
            data (pd.DataFrame): The dataframe containing the articles' data (title, summary, sentiment, keywords).

        Returns:
            str: A formatted prompt for the model.
        """
        prompt = "Compare the following articles based on sentiment, keywords, and summaries:\n\n"

        for i, row in data.iterrows():
            prompt += f"""{i + 1}. **Title**: {row['title']}
            **Date**: {row['published_date']}
            **Summary**: {row['summary']}
            **Keywords**: {row['meta_keywords']}
            **Sentiment**: {row['sentiment']}
            \n"""

        prompt += (
            "\nComparison highlighting how news coverage differs in various reports. Help user form an opinion on the news. do not use Key Takeways or Recommendations."
            "Final output should be structured comparative analysis report with focus on comparative sentiment score including Sentiment Distribution, Coverage differences, topic overlap, final Sentiment Analysis."
        )

        return prompt

    def generate_comparative_report(self, data):
        """
        Uses the Groq API to generate a comparative analysis report based on the provided data.

        Args:
            data (pd.DataFrame): The dataframe containing articles' data (title, summary, sentiment, keywords).

        Returns:
            str: The comparative analysis report.
        """
        # Prepare the comparison prompt
        prompt = self.prepare_comparison_prompt(data)

        try:
            # Send the prompt to the Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI trained to generate comparative analysis reports.",
                    },
                    {"role": "user", "content": prompt},
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=1000,  # Adjust as needed based on response length
            )

            # Return the response content
            return chat_completion.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error generating report: {e}")
            return "Error generating comparative report."
