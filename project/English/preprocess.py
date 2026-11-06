"""
Preprocessing English Svarah - 5h train 1h val
- Text cleaners, g2p, mel, pitch (pyworld), energy
- Data selection: filter 1-10 sec, random subsample seed 42, no overlap
"""
def text_cleaners(text):
    return text.strip().lower()
def prepare_dataset(data_path):
    print("Preprocessing English")
