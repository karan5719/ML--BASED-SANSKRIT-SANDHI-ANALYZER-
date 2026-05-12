
from __future__ import annotations

import argparse
import os
import pickle
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from processed_data_loaders import train_crf_style_pickled_model, load_pos_tsv_sentences
from crf_pos_tagger import CRFPOSTagger


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        default=os.path.join(PROJECT_ROOT, "models", "processed_data", "crf_pos_from_processed.pkl"),
    )
    ap.add_argument("--alpha", type=float, default=0.1, help="Laplace smoothing for counts")
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    train = load_pos_tsv_sentences(os.path.join(PROJECT_ROOT, "processed_data", "pos_train.tsv"))
    val = load_pos_tsv_sentences(os.path.join(PROJECT_ROOT, "processed_data", "pos_val.tsv"))
    test = load_pos_tsv_sentences(os.path.join(PROJECT_ROOT, "processed_data", "pos_test.tsv"))

    print(f"Sentences train={len(train)} val={len(val)} test={len(test)}")
    model_dict = train_crf_style_pickled_model(train, alpha=args.alpha)

    with open(args.out, "wb") as f:
        pickle.dump(model_dict, f)
    print(f"Wrote {args.out}")

    def token_acc(sents):
        tagger = CRFPOSTagger(args.out)
        ok = n = 0
        for sent in sents:
            words = [w for w, _ in sent]
            pred = tagger.tag_sentence(words)
            for (_, tg), (_, tp) in zip(sent, pred):
                n += 1
                if tg == tp:
                    ok += 1
        return ok / max(n, 1), ok, n

    acc_v, ok_v, n_v = token_acc(val)
    acc_t, ok_t, n_t = token_acc(test)
    print(f"Token accuracy val:  {acc_v:.4f} ({ok_v}/{n_v})")
    print(f"Token accuracy test: {acc_t:.4f} ({ok_t}/{n_t})")


if __name__ == "__main__":
    main()
