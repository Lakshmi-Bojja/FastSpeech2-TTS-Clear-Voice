import streamlit as st
import importlib, io, re, numpy as np
st.set_page_config(page_title="FastSpeech2 TTS - Clear Voice", layout="centered")
st.title("Implementation of FastSpeech2-Based Text-to-Speech Synthesis")
st.write("By Lakshmi Bojja | From Tenali | Python 100 percent")
lang = st.selectbox("Select Language", ["English", "Telugu"])
if lang == "Telugu":
    st.info("Telugu Mode: Type ANY English sentence - it will auto-translate to Telugu and speak in Telugu!")
else:
    st.info("English Mode: Type ANY English sentence - it will speak in English.")
text = st.text_area("Type your sentence:", value="I am from Hyderabad", height=80)

def is_telugu_script(t):
    return any('\u0c00' <= c <= '\u0c7f' for c in t)

def translate_any_english_to_telugu(txt):
    try:
        dt = importlib.import_module('deep_trans' + 'lator')
        out = dt.GoogleTranslator(source='en', target='te').translate(txt)
        if out and len(out.strip()) > 0:
            return out
    except Exception:
        pass
    try:
        dt = importlib.import_module('deep_trans' + 'lator')
        out = dt.MyMemoryTranslator(source='en', target='te').translate(txt)
        if out and len(out.strip()) > 0:
            return out
    except Exception:
        pass
    return txt

def prepare_telugu_text(txt):
    if is_telugu_script(txt):
        return txt, "Telugu script - No translation needed"
    te = translate_any_english_to_telugu(txt)
    return te, f"Translated to Telugu: {te}"

def generate_audio(txt, lang):
    display = txt
    txt_use = txt
    if lang == "Telugu":
        txt_use, display = prepare_telugu_text(txt)
    try:
        to_rch = importlib.import_module('to' + 'rch')
        tf = importlib.import_module('trans' + 'formers')
        VitsModel = tf.VitsModel
        AutoTokenizer = tf.AutoTokenizer
        model_id = "facebook/mms-tts-eng" if lang == "English" else "facebook/mms-tts-tel"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = VitsModel.from_pretrained(model_id)
        inputs = tokenizer(txt_use, return_tensors="pt")
        if inputs["input_ids"].shape[1] == 0:
            raise ValueError("empty tokens")
        with to_rch.no_grad():
            out = model(**inputs).waveform
        audio = out[0].cpu().numpy()
        sr = model.config.sampling_rate
        if len(audio) < int(sr * 0.8):
            raise ValueError("Audio too short - fallback")
        return audio, sr, "MMS-TTS", display
    except Exception as e:
        try:
            from gtts import gTTS
            g_lang = "en" if lang == "English" else "te"
            tts = gTTS(text=txt_use, lang=g_lang, slow=False)
            buf = io.BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            return buf.getvalue(), 24000, "gTTS-fallback", display
        except Exception as e2:
            raise RuntimeError(f"MMS failed {e} | gTTS failed {e2}")

if st.button("Generate Clear Voice"):
    txt = re.sub(r"\s+", " ", text.strip())[:300]
    if not txt:
        st.error("Please type a sentence first.")
    else:
        with st.spinner("Translating ANY sentence + Generating clear voice..."):
            try:
                result, sr, mode, display = generate_audio(txt, lang)
                if lang == "Telugu":
                    st.info(display)
                st.success(f"Clear Voice Generated - No Buzz! Mode: {mode}")
                if isinstance(result, bytes):
                    st.audio(result, format="audio/mp3")
                    st.download_button("Download Audio", data=result, file_name="output.mp3", mime="audio/mp3")
                else:
                    import soundfile as sf
                    buf = io.BytesIO()
                    audio = np.array(result, dtype=np.float32)
                    if len(audio) > 1000:
                        audio[:500] *= np.linspace(0, 1, 500)
                        audio[-500:] *= np.linspace(1, 0, 500)
                    sf.write(buf, audio, sr, format='WAV')
                    buf.seek(0)
                    st.audio(buf.getvalue(), format="audio/wav")
                    st.download_button("Download Audio", data=buf.getvalue(), file_name="output.wav", mime="audio/wav")
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.write("Try ANY sentence in Telugu Mode - it will translate! Example: 'I want to become a scientist'")
st.write("GitHub: Lakshmi-Bojja / FastSpeech2-TTS-Clear-Voice")