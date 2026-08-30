---
name: soil-teaching-deck
description: >
  Create, analyze, or improve SOIL-style teaching PowerPoint decks. Use when the
  user asks for teaching slides, classroom slides, lesson-material-to-slides,
  SOIL slides, instructional presentation design, or a review of an existing
  teaching deck's cognitive load and teaching flow. Produces editable .pptx
  slides with PowerPoint text objects, optional AI illustrations, optional
  geometry diagrams, and a SOIL teaching structure.
metadata:
  short-description: SOIL editable teaching PPTX deck
---

# SOIL Teaching Deck

Use this skill for editable instructional PowerPoint decks. The goal is teaching
clarity first, visual design second, and file correctness last.

## Output Contract

- Produce an editable `.pptx` unless the user asks only for diagnosis or style.
- Text should remain PowerPoint text objects.
- Every non-geometric visual image, including cover visuals, background images,
  illustrations, section-divider images, and card images, must be generated with
  Codex's built-in image generation capability first. Do not substitute local
  shape rendering or procedural placeholder images for AI images.
- For math symbols in PowerPoint, use the two-layer text-box approach when needed:
  keep readable surrounding text editable, and isolate symbols/formulas in
  separate boxes or rendered image snippets if PowerPoint text handling is weak.
- Report the final absolute file path.

## Mode Selection

Choose the path from the user's request:

- Material to deck: run SOIL engines 1-6.
- Topic only: first expand a minimal teaching outline, then run engines 1-6.
- Existing deck review: inspect the deck, run cognitive diagnosis, then propose
  or implement fixes.
- Style definition: run only the style engine and output a reusable style spec.

If the user has already provided enough detail, do not stop for a long interview.
Ask only the next missing detail that affects the work, usually audience and
lesson duration.

## Core Workflow

1. Concept positioning: identify the one big idea, three sub-ideas, common
   misunderstandings, takeaway sentence, minimal fact pack, and slide-vs-talk
   split. See `references/soil-engines.md`.
2. Context positioning: arrange 引起動機 -> 維持注意 -> 喚起行動.
3. Page architecture: choose page roles, one core point per page, layout recipe,
   and any `visuals` or `geometry` needs. See `references/layout-recipes.md`.
4. Cognitive editing: reduce noise, chunk, add information, structure, sequence,
   and step the content.
5. Style construction: define palette, fonts, title/body scale, motif, and image
   policy.
6. Build and verify the PPTX using the local presentation workflow. Prefer the
   available Presentations skill when it is active; otherwise use
   `python-pptx` patterns consistent with the repo.

## Design Rules

- Use a 16:9 wide deck.
- Type scale: cover title 72-84pt, slide title 44-56pt, subtitle 28-34pt,
  body 18-21pt, muted 14-16pt.
- Use bold, readable Chinese fonts. Default to Microsoft JhengHei unless a
  project font is clearly available.
- Keep page titles short, ideally <= 10 Chinese characters.
- Use fixed alignment grids and consistent margins.
- Every page should have either a visual, a diagram, a comparison structure, a
  strong question, or a clear typographic focal point.
- Use only 1-2 accent colors.

## References

- Read `references/soil-engines.md` for SOIL planning outputs.
- Read `references/layout-recipes.md` before building slides.
- Read `references/visual-assets.md` when AI illustrations or background images
  are needed.
- Read `references/geometry.md` for math diagrams.
- Read `references/validation.md` before final delivery.

## Codex Conversion Notes

- Do not use Claude-only paths such as `/home/claude`, `/mnt/skills`, or
  `.claude/skills/draw/draw.py`.
- Use PowerShell in commands and user-facing examples.
- Use Codex built-in image generation for every bitmap visual image. Only precise
  math/geometry diagrams are exempt; those should be deterministic SVG/Python
  drawings for correctness.
- Keep AGENTS.md clean; progress and teaching notes belong in Obsidian if the
  user asks for project synchronization.
