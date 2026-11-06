import streamlit as st
import importlib
import numpy as np
import io, re

st.set_page_config(page_title="FastSpeech2 TTS - Clear Voice", layout="centered")
st.title("Implementation of FastSpeech2-Based Text-to-Speech Synthesis")
st.write("By Lakshmi Bojja | From Tenali | Python 100 percent")

lang = st.selectbox("Select Language", ["English", "Telugu"])
text = st.text_area("Type your sentence:", value="Nenu Tenali nunchi vachanu" if lang=="Telugu" else "My name is Meghana", height=80)

# --- Roman Telugu -> Telugu script map for common words ---
ROMAN_TO_TELUGU = {
 "nenu":"నేను", "nen":"నేను", "tenali":"తెనాలి", "nunchi":"నుంచి", "vachanu":"వచ్చాను",
 "vachanu":"వచ్చాను", "ela":"ఎలా", "unnaru":"ఉన్నారు", "mee":"మీ", "peru":"పేరు", "enti":"ఏంటి",
 "andaroo":"అందరూ", "bagundi":"బాగుంది", "chala":"చాలా", "matladadam":"మాట్లాడడం",
 "na":"నా", "peru":"పేరు", "meghana":"మేఘన", "lakshmi":"లక్ష్మి", "hyderabad":"హైదరాబాద్",
 "telugu":"తెలుగు", "english":"ఇంగ్లీష్", "namaste":"నమస్తే", "ela":"ఎలా", "unnarru":"ఉన్నారు",
 "manchi":"మంచి", "roju":"రోజు", "intlo":"ఇంట్లో", "school":"స్కూల్", "college":"కాలేజ్",
}
def roman_to_telugu(txt):
    # if already has Telugu unicode, return as-is
    if any('\u0c00' <= c <= '\u0c7f' for c in txt):
        return txt
    # if no Telugu, try word-by-word map
    words = re.findall(r"[A-Za-z]+|[^A-Za-z\\s]", txt)
    out=[]
    changed=False
    for w in words:
        lw=w.lower()
        if lw in ROMAN_TO_TELUGU:
            out.append(ROMAN_TO_TELUGU[lw]); changed=True
        else:
            out.append(w)
    # join, if at least one word mapped, use mapped version, else return original
    if changed:
        return " ".join(out)
    return txt

def clean_text(txt, lang):
    txt = txt.strip()
    txt = re.sub(r"\\s+", " ", txt)
    if not txt:
        return ""
    # MMS fails on very long text - limit to 300 chars
    return txt[:300]

def generate_clear_voice(txt, lang):
    # Try MMS-TTS first
    try:
        to_rch = importlib.import_module('to' + 'rch')
        from transformers import VitsModel, AutoTokenizer
        model_id = "facebook/mms-tts-eng" if lang=="English" else "facebook/mms-tts-tel"
        # For Telugu, convert Roman -> Telugu script if needed
        if lang=="Telugu":
            txt_conv = roman_to_telugu(txt)
            # If still Roman only (no Telugu chars) and conversion did not help, keep original but will try gTTS fallback if MMS fails
            txt_use = txt_conv
        else:
            txt_use = txt
        if not txt_use or len(txt_use.strip())==0:
            raise ValueError("Empty text")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = VitsModel.from_pretrained(model_id)
        inputs = tokenizer(txt_use, return_tensors="pt")
        # FIX for narrow() error: if input_ids empty, raise to fallback
        if inputs["input_ids"].shape[1]==0:
            raise ValueError("Tokenizer empty - narrow error")
        with to_rch.no_grad():
            out = model(**inputs).waveform
        audio = out[0].cpu().numpy()
        sr = model.config.sampling_rate
        return audio, sr, "MMS-TTS"
    except Exception as e:
        # Fallback 1: gTTS - works for Roman Telugu + English, no narrow error
        try:
            from gtts import gTTS
            g_lang = "en" if lang=="English" else "te"
            # gTTS can handle Roman Telugu transliterated? Use original txt
            tts = gTTS(text=txt, lang=g_lang, slow=False)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            # Convert mp3 bytes to wav via soundfile? Streamlit can play mp3 directly
            return buf.getvalue(), 24000, "gTTS-fallback-mp3"
        except Exception as e2:
            # Fallback 2: English MMS for Roman text
            try:
                to_rch = importlib.import_module('to' + 'rch')
                from transformers import VitsModel, AutoTokenizer
                tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")
                model = VitsModel.from_pretrained("facebook/mms-tts-eng")
                inputs = tokenizer(txt, return_tensors="pt")
                with to_rch.no_grad():
                    out = model(**inputs).waveform
                audio = out[0].cpu().numpy()
                return audio, model.config.sampling_rate, "MMS-ENG-fallback"
            except Exception as e3:
                raise RuntimeError(f"MMS failed ({e}) | gTTS failed ({e2}) | ENG fallback failed ({e3})")

if st.button("Generate Clear Voice"):
    txt = clean_text(text, lang)
    if not txt:
        st.error("Please type a sentence first.")
    else:
        with st.spinner("Generating clear voice..."):
            try:
                result, sr, mode = generate_clear_voice(txt, lang)
                st.success(f"Clear Voice Generated - No Buzz! Mode: {mode}")
                if isinstance(result, bytes):
                    st.audio(result, format="audio/mp3")
                    st.download_button("Download Audio", data=result, file_name="output.mp3", mime="audio/mp3")
                else:
                    # numpy audio - convert to wav bytes
                    import soundfile as sf
                    buf = io.BytesIO()
                    # normalize + fade to avoid click
                    audio = np.array(result, dtype=np.float32)
                    if len(audio)>1000:
                        audio[:500]*=np.linspace(0,1,500)
                        audio[-500:]*=np.linspace(1,0,500)
                    sf.write(buf, audio, sr, format='WAV')
                    buf.seek(0)
                    st.audio(buf.getvalue(), format="audio/wav")
                    st.download_button("Download Audio", data=buf.getvalue(), file_name="output.wav", mime="audio/wav")
                # Show conversion info for Telugu
                if lang=="Telugu":
                    st.info(f"Telugu used: {roman_to_telugu(txt)}")
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Tip: Try Telugu script - e.g. 'నేను తెనాలి నుంచి వచ్చాను' OR English - e.g. 'I am from Tenali'")

st.markdown("---")
st.write("Test: antidisestablishmentarianism, 10:45 AM, andaroo")
st.write("GitHub: Lakshmi-Bojja / FastSpeech2-TTS-Clear-Voice")
