# nanoGPT — Training a Language Model From Scratch

A character-level GPT trained using Andrej Karpathy's
[nanoGPT](https://github.com/karpathy/nanoGPT), first on a sample Shakespeare
dataset to validate the pipeline, then on my own cleaned Twitter dataset
(from the [data cleaning assignment](https://github.com/PKrithika/hw2_data_cleaning)).
Includes a small Flask web app to generate text from either trained model.

## What it does

1. **`prepare.py`** — tokenizes raw text into character-level tokens (`train.bin`, `val.bin`, `meta.pkl`)
2. **`train.py`** — trains a small GPT model on those tokens, tracking loss over time
3. **`sample.py`** — loads a trained checkpoint and generates new text
4. **`app.py`** + **`index.html`** — a Flask web UI to generate text from either
   trained model in the browser, instead of the terminal

## Folder structure
nanoGPT/
├── data/
│ ├── shakespeare_char/ # sample dataset (provided)
│ └── twitter_char/ # my own dataset, from HW2's cleaned output
├── config/
│ ├── train_shakespeare_char.py
│ └── train_twitter_char.py
├── out-shakespeare-char/ # trained Shakespeare model checkpoint
├── out-twitter-char/ # trained Twitter model checkpoint
├── app.py # Flask backend
├── index.html # frontend UI
├── train.py / sample.py / prepare.py # (from nanoGPT)
└── README.md


## How to run

```bash
uv add torch numpy transformers datasets tiktoken wandb tqdm requests flask

# Tokenize a dataset
python data/twitter_char/prepare.py

# Train
python train.py config/train_twitter_char.py --device=cpu --compile=False \
  --eval_iters=20 --log_interval=1 --block_size=64 --batch_size=12 \
  --n_layer=4 --n_head=4 --n_embd=128 --max_iters=2000 --lr_decay_iters=2000 --dropout=0.0

# Generate text from the terminal
python sample.py --out_dir=out-twitter-char --device=cpu

# Or launch the web UI
python app.py   # then open http://127.0.0.1:5000
```

## Experiments & findings

| Experiment | Val loss |
|---|---|
| 4 layers, 2000 iterations | 1.89 |
| 4 layers, 4000 iterations | 1.70 (better) |
| 6 layers, 2000 iterations | 1.92 (worse) |

**More training helped** — doubling iterations from 2000 to 4000 (same model
size) improved validation loss noticeably.

**More layers alone did not help** — increasing from 4 to 6 layers while
keeping training time fixed made results slightly worse. A larger model has
more parameters to learn and needs proportionally more training time to
benefit from that extra capacity; it doesn't automatically outperform a
smaller model trained for the same number of steps.

## Sample output

**Shakespeare model** — picks up dialogue formatting and old English phrasing:
LADO:
You beand our king upor teept more put thein;
You do mile spord of unfent all of death lied,


**Twitter model** — same architecture, distinctly different tone:
i'll becazy, thangs a no need mire pontory can shairs of of 10 the to add
othe her the seasshil ave otheree are schouse backen't better to u was i
momes so on my be to i can in who wreeered don't a lmid lol

Both outputs use invented/garbled words (expected for a small character-level
model trained briefly on CPU), but each clearly reflects the style of its
training data — formal dialogue structure vs. casual, lowercase, internet-speak.
