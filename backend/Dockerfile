# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download necessary NLTK resources
RUN mkdir -p /app/nltk_data && \
    python -m nltk.downloader -d /app/nltk_data punkt stopwords punkt_tab && \
    ls -la /app/nltk_data/tokenizers/punkt_tab


# Tell NLTK where to find the downloaded data
ENV NLTK_DATA="/app/nltk_data"

# Copy all project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
