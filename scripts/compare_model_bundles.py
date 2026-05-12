
from __future__ import annotations

import argparse
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from model_presets import bundle_paths_for_preset
from integrated_sanskrit_processor import IntegratedSanskritProcessor


def _fmt_pos(tagged):
    if not tagged:
        return "(none)"
    lines = []
    for item in tagged:
        if len(item) >= 2:
            lines.append(f"  {item[0]!s:<22} {item[1]}")
    return "\n".join(lines) if lines else "(none)"


def _fmt_sandhi(ops):
    if not ops:
        return "(none)"
    lines = []
    for op in ops:
        orig = op.get("original", "")
        sp = op.get("split", [orig])
        lines.append(f"  {orig!s}  ->  {' + '.join(sp)}  ({op.get('method', '')})")
    return "\n".join(lines)


def _run(proc: IntegratedSanskritProcessor, text: str) -> dict:
    r = proc.process_text(text)
    pos = r.get("pos_analysis", {}) or {}
    sand = r.get("sandhi_analysis", {}) or {}
    return {
        "tokens": r.get("tokens", []),
        "tagged": pos.get("tagged_tokens", []),
        "sandhi_ops": sand.get("sandhi_operations", sand.get("operations", [])),
        "confidence": r.get("overall_confidence"),
        "error": r.get("error"),
    }


def _build(label: str, preset: str) -> IntegratedSanskritProcessor | None:
    p = bundle_paths_for_preset(PROJECT_ROOT, preset)
    pos_p = p["pos_model_path"]
    sd_p = p["sandhi_bilstm_path"]
    voc = p.get("sandhi_vocab_path")
    if not os.path.isfile(pos_p):
        print(f"[{label}] missing POS model: {pos_p}")
        return None
    if not os.path.isfile(sd_p):
        print(f"[{label}] missing sandhi model: {sd_p}")
        return None
    voc_arg = voc if (voc and os.path.isfile(voc)) else None
    return IntegratedSanskritProcessor(
        pos_model_path=pos_p,
        bilstm_threshold=0.7,
        use_bilstm=True,
        sandhi_checkpoint_path=sd_p,
        sandhi_vocab_json_path=voc_arg,
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="A/B compare default vs processed model bundles")
    ap.add_argument(
        "--text",
        action="append",
        help="Sanskrit sentence (repeat for multiple). Default: built-in samples",
    )
    args = ap.parse_args()

    samples = args.text or [
        "अमृतत्वस्य तु नाशास्ति वित्तेन ।",
        "रामः सीतां पश्यति",
        "तथापि गच्छति",
    ]

    print("Loading default bundle…")
    default_p = _build("default", "default")
    print("Loading processed bundle…")
    processed_p = _build("processed", "processed")

    if not default_p and not processed_p:
        sys.exit(1)
    if not default_p:
        print("Only processed model available; comparisons are one-sided.")
    if not processed_p:
        print("Only default model available; train processed models first.")

    for i, text in enumerate(samples, 1):
        print("\n" + "=" * 72)
        print(f"Sample {i}: {text!r}")
        print("=" * 72)
        d = None
        p = None
        if default_p:
            d = _run(default_p, text)
            print("\n--- DEFAULT ---")
            if d.get("error"):
                print("Error:", d["error"])
            else:
                print("tokens:", d["tokens"])
                print("POS:\n" + _fmt_pos(d["tagged"]))
                print("sandhi:\n" + _fmt_sandhi(d["sandhi_ops"]))
                print(f"overall_confidence: {d.get('confidence')}")
        if processed_p:
            p = _run(processed_p, text)
            print("\n--- PROCESSED ---")
            if p.get("error"):
                print("Error:", p["error"])
            else:
                print("tokens:", p["tokens"])
                print("POS:\n" + _fmt_pos(p["tagged"]))
                print("sandhi:\n" + _fmt_sandhi(p["sandhi_ops"]))
                print(f"overall_confidence: {p.get('confidence')}")
        if default_p and processed_p and d is not None and p is not None:
            dt = tuple(d["tokens"]) if not d.get("error") else ()
            pt = tuple(p["tokens"]) if not p.get("error") else ()
            dg = tuple((a[0], a[1]) for a in (d.get("tagged") or []) if len(a) >= 2) if not d.get("error") else ()
            pg = tuple((a[0], a[1]) for a in (p.get("tagged") or []) if len(a) >= 2) if not p.get("error") else ()
            print("\n--- DIFF SUMMARY ---")
            print(f"  tokens equal: {dt == pt}")
            print(f"  POS tags equal: {dg == pg}")


if __name__ == "__main__":
    main()
