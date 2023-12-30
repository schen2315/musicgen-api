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

MODELS = ['facebook/musicgen-small', 'facebook/musicgen-melody']

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default=MODELS[0])
    parser.add_argument('--text', type=str, default='modern upbeat eletronic lofi beats')
    parser.add_argument('--duration', type=int, default=10)
    parser.add_argument('--sample_rate', type=int, default=48000)
    parser.add_argument('--outfile_name', type=str, default='output')

    args = parser.parse_args()
    make_music(model=args.model,
               text=args.text,
               duration=args.duration,
               outfile_name=args.outfile_name,
               sample_rate=args.sample_rate)

