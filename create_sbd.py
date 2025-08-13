#!/usr/bin/env python3
from pathlib import Path
import shutil

# Point to the top of your export! This expects the "your-email-adress" folder
ROOT = Path(r"relative-path-to-your-mbox-export").resolve()

def unique(p: Path) -> Path:
    if not p.exists():
        return p
    stem, suf = (p.stem, p.suffix) if p.suffix else (p.name, "")
    i = 2
    while (np := p.with_name(f"{stem} ({i}){suf}")).exists():
        i += 1
    return np

def mailbox_in(dirpath: Path) -> Path | None:
    """Prefer file named like the folder; fallback to 'mbox'."""
    cand = dirpath / dirpath.name
    if cand.is_file():
        return cand
    cand = dirpath / "mbox"
    return cand if cand.is_file() else None

def fix_one(folder: Path):
    parent, name = folder.parent, folder.name
    # Free 'parent/name' so we can place the mailbox file there
    tmp = unique(parent / (".__TMP__" + name))
    folder.rename(tmp)

    mbx = mailbox_in(tmp)
    mailbox_target = unique(parent / name)

    if mbx:
        shutil.move(str(mbx), str(mailbox_target))
    elif not mailbox_target.exists():
        mailbox_target.touch()  # container-only folder still visible in TB

    # If subfolders remain, tmp becomes '<name>.sbd'; otherwise remove if empty
    has_children = any(p.is_dir() for p in tmp.iterdir())
    if has_children:
        tmp.rename(unique(parent / f"{name}.sbd"))
    else:
        try:
            tmp.rmdir()
        except OSError:
            tmp.rename(unique(parent / f"{name}.sbd"))

def main():
    # Process deepest-first to keep paths valid during renames
    dirs = [p for p in ROOT.rglob("*") if p.is_dir() and not p.name.endswith(".sbd")]
    dirs.sort(key=lambda p: len(p.parts), reverse=True)

    # Include ROOT itself only if it actually contains a mailbox (avoid renaming a pure container like 'mbox_dir')
    if (ROOT / ROOT.name).is_file() or (ROOT / "mbox").is_file():
        dirs.append(ROOT)

    for d in dirs:
        if d.exists() and d.is_dir() and not d.name.endswith(".sbd"):
            fix_one(d)

    print("✅ Done. Thunderbird-ready: 'Name' (mailbox file) + 'Name.sbd' (subfolders).")

if __name__ == "__main__":
    main()
