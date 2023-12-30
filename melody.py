from scipy.io.wavfile import write

import torch
import torchaudio
from audiocraft.models import MusicGen
from audiocraft.models import MultiBandDiffusion
from audiocraft.data.audio import audio_write

import argparse

USE_DIFFUSION_DECODER = True

if USE_DIFFUSION_DECODER:
    mbd = MultiBandDiffusion.get_mbd_musicgen()

MODELS = ['facebook/musicgen-melody', 'facebook/musicgen-small']

# model = MusicGen.get_pretrained('facebook/musicgen-melody')
# model.set_generation_params(duration=8)

# output = model.generate(
#     descriptions=[
#         'modern upbeat eletronic lofi beats'
#     ],
#     progress=True, return_tokens=True
# )
# if USE_DIFFUSION_DECODER:
#     out_diffusion = mbd.tokens_to_wav(output[1])
#     outputs = torch.cat([output[0], out_diffusion], dim=0)
#     outputs = outputs.detach().cpu().float()
#     for out in outputs:
#         i = 1
#         with open(f"./example-{i}.wav", "wb") as f:
#            audio_write(f"./example-{i}.wav", out, 32000, strategy="loudness",
#                 loudness_headroom_db=16, loudness_compressor=True, add_suffix=False)
#         i += 1

def make_music(model=MODELS[0], 
               text='modern upbeat eletronic lofi beats',
               duration=10,
               outfile_name='output',
               sample_rate=32000):
    model = MusicGen.get_pretrained(model)
    model.set_generation_params(duration=duration)

    output = model.generate(
        descriptions=[
            text
        ],
        progress=True, return_tokens=True
    )
    if USE_DIFFUSION_DECODER:
        out_diffusion = mbd.tokens_to_wav(output[1])
        outputs = torch.cat([output[0], out_diffusion], dim=0)
        outputs = outputs.detach().cpu().float()
        for out in outputs:
            i = 1
            with open(f"./{outfile_name}-{i}.wav", "wb") as f:
                audio_write(f"./{outfile_name}-{i}.wav", out, sample_rate, strategy="loudness",
                        loudness_headroom_db=16, loudness_compressor=True, add_suffix=False)
            i += 1

if __name__ == "__main__":
    make_music(model=MODELS[0],
               text='modern upbeat eletronic lofi beats',
               duration=10,
               outfile_name='output',
               sample_rate=48000)
