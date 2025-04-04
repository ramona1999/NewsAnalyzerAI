import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")


class Summarizer:
    """
    A wrapper for summarizing text using Groq API.
    """

    def __init__(self, model="llama-3.1-8b-instant", api_key=groq_api_key):
        """
        Initializes the Summarizer with Groq API.

        Args:
            model (str): The model name to use (default: 'llama3-70b').
            api_key (str): API key for Groq API.
        """
        self.model = model
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY is missing. Set it in environment variables."
            )

        self.client = Groq(api_key=self.api_key)

    def summarize(self, text, detailed=False):
        """
        Summarizes the given text using Groq API.

        Args:
            text (str or list): The text to summarize (single string or list of chunks).
            detailed (bool): If True, requests a more detailed summary.

        Returns:
            str: The summarized text.
        """
        if isinstance(text, list):
            text = " ".join(text)

        prompt = (
            "You are provided with text from a news article. Provide a concise summary while capturing key points which are would help in comparitive analysis with other articles."
            if detailed
            else "Provide a concise summary of this text: "
        ) + text

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a highly skilled summarization AI.",
                    },
                    {"role": "user", "content": prompt},
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=200,
            )

            return chat_completion.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error: {e}")
            return text
