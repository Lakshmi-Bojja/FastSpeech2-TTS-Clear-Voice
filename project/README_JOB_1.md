
# FastSpeech2 TTS - English & Telugu - JOB READY VERSION
## This version WORKS - Generates REAL Audio

### How to Run (Working Code)
```
pip install -r requirements_job.txt
python demo.py --lang english
python demo.py --lang telugu
python app.py  # Opens web demo http://127.0.0.1:7860
```

### What is in this ZIP (Pending Items Completed)
- demo.py - WORKING - Uses pretrained facebook/mms-tts-eng / tel, fallback gTTS
- app.py - WORKING - Gradio web demo for interview
- check_audio.py - Quick audio pipeline check
- Results/.../test_generated_audios/ E1.wav-E4.wav, T1.wav-T4.wav - REAL wav files to play on GitHub
- Report/Technical_Report_Full.pdf - Full 14-section report
- requirements_job.txt

### How to Upload to GitHub
Extract ZIP -> Copy demo.py, app.py, check_audio.py, requirements_job.txt into your repo root
Copy Results/.../*.wav into Results/.../test_generated_audios/
Copy Report/Technical_Report_Full.pdf into Report/
Commit changes - Done!
