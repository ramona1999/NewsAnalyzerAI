import pandas as pd
from .news_fetcher import NewsExtractor
from .summarization import Summarizer
from .text_preprocessing import SentenceChunker
from .sentiment_analysis import SentimentAnalyzer  # Import SentimentAnalyzer


class DataHandler:
    def __init__(self, news_extractor):
        self.news_extractor = news_extractor  # Store the NewsExtractor instance
        self.summarizer = Summarizer()  # Initialize the Summarizer
        self.text_processor = SentenceChunker()  # Initialize text processor
        self.sentiment_analyzer = SentimentAnalyzer()  # Initialize SentimentAnalyzer

    def load_data(self):
        data = self.news_extractor.get_dataframe()
        if data.empty:
            print("No data found.")
            return None

        # Process and summarize each article
        summaries = []
        sentiments = []
        for text in data["text"]:
            processed_text = self.text_processor.preprocess(text)
            summary = "".join(
                self.summarizer.summarize(chunk) for chunk in processed_text
            )
            summaries.append(summary)

            # Analyze sentiment of the summary
            sentiment = self.sentiment_analyzer.analyze_summary(summary)
            sentiments.append(sentiment)

        # Add summaries and sentiments to DataFrame
        data["summary"] = summaries
        data["sentiment"] = sentiments
        return data
