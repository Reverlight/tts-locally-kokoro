#!/usr/bin/env python3
"""
QUICKSTART: 5 minutes to local high-quality TTS
Just copy this file and run: python quickstart.py
"""

from kokoro import KPipeline
import soundfile as sf
import os

# Create output folder
os.makedirs('audio_output', exist_ok=True)

# Initialize Kokoro (downloads model on first run ~500MB)
print("Loading Kokoro TTS model...")
pipeline = KPipeline(lang_code='a')  # 'a' = American English, 'b' = British
print("✅ Ready!")

# Your text here
text = """
Kokoro is a lightweight yet powerful text-to-speech model with just 82 million parameters.
Despite its small size, it delivers high quality audio comparable to much larger models.
It runs efficiently on both CPU and GPU, making it perfect for local applications.
"""

# Generate with different voices
voices = ['af_bella', 'af_sarah', 'am_michael']

for voice in voices:
    print(f"\n🎙️  Generating with {voice}...")
    samples, sample_rate = pipeline(text, voice=voice, speed=1.0)
    
    filename = f'audio_output/output_{voice}.wav'
    sf.write(filename, samples, sample_rate)
    print(f"✅ Saved: {filename}")

print("\n🎉 Done! Check audio_output/ folder for your audio files.")
