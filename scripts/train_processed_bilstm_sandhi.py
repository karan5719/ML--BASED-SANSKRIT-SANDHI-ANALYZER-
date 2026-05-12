
from __future__ import annotations

import argparse
import os
import sys
import unicodedata

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

from processed_data_loaders import load_sandhi_tsv_rows

import torch
from torch.utils.data import DataLoader

from bilstm_sandhi import BiLSTMSandhiSplitter, SandhiDataset, build_char_vocabulary, load_model, save_model
from train_bilstm_sandhi import evaluate_model, train_model


def load_cleaned_length_aligned(path: str) -> list[tuple[str, list[str]]]:
    out: list[tuple[str, list[str]]] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "=>" not in line:
                continue
            left, right = line.split("=>", 1)
            combined = unicodedata.normalize("NFC", left.strip())
            parts = [unicodedata.normalize("NFC", p.strip()) for p in right.split("+") if p.strip()]
            if " " in combined or not parts:
                continue
            if sum(len(p) for p in parts) != len(combined):
                continue
            out.append((combined, parts))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--lr", type=float, default=0.001)
    ap.add_argument("--patience", type=int, default=6)
    ap.add_argument("--max-len", type=int, default=50)
    ap.add_argument(
        "--out",
        default=os.path.join(PROJECT_ROOT, "models", "processed_data", "bilstm_sandhi_from_processed.pt"),
        help="Output checkpoint path",
    )
    ap.add_argument(
        "--supplement-cleaned",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Add length-aligned examples from data/sandhi_cleaned.txt to training only",
    )
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    train_rows = load_sandhi_tsv_rows(os.path.join(PROJECT_ROOT, "processed_data", "sandhi_train.tsv"))
    val_rows = load_sandhi_tsv_rows(os.path.join(PROJECT_ROOT, "processed_data", "sandhi_val.tsv"))
    test_rows = load_sandhi_tsv_rows(os.path.join(PROJECT_ROOT, "processed_data", "sandhi_test.tsv"))

    extra: list[tuple[str, list[str]]] = []
    if args.supplement_cleaned:
        cleaned_path = os.path.join(PROJECT_ROOT, "data", "sandhi_cleaned.txt")
        if os.path.isfile(cleaned_path):
            extra = load_cleaned_length_aligned(cleaned_path)

    train_data = list(train_rows) + list(extra)
    val_data = list(val_rows)
    test_data = list(test_rows)

    print(f"Train rows (processed aligned): {len(train_rows)}")
    print(f"Train supplement (cleaned aligned): {len(extra)}")
    print(f"Val rows: {len(val_data)}  Test rows: {len(test_data)}")

    if len(train_data) < 50:
        print("Too few training examples. Try --supplement-cleaned (default true) or check TSV paths.")
        sys.exit(1)

    char_to_idx = build_char_vocabulary(train_data + val_data + test_data)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}  vocab_size: {len(char_to_idx)}")

    train_loader = DataLoader(
        SandhiDataset(train_data, char_to_idx, max_len=args.max_len),
        batch_size=args.batch_size,
        shuffle=True,
    )
    val_loader = DataLoader(
        SandhiDataset(val_data, char_to_idx, max_len=args.max_len),
        batch_size=args.batch_size,
        shuffle=False,
    )

    model = BiLSTMSandhiSplitter(
        vocab_size=len(char_to_idx),
        embedding_dim=64,
        hidden_dim=128,
        num_layers=2,
        device=str(device),
    )
    model.to(device)
    model.char_to_idx = char_to_idx

    train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        num_epochs=args.epochs,
        device=str(device),
        learning_rate=args.lr,
        patience=args.patience,
        save_path=args.out,
        char_to_idx=char_to_idx,
    )

    best, _ = load_model(args.out, str(device))
    test_loader = DataLoader(
        SandhiDataset(test_data, char_to_idx, max_len=args.max_len),
        batch_size=args.batch_size,
        shuffle=False,
    )
    m = evaluate_model(best, test_loader, str(device), char_to_idx)
    print("=== held-out processed test (length-aligned) ===")
    print(m)
    print(f"Saved: {args.out}")


if __name__ == "__main__":
    main()
