import uuid
from gtts import gTTS
import os


class TextToSpeech:
    def __init__(self, language="hi"):
        self.language = language

    def text_to_speech(self, text):
        """Convert text to speech and save as a unique audio file."""
        unique_filename = f"summary_{uuid.uuid4().hex}.mp3"
        output_path = os.path.join(
            "audio_files", unique_filename
        )  # Store in 'audio_files' directory

        os.makedirs("audio_files", exist_ok=True)  # Ensure directory exists
        tts = gTTS(text=text, lang=self.language)
        tts.save(output_path)

        print(f"Audio saved as {output_path}")
        return output_path  # Return path of generated file
