"""
Resolve POS + sandhi model file paths from a single preset or per-file env overrides.

Environment:
  SANSKRIT_MODEL_PRESET   default | processed   (optional; default bundle if unset or empty)
  POS_MODEL_PATH          overrides preset POS path if set to an existing file
  SANDHI_BILSTM_PATH      overrides preset sandhi .pt if set to an existing file
  SANDHI_VOCAB_PATH       overrides sandhi_vocab.json for default bundle (optional)

When preset is ``processed``, vocab comes from the BiLSTM checkpoint (sandhi_vocab.json omitted).
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional


def _abs(project_root: str, *parts: str) -> str:
    return os.path.normpath(os.path.join(project_root, *parts))


def _bundles(project_root: str) -> Dict[str, Dict[str, Optional[str]]]:
    root = os.path.abspath(project_root)
    return {
        "default": {
            "pos_model_path": _abs(root, "models", "enhanced_crf_pos_model_v3.pkl"),
            "sandhi_bilstm_path": _abs(root, "models", "bilstm_sandhi.pt"),
            "sandhi_vocab_path": _abs(root, "models", "sandhi_vocab.json"),
        },
        "processed": {
            "pos_model_path": _abs(root, "models", "processed_data", "crf_pos_from_processed.pkl"),
            "sandhi_bilstm_path": _abs(root, "models", "processed_data", "bilstm_sandhi_from_processed.pt"),
            "sandhi_vocab_path": None,
        },
    }


def bundle_paths_for_preset(project_root: str, preset: str) -> Dict[str, Any]:
    """
    Paths for a named bundle only (ignores POS_MODEL_PATH / SANDHI_* env overrides).
    Use for A/B scripts that load two checkpoints in one process.
    """
    key = preset.strip().lower()
    bundles = _bundles(project_root)
    if key not in bundles:
        raise ValueError(f"Unknown preset {preset!r}; expected 'default' or 'processed'")
    b = bundles[key]
    return {
        "preset": key,
        "pos_model_path": b["pos_model_path"],
        "sandhi_bilstm_path": b["sandhi_bilstm_path"],
        "sandhi_vocab_path": b.get("sandhi_vocab_path"),
    }


def resolve_sanskrit_model_paths(project_root: str) -> Dict[str, Any]:
    project_root = os.path.abspath(project_root)
    preset = os.environ.get("SANSKRIT_MODEL_PRESET", "").strip().lower()
    bundles = _bundles(project_root)

    if preset == "processed":
        base = bundles["processed"]
        preset_used = "processed"
    elif preset in ("", "default"):
        base = bundles["default"]
        preset_used = "default"
    else:
        print(f"⚠️  Unknown SANSKRIT_MODEL_PRESET={preset!r}; using 'default' bundle.")
        base = bundles["default"]
        preset_used = "default"

    pos = os.environ.get("POS_MODEL_PATH", "").strip()
    if pos and os.path.isfile(pos):
        pos_model_path = pos
    else:
        pos_model_path = base["pos_model_path"]

    sandhi_pt = os.environ.get("SANDHI_BILSTM_PATH", "").strip()
    if sandhi_pt and os.path.isfile(sandhi_pt):
        sandhi_bilstm_path = sandhi_pt
    else:
        sandhi_bilstm_path = base["sandhi_bilstm_path"]

    vocab = os.environ.get("SANDHI_VOCAB_PATH", "").strip()
    if vocab and os.path.isfile(vocab):
        sandhi_vocab_path: Optional[str] = vocab
    else:
        sandhi_vocab_path = base.get("sandhi_vocab_path")

    return {
        "preset": preset_used,
        "pos_model_path": pos_model_path,
        "sandhi_bilstm_path": sandhi_bilstm_path,
        "sandhi_vocab_path": sandhi_vocab_path,
    }
