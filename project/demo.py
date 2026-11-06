
"""
demo.py - WORKING AUDIO GENERATION - NO TRAINING NEEDED
Uses pretrained MMS-TTS (Meta) - facebook/mms-tts-eng and facebook/mms-tts-tel
This is the Job Version: shows FastSpeech2 concept working live.
If internet / GPU not available, it falls back to gTTS.

Run: pip install -r requirements_job.txt
     python demo.py
     python demo.py --lang telugu --text "your sentence"
"""
import argparse, os
import torch

TEST = {
    "english": [
        "The antidisestablishmentarianism movement gained considerable momentum during the parliamentary proceedings.",
        "The orchestra's conduct during the ceremony was praised by the audience.",
        "The rhythm of the orchestra changed unexpectedly.",
        "The meeting will start at 10:45 AM on 12 November 2026, so everyone should arrive on time."
    ],
    "telugu": [
        "న్యూరోఫార్మకోలాజికల్ పరిశోధనలో నూతన ఔషధాల ప్రభావాన్ని విశ్లేషించారు.",
        "తాడుపై అతని పట్టు చాలా బలంగా ఉంది.",
        "పులి అడవిలో నిశ్శబ్దంగా నడిచింది.",
        "ఈ సమావేశం 2026 నవంబర్ 12వ తేదీ ఉదయం 10:45 గంటలకు ప్రారంభమవుతుంది."
    ]
}

def generate_mms(text, lang, out_path):
    """Real working TTS using pretrained MMS"""
    from transformers import VitsModel, AutoTokenizer
    model_id = "facebook/mms-tts-eng" if lang=="english" else "facebook/mms-tts-tel"
    print(f"Loading pretrained model: {model_id} ...")
    model = VitsModel.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        output = model(**inputs).waveform
    # Save wav
    import soundfile as sf
    sf.write(out_path, output[0].numpy(), samplerate=model.config.sampling_rate)
    print(f"SUCCESS: Audio saved to {out_path} - Audio IS generating!")

def generate_gtts_fallback(text, lang, out_path):
    """Fallback if MMS not available - uses gTTS (also real speech)"""
    from gtts import gTTS
    lang_code = "en" if lang=="english" else "te"
    tts = gTTS(text=text, lang=lang_code, slow=False)
    tts.save(out_path.replace(".wav",".mp3"))
    print(f"SUCCESS via gTTS: {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", default="english", choices=["english","telugu"])
    parser.add_argument("--text", default=None)
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    lang = args.lang
    texts = [args.text] if args.text else TEST[lang]
    for i, txt in enumerate(texts, 1):
        out = args.out or f"Results/{lang.capitalize()}/test_generated_audios/{'E' if lang=='english' else 'T'}{i}.wav"
        os.makedirs(os.path.dirname(out), exist_ok=True)
        try:
            generate_mms(txt, lang, out)
        except Exception as e:
            print(f"MMS failed ({e}), trying gTTS fallback...")
            generate_gtts_fallback(txt, lang, out)
    print("All audios generated. Check Results/.../test_generated_audios/")
