# User-Approved Visual Baselines

Read this file before every modeling task for this user.

## Active minimum standard

On 2026-08-13, the user explicitly approved the corrective V3 Mudkip, Marshtomp, and Swampert family as:

- the minimum visual-quality baseline for rebuilding the remaining 24 Pokémon; and
- the minimum design-rigor baseline for future 3D-modeling requests.

Project evidence:

- `C:/Users/ymguan/Documents/新遊戲專案/prototype/starters-gen1-3/highpoly-redesign/blender-pokedex-highpoly-v3-corrective/production/APPROVED-BASELINE.md`
- `C:/Users/ymguan/Documents/新遊戲專案/prototype/starters-gen1-3/highpoly-redesign/blender-pokedex-highpoly-v3-corrective/production/hoenn-water-corrective-comparison.jpg`
- editable sources under `production/sources/`;
- high GLBs under `production/models/high/`;
- per-asset evidence under `production/verification/`.

Measured examples:

| Asset | High triangles | Purposeful feature meshes | Bones | Clips |
|---|---:|---:|---:|---:|
| Mudkip | 474,564 | 34 | 9 | 8 |
| Marshtomp | 540,200 | 38 | 14 | 8 |
| Swampert | 682,736 | 45 | 13 | 8 |

## Interpretation

Use V3 as a quality floor for:

- deliberate primary silhouette and readable mass distribution;
- purposeful secondary forms rather than primitive inflation;
- anatomy or construction logic appropriate to the subject;
- clear differences among stages, variants, or related assets;
- clean close-up curvature and intentional material/color regions;
- anatomy-appropriate rigging and local deformation when animation is required;
- side-by-side evidence and honest separation of technical versus art approval.

Do not force Pokémon proportions, the example's materials, 250k+ triangles, 8 clips, or its bone counts onto unrelated assets. Choose measurable budgets from the actual brief, but never lower the design rigor. A static product may need no rig; a low-poly prop may need far fewer polygons; a hero creature may need more detail and joints.

If the evidence paths are unavailable, retain these quality criteria and ask the user to reattach a visual baseline only when literal style matching is material.

## Blue-polo child protagonist baseline

On 2026-08-14, the user approved the static V3.8 character appearance for rigging. Preserve these non-negotiable features in all runtime and animated derivatives:

- cute enlarged head with a broad rounded crown, not an egg shape or pointed crown;
- short connected neck; no head/body separation;
- no facial features and no display base;
- collar, placket, and badge conformed to the shirt rather than floating;
- natural closed hand silhouette with no isolated pointing finger;
- ankles overlapping shoe openings; flat-bottom deep-navy athletic shoes;
- the accepted two-tone blue polo appearance, not white, gray, near-black, or a differently saturated blue.

Project evidence:

- approved master: `C:/Users/ymguan/Documents/新遊戲專案/prototype/reference-child-character/highpoly-featureless-v3/sources/blue-polo-child-featureless-high-v3.blend`;
- approved views: `C:/Users/ymguan/Documents/新遊戲專案/prototype/reference-child-character/highpoly-featureless-v3/previews/`;
- runtime comparison: `C:/Users/ymguan/Documents/新遊戲專案/prototype/reference-child-character/animated-v3.8/color-match-comparison-v2.jpg`;
- current animation review: `C:/Users/ymguan/Documents/新遊戲專案/prototype/reference-child-character/animated-v3.8/animation-review-sheet-v2.jpg`;
- rejected weak throw: `C:/Users/ymguan/Documents/新遊戲專案/prototype/reference-child-character/animated-v3.8/REJECTED-v1-weak-forward-throw/`.

The approved displayed polo samples are upper `#C7E4EC`, lower `#82BDD9`, and accent `#2CA6D1`. Treat them as render-display targets, not raw shader inputs. The GLB-safe implementation uses a packed 512x512 color-block texture with UVs. The static appearance is `USER_APPROVED_PILOT`; animation remains independently reviewable and must not inherit approval automatically.

## Remaining 24 Pokémon

Treat the V2 batch as `REJECTED_ART_QUALITY` and never reuse it as the shape source. For each materially different anatomy/topology family:

1. build an information-rich representative from official references;
2. compare official reference, V3 design rigor, candidate five views, and deformed rig evidence;
3. ensure evolution stages have distinct proportions, silhouette, and appendage layout;
4. expand the family only after its pathway passes the art and technical gates;
5. never count a file-only or polygon-only pass as verified.
