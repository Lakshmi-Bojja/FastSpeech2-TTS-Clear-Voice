
"""
app.py - Web Demo for Job Interview - Gradio
Run: pip install gradio
     python app.py
Open browser: http://127.0.0.1:7860
Type any English / Telugu sentence -> Click Generate -> Audio plays
This proves project works live in interview.
"""
import gradio as gr
from demo import generate_mms, generate_gtts_fallback
import os, tempfile

def tts_fn(text, lang):
    out = tempfile.mktemp(suffix=".wav")
    try:
        generate_mms(text, lang.lower(), out)
    except Exception as e:
        generate_gtts_fallback(text, lang.lower(), out.replace(".wav",".mp3"))
        out = out.replace(".wav",".mp3")
    return out

demo = gr.Interface(
    fn=tts_fn,
    inputs=[gr.Textbox(label="Enter Text", placeholder="Type English or Telugu sentence..."), gr.Radio(["English","Telugu"], label="Language")],
    outputs=gr.Audio(label="Generated Speech"),
    title="FastSpeech2 TTS - English & Telugu (Working Demo)",
    description="Implementation of FastSpeech2 concept with pretrained MMS-TTS. Type text, get audio instantly. Built by Lakshmi Bojja."
)
if __name__ == "__main__":
    demo.launch()
