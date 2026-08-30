# MCP and Environment Setup

Use this procedure when Blender control or AI 3D generation capabilities are missing.

## Capability inventory

Check the current tool catalog for capabilities equivalent to:

- inspect/control Blender and run Blender Python;
- export, import, and inspect GLB/glTF assets;
- submit text-to-3D or image-to-3D jobs;
- poll asynchronous generation jobs;
- download/import generated assets;
- verify a browser canvas and console.

Do not require exact historical names such as `blender-mcp_generate_hunyuan3d_model`. MCP server prefixes and tool names vary by installation and version.

Run `python scripts/check_environment.py --pretty` for read-only local diagnostics. Treat its `mcpInspection` field as a reminder that MCP availability must be checked by the agent from the live tool catalog.

## Consent gate

On first invocation, when no related Blender-control or AI-3D MCP capability is available, perform this consent gate before modeling even when local Blender or Three.js can provide a fallback:

1. State the missing capability and whether it is required or optional.
2. Recommend one of these paths:
   - local Blender-only/Three.js fallback;
   - local Blender MCP;
   - local Hunyuan3D or another local AI model;
   - hosted AI 3D service/API.
3. Disclose material consequences: download size, GPU/VRAM need, installation location, network access, possible API charges, reference-image upload, account/credential requirement, and license limits.
4. Ask for explicit consent before any install, model download, account connection, paid request, or MCP configuration change.
5. Pause for the user's answer. If the user declines, continue with the best available fallback and record the limitation without asking again during the same task.

Do not promise that an MCP path is free until its current server license, model/backend, hosting mode, and provider pricing have been verified from official sources. Distinguish a free/open-source MCP server from GPU, model-hosting, cloud API, and electricity costs.

Never treat a general request to model an object as consent to install software or incur charges.

## Installation after consent

After explicit consent:

1. Verify the current official repository or vendor documentation; installation commands and package names are time-sensitive.
2. Prefer official releases, package registries, checksums, pinned versions, and user-scoped installation.
3. Do not pipe remote scripts directly into a shell. Do not disable security controls. Do not expose tokens in commands, logs, files, or chat.
4. Request platform approval when network or out-of-sandbox writes require it.
5. Install only the selected dependency and its documented prerequisites.
6. Configure secrets through the product's secure settings or environment mechanism, never inside the skill.
7. Restart/reload the MCP host if required.
8. Re-inspect the live tool catalog and run a harmless health check. Package presence alone is not proof that an MCP capability is usable.
9. If verification fails, troubleshoot within the approved scope or fall back; never repeatedly install unrelated packages.

## Local Hunyuan guidance

- Treat local model weights/code as separate from compute cost and licensing.
- Check the selected version's official VRAM and platform requirements before downloading.
- Confirm sufficient storage and GPU compatibility.
- Keep AI generation optional; Blender remains the deterministic fallback.

## Hosted service guidance

- Confirm the provider, price/credits, retention policy, reference-image privacy, output terms, and rate limits before use.
- Ask again before the first paid generation if the earlier consent did not clearly authorize charges.
- Record provider/model and settings in asset metadata without recording secrets.
