from fastapi import FastAPI
from fastapi.responses import FileResponse
from utils import (
    NewsExtractor,
    DataHandler,
    ComparativeAnalysis,
    Translator,
    TextToSpeech,
)
from dotenv import load_dotenv
import os
import re
import pandas as pd

load_dotenv()
app = FastAPI()

api_key = os.getenv("newsapi")


@app.get("/full-analysis/{company}")
def full_analysis(company: str):
    news = NewsExtractor(api_key)
    data_handler = DataHandler(news)

    raw_links = news.company_news_links(company)

    for link in raw_links:
        news.extract_news_info(link)

    df = data_handler.load_data()
    if df is None or df.empty:
        return {"message": "No news data available"}

    comparative_analysis = ComparativeAnalysis()
    comparative_summary = comparative_analysis.generate_comparative_report(df)

    hindi_translator = Translator()
    translated_summary = hindi_translator.translate_text(comparative_summary)

    tts = TextToSpeech()
    text = re.sub(r"\*\*|\*", "", translated_summary)
    audio_path = tts.text_to_speech(text)

    # Return relative path instead of full system path
    audio_filename = os.path.basename(audio_path)
    audio_url = f"http://host.docker.internal:8000/audio/{audio_filename}"

    return {
        "news_data": df.to_dict(orient="records"),
        "comparative_summary": comparative_summary,
        "translated_summary": translated_summary,
        "audio_path": audio_url,
    }


# Serve audio files
@app.get("/audio/{filename}")
def get_audio(filename: str):
    file_path = os.path.join("audio_files", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg")
    return {"error": "File not found"}
