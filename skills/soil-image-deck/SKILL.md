---
name: soil-image-deck
description: >
  Create a SOIL-style image-first presentation where each slide is a full-page
  bitmap image, then package the images into a .pptx. Use when the user asks for
  a pure image deck, all-image slides, AI-generated poster-like slides, quick
  visual-impact teaching slides, livestream opening slides, social sharing
  slides, or a deck where later text editing is not important. Supports baked
  mode and plate mode with editable PowerPoint text overlays.
metadata:
  short-description: SOIL full-image PPTX deck
---

# SOIL Image Deck

Use this skill for visual-impact decks where every slide is driven by one
full-page image.

## Output Modes

- `baked`: each generated image already contains the slide text; the PPTX is one
  full-bleed image per slide.
- `plate`: generated images contain no text; the PPTX overlays editable
  PowerPoint text boxes from `spec.yaml`.

Default to `baked` for speed and social/livestream materials. Use `plate` when
the user needs editable text or expects later revisions.

## Hard Image Rule

Every slide image in this skill must be produced with Codex's built-in image
generation capability first. Do not create the slide images through local
Pillow/CSS/SVG/shape rendering, procedural graphics, or placeholder panels unless
the user explicitly asks for a non-AI prototype. The value of this skill is that
the slide itself is an AI-generated visual artifact.

## Workflow

1. Determine whether the user has material, only a topic, or an existing YAML
   spec. If enough information is already present, proceed directly.
2. Produce a page plan: page number, role, core point, minimal on-image text,
   image brief, and layout hint.
3. Define an `image_policy` with style tokens, negative prompt, size, quality,
   palette, and any pages upgraded to higher quality.
4. Generate images with the built-in image generation skill and preserve those
   generated outputs for packaging into `slides/images/`.
5. Visually inspect generated images before packaging. Reject images with
   unreadable text, wrong layout, unwanted symbols, or style drift.
6. Package the deck using `scripts/pack_pptx.py`.
7. Report the final `.pptx` absolute path and mode used.

## Design Rules

- Keep each slide to one core point.
- For baked mode, keep Chinese on-image text under about 20 characters per slide
  when possible.
- Avoid asking image generation to render dense paragraphs or data tables.
- Use SOIL rhythm: 引起動機 -> 維持注意 -> 喚起行動.
- Use 1-2 accent colors and consistent visual style.
- Cover and action pages may use higher image quality.

## Packaging

From the project folder, use PowerShell:

```powershell
python .\skills_codex\soil-image-deck\scripts\pack_pptx.py `
  --images-dir .\slides\images `
  --output .\slides\output.pptx `
  --mode baked
```

For editable overlay mode:

```powershell
python .\skills_codex\soil-image-deck\scripts\pack_pptx.py `
  --images-dir .\slides\images `
  --output .\slides\output-editable.pptx `
  --mode plate `
  --spec .\slides\spec.yaml
```

## When To Read References

- Read `references/spec-format.md` when using `plate` mode.
- Read `references/image-prompts.md` before generating images.

## Dependencies

- Python packages: `python-pptx`, `Pillow`, `PyYAML`.
- Image generation must use Codex's built-in image generation capability for
  every slide image. If the current environment cannot save those generated
  images to local files, stop and explain the file-persistence limitation instead
  of substituting local rendered graphics.
