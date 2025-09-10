# Image Assets Policy

Purpose: Ensure all image assets are organized, versioned, and free of redundant or legacy duplicates.

## Directories
- Debug captures: `tech/assets/images/debug/`
- Error & failure screenshots: `tech/assets/images/errors/`
- Future rendered outputs (demo thumbnails): `tech/assets/images/demos/` (create on first use)

## Rules
1. No PNG/JPG/GIF at repository root.
2. Filenames: `<context>_<shortdesc>_[v<major>.<minor>].png` for curated images; raw debug/error keep auto timestamping acceptable.
3. Large images (>1MB) must be optimized (pngquant or webp) before commit; keep original externally if needed.
4. Remove or archive obsolete debug images older than 90 days unless referenced in reports.
5. Reports referencing images must use relative paths within `tech/assets/images/`.
6. No binary images in panini/ axis unless they are domain reference diagrams (then prefer vector SVG under `panini/references/diagrams/`).

## Review Checklist
- [ ] New image under correct subfolder
- [ ] Size < 1MB (or justification documented in commit message)
- [ ] Referenced paths updated in markdown/tests
- [ ] Not duplicating an existing image (hash compare optional)

## Automation Ideas
- Add CI step to reject new root-level *.png
- Script to list images >1MB and produce optimization suggestions

