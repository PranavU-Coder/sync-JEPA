"""evaluate an Audio-JEPA checkpoint on ESC-50 via linear probe with kNN

usage:
    uv run python src/syncJEPA/eval.py \\
        --checkpoint runs/baseline/final.pt \\
        --esc50_root ./data/esc50
"""

import argparse
import csv
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import numpy as np
import torch
import torch.nn.functional as F
import torchaudio
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from ajepa import AudioJEPA
from prep import compute_mel_params


def load_checkpoint(ckpt_path, device):
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    cfg = ckpt["config"]
    model = AudioJEPA.from_config(cfg).to(device)
    model.load_state_dict(ckpt["model"])
    model.eval()
    step = ckpt.get("step", "?")
    return model, cfg, step


@torch.no_grad()
def extract_features(model, cfg, esc50_root, device):
    """return (features, labels, folds) numpy arrays."""
    sr = cfg["data"]["sample_rate"]
    n_mels = cfg["data"]["n_mels"]
    n_frames = cfg["data"]["n_time_bins"]
    n_fft, hop = compute_mel_params(cfg)

    mel_xform = torchaudio.transforms.MelSpectrogram(
        sample_rate=sr,
        n_fft=n_fft,
        hop_length=hop,
        n_mels=n_mels,
        f_min=50,
        f_max=sr // 2,
        power=2.0,
    ).to(device)

    meta = []
    with open(Path(esc50_root) / "meta" / "esc50.csv") as f:
        for row in csv.DictReader(f):
            meta.append((row["filename"], int(row["target"]), int(row["fold"])))

    audio_dir = Path(esc50_root) / "audio"
    encoder = model.target_encoder  # frozen EMA encoder, per AJEPA convention

    features, labels, folds = [], [], []
    for fname, target, fold in tqdm(meta, desc="extract", dynamic_ncols=True):
        wav, file_sr = torchaudio.load(str(audio_dir / fname))
        if wav.shape[0] > 1:
            wav = wav.mean(dim=0, keepdim=True)
        if file_sr != sr:
            wav = torchaudio.functional.resample(wav, file_sr, sr)
        wav = wav.to(device)

        mel = mel_xform(wav)
        log_mel = torch.log(mel + 1e-6).squeeze(0)  # (n_mels, T)

        # pad or center-crop to n_frames
        _, T = log_mel.shape
        if T >= n_frames:
            s = (T - n_frames) // 2
            log_mel = log_mel[:, s : s + n_frames]
        else:
            log_mel = F.pad(log_mel, (0, n_frames - T), value=float(log_mel.min()))

        log_mel = (log_mel - log_mel.mean()) / (log_mel.std() + 1e-6)

        x = log_mel.unsqueeze(0).unsqueeze(0)  # (1, 1, n_mels, n_frames)
        emb = encoder(x)  # (1, n_patches, D)
        pooled = emb.mean(dim=1).squeeze(0)  # (D,)

        features.append(pooled.float().cpu().numpy())
        labels.append(target)
        folds.append(fold)

    return np.array(features), np.array(labels), np.array(folds)


def evaluate(features, labels, folds):
    lin_accs, knn_accs = [], []
    for test_fold in range(1, 6):
        tr = folds != test_fold
        te = folds == test_fold
        X_tr, X_te = features[tr], features[te]
        y_tr, y_te = labels[tr], labels[te]

        # standardize features
        scaler = StandardScaler()
        X_tr_s = scaler.fit_transform(X_tr)
        X_te_s = scaler.transform(X_te)

        lin = LogisticRegression(max_iter=2000, C=1.0, n_jobs=-1)
        lin.fit(X_tr_s, y_tr)
        lin_acc = accuracy_score(y_te, lin.predict(X_te_s))

        knn = KNeighborsClassifier(n_neighbors=5, n_jobs=-1)
        knn.fit(X_tr_s, y_tr)
        knn_acc = accuracy_score(y_te, knn.predict(X_te_s))

        lin_accs.append(lin_acc)
        knn_accs.append(knn_acc)
        print(
            f"  fold {test_fold}: linear {lin_acc * 100:5.2f}%   kNN {knn_acc * 100:5.2f}%"
        )

    return np.array(lin_accs), np.array(knn_accs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--esc50_root", required=True)
    parser.add_argument(
        "--device", default="cuda" if torch.cuda.is_available() else "cpu"
    )
    args = parser.parse_args()

    device = torch.device(args.device)

    t0 = time.time()
    print(f"checkpoint: {args.checkpoint}")
    model, cfg, step = load_checkpoint(args.checkpoint, device)
    print(
        f"  trained for {step} steps, encoder dim {cfg['model']['embed_dim']}, "
        f"patches {model.n_patches}"
    )

    print("extracting features on ESC-50...")
    feats, labs, folds = extract_features(model, cfg, args.esc50_root, device)
    print(f"features: {feats.shape}  labels: {labs.shape}")

    print("5-fold CV:")
    lin, knn = evaluate(feats, labs, folds)

    print()
    print(f"Linear probe  : {lin.mean() * 100:.2f}  +/- {lin.std() * 100:.2f}")
    print(f"kNN (k=5)     : {knn.mean() * 100:.2f}  +/- {knn.std() * 100:.2f}")
    print(f"Total time    : {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
