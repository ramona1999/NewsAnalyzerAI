import requests
import json
import pandas as pd
import csv
from datetime import datetime, timedelta
import trafilatura


class NewsExtractor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.dataframe = pd.DataFrame(
            columns=[
                "title",
                "published_date",
                "source",
                "link",
                "text",
                "meta_keywords",
            ]
        )

    def company_news_links(self, company_name, days=20, limit=10):
        date = datetime.now()
        from_date = (date - timedelta(days=days)).strftime("%Y-%m-%d")

        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={company_name}&"
            f"from={from_date}&"
            f"sortBy=popularity&"
            f"language=en&"
            f"apiKey={self.api_key}"
        )

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if "articles" not in data:
                print("No articles found.")
                return []

            articles = data["articles"]
            unique_sources = set()
            filtered_articles = []

            for article in articles:
                source_name = article.get("source", {}).get("name", "Unknown Source")
                title = article.get("title", "")
                description = article.get("description", "")
                article_url = article.get("url", "")

                if (
                    title
                    and description
                    and company_name.lower() in (title + description).lower()
                ):
                    if source_name not in unique_sources:
                        unique_sources.add(source_name)
                        filtered_articles.append(article_url)

                if len(filtered_articles) >= limit:
                    break

            return filtered_articles

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []

    def extract_news_info(self, url):
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            extracted_data = trafilatura.extract(
                downloaded, output_format="json", with_metadata=True
            )
            if extracted_data:
                article_data = json.loads(extracted_data)
                news_entry = {
                    "title": article_data.get("title", "No Title"),
                    "published_date": article_data.get("date", "No Date"),
                    "source": article_data.get("hostname", "No Source"),
                    "link": url,
                    "text": article_data.get("text", "No Summary"),
                    "meta_keywords": (
                        article_data.get("tags", "").split(",")
                        if article_data.get("tags")
                        else []
                    ),
                }

                self.dataframe = pd.concat(
                    [self.dataframe, pd.DataFrame([news_entry])], ignore_index=True
                )
                return news_entry
            else:
                print("Failed to extract metadata.")
        else:
            print(f"Failed to fetch: {url}")
        return None

    def get_dataframe(self):
        return self.dataframe
