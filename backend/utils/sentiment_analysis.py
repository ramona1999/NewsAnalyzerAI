from transformers import pipeline
import nltk

# Download punkt_tab to the correct directory at runtime if needed
nltk.download("punkt_tab", download_dir="/app/nltk_data")
# Set the path in your code before using NLTK
from nltk.tokenize import sent_tokenize


class SentimentAnalyzer:
    def __init__(self, model_name="ProsusAI/finbert"):
        """
        Initializes the sentiment analysis pipeline.
        Args:
            model_name (str): Name of the transformer model to use for sentiment analysis.
        """
        self.sentiment_analyzer = pipeline("sentiment-analysis", model=model_name)

    def analyze_text(self, text):
        """
        Analyzes sentiment for a single text input.
        Args:
            text (str): The text to analyze.
        Returns:
            str: The predicted sentiment label.
        """
        result = self.sentiment_analyzer(text)[0]
        return result["label"].capitalize()

    def analyze_summary(self, summary):
        """
        Analyzes sentiment for a long summary by splitting it into sentences.
        Args:
            summary (str): The long text to analyze.
        Returns:
            str: The most frequent sentiment label.
        """
        sentences = sent_tokenize(summary)
        sentiments = [self.analyze_text(sentence) for sentence in sentences]

        sentiment_counts = {label: sentiments.count(label) for label in set(sentiments)}
        overall_sentiment = max(sentiment_counts, key=sentiment_counts.get)

        return overall_sentiment
