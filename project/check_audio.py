
# Quick check: python check_audio.py
# Creates test_output.wav - if file created and plays, audio pipeline works
import numpy as np, wave
sr=22050
t=np.linspace(0,2,sr*2)
y=(0.5*np.sin(2*np.pi*440*t)*32767).astype(np.int16)
with wave.open("test_output.wav","wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
    wf.writeframes(y.tobytes())
print("SUCCESS: test_output.wav created")
