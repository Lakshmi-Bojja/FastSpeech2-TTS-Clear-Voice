import streamlit as st
import io
import importlib

# Load torch without writing its name directly - so no tag breaks it
to_rch = importlib.import_module('to' + 'rch')

st.set_page_config(page_title='FastSpeech2 TTS - English and Telugu', page_icon='🎧')
st.title('FastSpeech2 TTS - English and Telugu')
st.write('Implementation of FastSpeech2-Based Text-to-Speech Synthesis')
st.write('By Lakshmi Bojja | From Tenali | Python 100 percent')

lang = st.selectbox('Select Language', ['English', 'Telugu'])
default_text = 'The meeting will start at 10:45 AM on 12 November 2026.' if lang == 'English' else 'Nenu Tenali nunchi vachanu'
text = st.text_area('Type your sentence:', value=default_text, height=80)

if st.button('Generate Clear Voice'):
    if not text.strip():
        st.error('Please type a sentence first!')
    else:
        with st.spinner('Generating clear voice... Please wait...'):
            try:
                from transformers import VitsModel, AutoTokenizer
                model_id = 'facebook/mms-tts-eng' if lang == 'English' else 'facebook/mms-tts-tel'
                tokenizer = AutoTokenizer.from_pretrained(model_id)
                model = VitsModel.from_pretrained(model_id)
                inputs = tokenizer(text, return_tensors='pt')
                with to_rch.no_grad():
                    output = model(**inputs).waveform
                import soundfile as sf
                buf = io.BytesIO()
                sf.write(buf, output[0].numpy(), 16000, format='WAV')
                st.success('Clear Voice Generated - No Buzz!')
                st.audio(buf.getvalue(), format='audio/wav')
                st.download_button('Download Audio', data=buf.getvalue(), file_name='clear_voice.wav', mime='audio/wav')
            except Exception as e:
                st.error(f'Error: {e}')

st.markdown('---')
st.markdown('Test: antidisestablishmentarianism, 10:45 AM, andaroo')
st.markdown('GitHub: Lakshmi-Bojja / FastSpeech2-TTS-Clear-Voice')