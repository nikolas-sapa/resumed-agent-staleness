"""Recompute the committed analyses/*.json from the raw runs in the v1.0 release bundle.

No API calls. Copies the bundle's pilot/ directory to a temp dir (the harness analyses write
their output next to the runs), runs each frozen analysis module, and compares the result
against analyses/ in this repo.

Usage:
    python3 scripts/reproduce_analyses.py <bundle.tar.gz | extracted bundle dir>

One documented, expected divergence: analysis-conf.json was frozen before the MC investigation
extended the changed-A-mc / changed-B-mc arms in runs-conf/ to 96 instances
(SPEC-MC-INVESTIGATION-frozen-2026-10-07.md, "existing arm extended"). Re-running
analyze_conf on the final bundle therefore sees the extended arms. For analysis-conf.json the
script compares everything except the mc-dependent fields, and checks that the recomputed
model_compacted pair equals analysis-mc.json M1_power instead.

Exit code 0 only if every check passes.
"""
from __future__ import annotations
import json, shutil, subprocess, sys, tarfile, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ANALYSES = REPO / "analyses"
MODULES = {
    "analysis.json": "analyze",
    "analysis-v2.json": "analyze_v2",
    "analysis-conf.json": "analyze_conf",
    "analysis-mc.json": "analyze_mc",
}
MC_CELLS = ("changed-A-mc", "changed-B-mc")


def find_pilot(root: Path) -> Path:
    for p in [root / "pilot", *root.glob("*/pilot")]:
        if (p / "harness").is_dir():
            return p
    sys.exit(f"no pilot/harness found under {root}")


def diff(a, b, path="") -> list[str]:
    if type(a) is not type(b):
        return [f"{path}: {a!r} != {b!r}"]
    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f"{path}/{k}: missing in {'recomputed' if k not in a else 'committed'}")
            else:
                out += diff(a[k], b[k], f"{path}/{k}")
        return out
    if isinstance(a, list):
        out = [f"{path}: length {len(a)} != {len(b)}"] if len(a) != len(b) else []
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff(x, y, f"{path}[{i}]")
        return out
    return [] if a == b else [f"{path}: recomputed {a!r} != committed {b!r}"]


def strip_mc(d: dict) -> dict:
    d = json.loads(json.dumps(d))
    for c in MC_CELLS:
        d["cell_rates"].pop(c, None)
    d.pop("model_compacted", None)
    d["infra_excluded"] = [x for x in d["infra_excluded"] if x["cell"] not in MC_CELLS]
    return d


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1]).expanduser().resolve()
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        if src.is_file():
            with tarfile.open(src) as tf:
                tf.extractall(tmp / "bundle", filter="data")
            pilot_src = find_pilot(tmp / "bundle")
        else:
            pilot_src = find_pilot(src)
        work = tmp / "pilot"
        shutil.copytree(pilot_src, work, ignore=shutil.ignore_patterns("analysis*.json", "__pycache__", "._*"))

        recomputed = {}
        for name, mod in MODULES.items():
            r = subprocess.run([sys.executable, "-m", f"harness.{mod}"], cwd=work,
                               capture_output=True, text=True)
            if r.returncode != 0 or not (work / name).exists():
                print(f"FAIL {name}: harness.{mod} exited {r.returncode}\n{r.stderr[-2000:]}")
                failures += 1
                continue
            recomputed[name] = json.loads((work / name).read_text())

    for name, got in recomputed.items():
        want = json.loads((ANALYSES / name).read_text())
        if name == "analysis-conf.json":
            problems = diff(strip_mc(got), strip_mc(want))
            mc = json.loads((ANALYSES / "analysis-mc.json").read_text())["M1_power"]
            mcp = got.get("model_compacted", {})
            for k in ("n_pairs", "rate_c1", "rate_c2", "reduction_pp", "reduction_ci95_pp"):
                if mcp.get(k) != mc.get(k):
                    problems.append(f"/model_compacted/{k}: recomputed {mcp.get(k)!r} != "
                                    f"analysis-mc.json M1_power {mc.get(k)!r}")
            note = " (mc arms excluded; model_compacted matches analysis-mc M1_power)"
        else:
            problems = diff(got, want)
            note = ""
        if problems:
            failures += 1
            print(f"FAIL {name}: {len(problems)} difference(s)")
            for p in problems[:20]:
                print("   ", p)
        else:
            print(f"OK   {name} reproduced exactly{note}")

    print("analysis-mc-exploratory.json: not recomputed (no generating script in the bundle)")
    print("PASS" if failures == 0 else f"FAIL ({failures} file(s))")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
