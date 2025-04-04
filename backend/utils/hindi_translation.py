from deep_translator import GoogleTranslator


class Translator:
    def __init__(self, source_lang="en", target_lang="hi"):
        """Initialize the Google Translator."""
        self.translator = GoogleTranslator(source=source_lang, target=target_lang)

    def translate_text(self, text):
        """Translate the given text."""
        return self.translator.translate(text)
