
from __future__ import annotations

import math
import os
import unicodedata
from typing import Dict, List, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def load_sandhi_tsv_rows(tsv_path: str) -> List[Tuple[str, List[str]]]:
    
    out: List[Tuple[str, List[str]]] = []
    with open(tsv_path, encoding="utf-8") as f:
        next(f, None)  # header
        for line in f:
            line = line.strip()
            if not line or "\t" not in line:
                continue
            left, right = line.split("\t", 1)
            if not left.startswith("segment:"):
                continue
            combined = _nfc(left.replace("segment:", "", 1).strip())
            parts = [_nfc(p) for p in right.strip().split() if p]
            if not combined or not parts:
                continue
            if " " in combined:
                continue
            if sum(len(p) for p in parts) != len(combined):
                continue
            out.append((combined, parts))
    return out


def load_pos_tsv_sentences(tsv_path: str) -> List[List[Tuple[str, str]]]:
    """Each inner list is [(word, tag), ...] from tag: ... \\t w|TAG ..."""
    sentences: List[List[Tuple[str, str]]] = []
    with open(tsv_path, encoding="utf-8") as f:
        next(f, None)
        for line in f:
            line = line.strip()
            if not line or "\t" not in line:
                continue
            left, right = line.split("\t", 1)
            if not left.startswith("tag:"):
                continue
            tokens = []
            for piece in right.split():
                if "|" not in piece:
                    continue
                w, t = piece.rsplit("|", 1)
                tokens.append((w, t))
            if tokens:
                sentences.append(tokens)
    return sentences


def train_crf_style_pickled_model(
    sentences: List[List[Tuple[str, str]]],
    alpha: float = 0.1,
) -> Dict:
    """Build dict compatible with src.crf_pos_tagger.CRFPOSTagger.load_model."""
    tag_counts: Dict[str, float] = {}
    word_tag: Dict[str, Dict[str, float]] = {}
    trans: Dict[str, Dict[str, float]] = {}

    for sent in sentences:
        prev = "<START>"
        for w, t in sent:
            tag_counts[t] = tag_counts.get(t, 0.0) + 1.0
            word_tag.setdefault(w, {})
            word_tag[w][t] = word_tag[w].get(t, 0.0) + 1.0
            trans.setdefault(prev, {})
            trans[prev][t] = trans[prev].get(t, 0.0) + 1.0
            prev = t

    tags = sorted(tag_counts.keys())
    n_tags = max(len(tags), 1)

    emission_probs: Dict[str, Dict[str, float]] = {}
    for w, d in word_tag.items():
        tot = sum(d.values()) + alpha * n_tags
        emission_probs[w] = {t: math.log((d.get(t, 0.0) + alpha) / tot) for t in tags}

    transition_probs: Dict[str, Dict[str, float]] = {}
    for p, d in trans.items():
        tot = sum(d.values()) + alpha * n_tags
        transition_probs[p] = {t: math.log((d.get(t, 0.0) + alpha) / tot) for t in tags}

    known_words = set(word_tag.keys())
    known_tags = set(tags)

    return {
        "emission_probs": emission_probs,
        "transition_probs": transition_probs,
        "feature_weights": {},
        "known_words": list(known_words),
        "known_tags": list(known_tags),
        "is_trained": True,
    }
