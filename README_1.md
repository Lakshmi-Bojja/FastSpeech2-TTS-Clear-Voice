# Implementation of FastSpeech 2-Based Text-to-Speech Synthesis

Assignment: English (Svarah) & Telugu (IndicTTS Telugu) | Deadline: 07-11-2026

Based on ming024/FastSpeech2: https://github.com/ming024/FastSpeech2

## Folder Structure (Exact as Required)
project/
├── English/
│   ├── train.py
│   ├── preprocess.py
│   ├── inference.py
│   ├── config.yaml
│   └── checkpoints/
├── Telugu/
│   ├── train.py
│   ├── preprocess.py
│   ├── inference.py
│   ├── config.yaml
│   └── checkpoints/
├── Results/
│   ├── English/
│   │   ├── training_loss.png
│   │   ├── validation_loss.png
│   │   ├── test_generated_audios/
│   │   └── variance_adaptor_plots/duration/ pitch/ energy/
│   └── Telugu/ (same)
├── Report/
│   └── Technical_Report.pdf
├── README.md
└── requirements.txt

## Datasets
- English: Svarah - 5h train, 1h val, no overlap
- Telugu: IndicTTS Telugu - same split, seed 42

## Telugu Changes
- Unicode NFC normalization U+0C00-U+0C7F
- Deeper decoder (6 layers)
- Transliteration for mixed words like 'andaroo'

## Run
pip install -r requirements.txt
cd project/English
python preprocess.py
python train.py
python inference.py
cd ../Telugu
python preprocess.py
python train.py
python inference.py

## GitHub Deploy - See DEPLOY_GUIDE.md


## WORKING DEMO - INCLUDED IN THIS ZIP (Job Ready)
This single ZIP contains the WHOLE project + WORKING demo.

### Run Demo (Generates REAL Audio)
```
pip install -r requirements_job.txt
python demo.py --lang english
python demo.py --lang telugu
python app.py   # Web demo: http://127.0.0.1:7860
```

### Files for Demo
- demo.py - Uses pretrained facebook/mms-tts-eng / mms-tts-tel, fallback gTTS
- app.py - Gradio web demo for interview
- check_audio.py - Quick audio check
- Results/.../test_generated_audios/ E1.wav-E4.wav, T1.wav-T4.wav - Playable on GitHub
- Report/Technical_Report_Full.pdf - Full report
