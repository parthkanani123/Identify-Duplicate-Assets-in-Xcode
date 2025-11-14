#!/usr/bin/env python3
import sys, os, json, hashlib, csv, platform, re
from collections import Counter
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow not found. Install with:  python3 -m pip install pillow")
    sys.exit(1)

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".heic", ".heif", ".webp"}
BINARY_EXTS = {".pdf", ".svg"}
SCALE_RE = re.compile(r'@([123]x)(?=\.)', re.IGNORECASE)

def get_xcassets_dirs(root: Path):
    if root.is_dir() and root.name.endswith('.xcassets'):
        yield root
        return
    for p in root.rglob('*.xcassets'):
        if p.is_dir():
            yield p

def normalize_basename(path: Path) -> str:
    """Return file name without scale suffix and extension."""
    name = path.stem
    name = re.sub(r'@(?:1x|2x|3x)\b', '', name, flags=re.IGNORECASE)
    return name

def normalize_and_hash_image(img_path: Path) -> tuple[str, tuple[int, int]]:
    try:
        with Image.open(img_path) as img:
            img = img.convert('RGBA')
            data = img.tobytes()
            size = img.size
            h = hashlib.sha256(data).hexdigest()
            return (h, size)
    except Exception:
        return ("", (0, 0))

def hash_file_bytes(file_path: Path) -> tuple[str, tuple[int, int]]:
    try:
        data = file_path.read_bytes()
        h = hashlib.sha256(data).hexdigest()
        return (h, (0, 0))
    except Exception:
        return ("", (0, 0))

def detect_scale(path: Path) -> str:
    m = SCALE_RE.search(path.name)
    if m:
        return m.group(1).lower()  # '1x'/'2x'/'3x'
    return ""

def collect_assets(root: Path):
    print(f"🔍 Scanning for assets in: {root}")
    by_hash = {}
    for xcassets_dir in get_xcassets_dirs(root):
        for imageset_dir in xcassets_dir.rglob("*.imageset"):
            for file_path in imageset_dir.glob("*"):
                suffix = file_path.suffix.lower()
                if suffix in IMAGE_EXTS:
                    h, size = normalize_and_hash_image(file_path)
                elif suffix in BINARY_EXTS:
                    h, size = hash_file_bytes(file_path)
                else:
                    continue
                if not h:
                    continue
                entry = {
                    "imageset": str(imageset_dir),
                    "xcassets": str(xcassets_dir),
                    "scale": detect_scale(file_path),
                    "norm": normalize_basename(file_path),
                    "hash": h,
                }
                by_hash.setdefault(h, []).append(entry)
    return by_hash

def resolve_output_path(user_path: str) -> Path:
    default_name = "duplicate_assets.csv"
    if not user_path:
        return Path(os.getcwd()) / default_name
    p = Path(user_path).expanduser().resolve()
    if p.suffix.lower() == ".csv":
        p.parent.mkdir(parents=True, exist_ok=True)
        return p
    if p.exists() and p.is_dir():
        return p / default_name
    else:
        p.mkdir(parents=True, exist_ok=True)
        return p / default_name

def scale_score(scale: str) -> int:
    return {"3x": 3, "2x": 2, "1x": 1, "": 0}.get(scale.lower(), 0)

def collapse_scale_duplicate_groups(by_hash: dict, ignore_intra_imageset: bool = True):
    """Collapse groups that differ only by scale across same imagesets."""
    candidate_groups = []
    for h, entries in by_hash.items():
        if len(entries) <= 1:
            continue
        if ignore_intra_imageset and len({e["imageset"] for e in entries}) <= 1:
            continue
        candidate_groups.append(entries)

    collapsed = {}
    for entries in candidate_groups:
        imagesets_set = frozenset(e["imageset"] for e in entries)
        norm_counts = Counter(e["norm"] for e in entries)
        norm_name, _ = norm_counts.most_common(1)[0]
        key = (imagesets_set, norm_name)
        best_scale = max((scale_score(e["scale"]) for e in entries), default=0)
        existing = collapsed.get(key)
        if existing is None or best_scale > existing[0]:
            collapsed[key] = (best_scale, entries)
    return [entries for _, entries in collapsed.values()]

def save_duplicates_to_csv(groups: list, output_csv: Path):
    print(f"💾 Saving results to: {output_csv}")
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Group", "Hash", "Imageset", "Scale"])  # 👈 last column removed
        for idx, entries in enumerate(groups, start=1):
            group_hash = entries[0]["hash"]
            for e in entries:
                writer.writerow([
                    f"Group {idx}",
                    group_hash,
                    e["imageset"],
                    e["scale"]
                ])
            writer.writerow([])  # blank line
    print(f"✅ Duplicate list saved successfully! Groups written: {len(groups)}")

def maybe_open_in_finder(path: Path):
    try:
        if platform.system() == "Darwin":
            os.system(f'open "{path.parent}"')
    except Exception:
        pass

def main():
    input_path = input("📁 Enter .xcassets folder's location: ").strip()
    if not input_path:
        print("❌ No path entered. Exiting.")
        sys.exit(1)
    root = Path(input_path).expanduser()
    if not root.exists():
        print("❌ Invalid path. Please enter a valid folder path.")
        sys.exit(1)

    output_path_str = input("💾 Enter CSV file path or folder to save results: ").strip()
    output_csv = resolve_output_path(output_path_str)

    by_hash = collect_assets(root)
    collapsed_groups = collapse_scale_duplicate_groups(by_hash, ignore_intra_imageset=True)
    save_duplicates_to_csv(collapsed_groups, output_csv)
    maybe_open_in_finder(output_csv)

if __name__ == "__main__":
    main()
