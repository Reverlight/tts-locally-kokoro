from kokoro import KPipeline
import soundfile as sf
import os
from datetime import datetime
import numpy as np

pipeline = KPipeline(lang_code='a')

text = """
Breaking news from the world of technology. Researchers have developed a new AI model 
that can predict traffic patterns with 94% accuracy. The system uses real-time data 
from thousands of sensors placed across major cities. City officials say this could 
reduce commute times by up to 30 percent. The technology is expected to roll out 
in pilot cities by the end of next year.
"""


# 🇺🇸 👩	af_alloy, af_aoede, af_bella, af_heart, af_jessica, af_kore, af_nicole, af_nova, af_river, af_sarah, af_sky	en-us
# 🇺🇸 👨	am_adam, am_echo, am_eric, am_fenrir, am_liam, am_michael, am_onyx, am_puck	en-us
# 🇬🇧	bf_alice, bf_emma, bf_isabella, bf_lily, bm_daniel, bm_fable, bm_george, bm_lewis	en-gb
# 🇫🇷	ff_siwis	fr-fr
# 🇮🇹	if_sara, im_nicola	it
# 🇯🇵	jf_alpha, jf_gongitsune, jf_nezumi, jf_tebukuro, jm_kumo	ja
# 🇨🇳	zf_xiaobei, zf_xiaoni, zf_xiaoxiao, zf_xiaoyi, zm_yunjian, zm_yunxi, zm_yunxia, zm_yunyang	cmn


# good so far bm_daniel, bm_lewis, am_michael

# best so far

# am_puck


os.makedirs("outputs", exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

chunks = []
generator = pipeline(text, voice="am_puck")

for i, (gs, ps, audio) in enumerate(generator):
    filename = f"outputs/{timestamp}_{choice}_{i}.wav"
    print(f"Saved: {filename}")
    chunks.append(audio)

combined = np.concatenate(chunks)
combined_filename = f"outputs/{timestamp}_{choice}_combined.wav"
sf.write(combined_filename, combined, 24000)
print(f"Saved combined: {combined_filename}")