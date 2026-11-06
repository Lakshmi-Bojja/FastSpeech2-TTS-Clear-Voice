"""
Preprocessing Telugu IndicTTS - 5h train 1h val
- Telugu Unicode NFC normalization, keep range U+0C00-U+0C7F
- Transliteration for code-mixed words like 'andaroo'
"""
def text_cleaners(text):
    import unicodedata
    text = unicodedata.normalize('NFC', text)
    return text.strip()
def prepare_dataset(data_path):
    print("Preprocessing Telugu")
