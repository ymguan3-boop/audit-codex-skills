# Art-Quality and Batch Gate

Use this gate for reference-driven hero assets, characters, creatures, evolution/product families, and any batch where visual identity matters.

## Status model

Keep these statuses separate:

- `TECHNICAL_PASS`: file opens, exports, imports, and meets structural checks.
- `ART_REVIEW_PENDING`: technical checks passed but visual fidelity is not approved.
- `USER_APPROVED_PILOT`: the representative asset is approved for its pathway.
- `VERIFIED`: both technical and art gates passed for the delivered asset.
- `REJECTED_ART_QUALITY`: visual evidence fails even if file and polygon checks pass.

Never count `TECHNICAL_PASS` or `ART_REVIEW_PENDING` as verified.

## Baseline discovery

Before building:

1. Inspect prior sources, renders, manifests, screenshots, and user comments.
2. Identify the latest explicitly approved example and rejected examples.
3. Record exact baseline paths, approval evidence, intended style, and required identity features.
4. Use the approved example as the minimum silhouette, anatomy, feature-density, material, and rig-quality baseline. Polygon count does not override it.
5. If no approval history exists, mark the first representative asset `ART_REVIEW_PENDING` and request visual approval before batch expansion when fidelity is material.

## Representative evidence

Produce one representative per materially different anatomy/topology or modeling pathway. Show, on one comparison sheet:

- authoritative reference;
- approved prior baseline when available;
- rejected candidate when diagnosing a regression;
- candidate front, three-quarter, side, back, and close-up views;
- at least one locally deformed rig pose when animation is required.

Do not self-approve subjective resemblance by writing “manually reviewed.” Record who approved the pilot and the evidence path. When the user has already rejected a batch for visual quality, require explicit user approval of the corrective pilot before processing the remaining batch.

## Visual acceptance

Check evidence, not labels:

- primary silhouette and body mass distribution;
- proportions and placement of head, torso, limbs, appendages, and negative spaces;
- identity features, color/material regions, and important back/side forms;
- meaningful stage/variant differences; related assets must not read as the same base with scaled parts;
- purposeful secondary forms and surface transitions visible in close-up;
- absence of primitive-looking intersections, floating parts, thin cover plates, and accidental gaps;
- anatomy-appropriate rig joints and visible local deformation without detachment or collapse.

For a family or evolution line, compare every stage on one sheet. Reject the family when stage differentiation is materially weaker than the reference or approved baseline.

## High-poly regression signals

Stop and reject instead of rationalizing when any signal appears:

- triangle count rises sharply while silhouette and secondary-form information stay unchanged;
- the method is primarily subdivision of a simplified primitive assembly;
- the result has fewer meaningful anatomical parts or rig joints than an approved lower-count pilot;
- a manifest says subdivision alone is unacceptable while the build method relies on it;
- technical metrics pass but side-by-side evidence is visibly worse;
- multiple stages share nearly identical proportions, poses, or appendage layouts.

Subdivision may refine an already approved, information-rich mesh. Record the pre-subdivision art source and prove that the source itself meets the visual baseline.

## Rig gate

Define required joint groups per asset before rigging. Check the joints that drive visible motion rather than using a universal bone-count threshold. For limbs, normally inspect proximal, middle, and distal articulation; inspect spine/head and tail, wing, fin, ear, jaw, or other identity appendages when relevant. Render representative extreme poses and re-import the exported GLB before approval.

## Batch governance

- Freeze and identify the approved pilot source and evidence sheet.
- Expand by anatomy/topology pathway, not merely by a shared theme or franchise.
- Checkpoint each asset and retain source provenance.
- Create family sheets during production; do not wait until the entire batch is complete to discover regressions.
- Stop the pathway immediately when a sample falls below baseline. Repair and reapprove before continuing.

## Rejection and recovery

When a delivered asset or batch is found to fail art quality:

1. Change the top-level status to `REJECTED_ART_QUALITY` and set delivery approval to false.
2. Set verified counts to zero for the rejected scope; do not leave per-asset summaries implying approval.
3. Add a visible `REJECTED-NOT-FOR-DELIVERY` marker and prevent game integration.
4. Preserve failed sources as evidence; rename archives to include `REJECTED` instead of deleting them.
5. Identify the last approved baseline and rebuild from it or from a new representative pilot.
6. Re-run technical checks, visual comparison, deformation checks, and user approval. Never reuse the old `VERIFIED` claim.
