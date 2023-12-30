from scipy.io.wavfile import write

import torch
from audiocraft.models import MusicGen
from audiocraft.models import MultiBandDiffusion
from audiocraft.data.audio import audio_write

USE_DIFFUSION_DECODER = True

if USE_DIFFUSION_DECODER:
    mbd = MultiBandDiffusion.get_mbd_musicgen()

import torchaudio
from audiocraft.utils.notebook import display_audio

# model = MusicGen.get_pretrained('facebook/musicgen-melody')
model = MusicGen.get_pretrained('facebook/musicgen-small')
model.set_generation_params(duration=8)

# melody_waveform, sr = torchaudio.load("../assets/bach.mp3")
# melody_waveform = melody_waveform.unsqueeze(0).repeat(2, 1, 1)
output = model.generate(
    descriptions=[
        'lofi hip hop beat with a chill vibe'
    ],
    # melody_wavs=melody_waveform,
    # melody_sample_rate=8000,
    progress=True, return_tokens=True
)
# display_audio(output[0], sample_rate=8000)
if USE_DIFFUSION_DECODER:
    out_diffusion = mbd.tokens_to_wav(output[1])
    # write("example.wav", 32000, out_diffusion)
    # display_audio(out_diffusion, sample_rate=8000)
    outputs = torch.cat([output[0], out_diffusion], dim=0)
    outputs = outputs.detach().cpu().float()
    for out in outputs:
        i = 1
        with open(f"./example-{i}.wav", "wb") as f:
           audio_write(f"./example-{i}.wav", out, 32000, strategy="loudness",
                loudness_headroom_db=16, loudness_compressor=True, add_suffix=False)
        i += 1
