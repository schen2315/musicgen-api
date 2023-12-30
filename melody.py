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

model = MusicGen.get_pretrained('facebook/musicgen-melody')
# model = MusicGen.get_pretrained('facebook/musicgen-small')
model.set_generation_params(duration=8)

output = model.generate(
    descriptions=[
        'modern eletronic lofi beats'
    ],
    progress=True, return_tokens=True
)
if USE_DIFFUSION_DECODER:
    out_diffusion = mbd.tokens_to_wav(output[1])
    outputs = torch.cat([output[0], out_diffusion], dim=0)
    outputs = outputs.detach().cpu().float()
    for out in outputs:
        i = 1
        with open(f"./example-{i}.wav", "wb") as f:
           audio_write(f"./example-{i}.wav", out, 32000, strategy="loudness",
                loudness_headroom_db=16, loudness_compressor=True, add_suffix=False)
        i += 1
