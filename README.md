# 📰 News Analysis App - Documentation

## Overview

This project is a full-stack, containerized news analysis tool that enables users to input a company name and receive:

- News article aggregation (via NewsAPI)
- Article summarization using a Groq-hosted LLM
- Sentiment analysis data frame with FinBERT (downloadable)
- Comparative reporting in English and Hindi
- Hindi audio summary generation (playable + downloadable)

The application features a **FastAPI backend** and a **Streamlit frontend**, all deployable via Docker Compose or hosted on **🤗 Hugging Face Spaces**.

Live Demo: 👉 [Try it on Hugging Face](https://ramonad2024-news-analysis-frontend.hf.space/)

![System Architecture](https://github.com/user-attachments/assets/b803496d-6230-4c7a-b1ec-d95c50eed7bd)
---

## Features

| Feature               | Description                                                             |
| --------------------- | ----------------------------------------------------------------------- |
| 🔎 News Fetching      | Uses NewsAPI to fetch top articles for a company                        |
| 👍 Summarization      | Uses `llama3-8b-instant` model via Groq for summarizing each article    |
| 😃 Sentiment Analysis | FinBERT sentiment analysis (positive, negative, neutral) with table & bar chart |
| 📊 Comparative Report | Summary across all articles, translated to Hindi                        |
| 🎧 Audio Summary      | Hindi summary converted to audio using `gTTS` (playable + downloadable) |

---

## System Architecture

```
User Input
   |
Frontend (Streamlit)
   |
v
Backend (FastAPI)
   |- /full-analysis/<company>
       |- Fetch News Articles
       |- Summarize Articles (LLM via Groq)
       |- Analyze Sentiment (FinBERT)
       |- Generate Comparative Summary
       |- Translate to Hindi
       |- Convert to Audio
   |
v
Return Analysis Data
   |
Display Tabs (Streamlit)
```

---

## Folder Structure

```
project-root/
├── backend/
│   ├── main.py
│   ├── .env
│   ├── requirements.txt
│   ├── Dockerfile
│   └── utils/
│       ├── news_fetcher.py
│       ├── data_handler.py
│       ├── summarization.py
│       ├── sentiment_analysis.py
│       ├── comparative_analysis_report.py
│       ├── hindi_translation.py
│       └── text_to_speech.py
│
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
└── docs/ <--- You are here
    └── project_docs.md (this file)
```

---

## API Endpoint

### `GET /full-analysis/{company}`

- **Input**: `company` (e.g., "Tesla")
- **Returns**:
  ```json
  {
    "news_data": [
      {
        "title": "Tesla shares jump 5%...",
        "summary": "Tesla saw a 5% surge...",
        "sentiment": "positive",
        "link": "https://...",
        "source": "Bloomberg",
        "published_date": "2024-04-01"
      },
      ...
    ],
    "comparative_summary": "Tesla had mostly positive news...",
    "translated_summary": "टेस्ला के बारे में ...",
    "audio_path": "/audio/hindi_summary.mp3"
  }
  ```

---

## Frontend (Streamlit Tabs)

1. **News Data** – Raw headlines with link, source, and date
2. **Summaries** – Expandable summaries for each article
3. **Sentiment Analysis** – DataFrame + Bar chart of article sentiments
4. **Comparative Report** – Dual language summary comparison
5. **Audio Summary** – Hindi TTS of the comparative report (with download option)

---

## Setup (Dev or Production)

### With Docker Compose

```bash
docker-compose up --build
```

### .env Format (backend/.env)

```env
newsapi=YOUR_NEWSAPI_KEY
GROQ_API_KEY=YOUR_GROQ_KEY
HF_TOKEN=YOUR_HUGGINGFACE_TOKEN
```

### Where to Get API Keys:
- 🔑 [NewsAPI Key](https://newsapi.org/register)
- 🔑 [Groq API Key](https://console.groq.com/keys)
- 🔑 [Hugging Face Access Token](https://huggingface.co/settings/tokens)

### Manually (Non-Docker)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

---

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Streamlit
- **LLM**: Groq LLaMA 3 8B Instant
- **NLP**: HuggingFace Transformers, FinBERT
- **TTS**: gTTS (Hindi)
- **Translation**: deep-translator
- **Deployment**: Docker + Docker Compose, Hugging Face Spaces

---

## To-Do / Future Enhancements

- Add support for multiple companies at once
- Enable chart-based trend analysis
- Let user select model (Groq, OpenAI, etc.)
- Save analysis history locally or in DB

---

## License

This project is for educational and non-commercial research use only.

---

## Contact

Made with ❤️ by Ramona

If you'd like to collaborate, report bugs, or extend this, feel free to reach out!

