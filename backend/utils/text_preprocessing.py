import re


class SentenceChunker:
    def __init__(self, max_sentences=30, overlap=2):
        self.max_sentences = max_sentences
        self.overlap = overlap

    def preprocess(self, text):
        sentences = re.split(r"(?<=[.!?])\s+", text)
        chunks = []

        start = 0
        while start < len(sentences):
            end = min(start + self.max_sentences, len(sentences))
            chunk = " ".join(sentences[start:end])
            chunks.append(chunk)
            start += self.max_sentences - self.overlap

        print(f"Number of chunks: {len(chunks)}")
        return chunks
