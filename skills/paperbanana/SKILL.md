---
name: paperbanana
description: Generate publication-quality academic diagrams and statistical plots from methodology text and caption. Multi-phase pipeline with reference retrieval, structured planning, venue-specific styling, and iterative critic refinement. Use this skill whenever the user wants to create academic figures, conference diagrams, methodology illustrations, architecture diagrams, or statistical plots for papers.
argument-hint: "[methodology text or file path] [caption]"
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion
---

# PaperBanana CC - Academic Illustration Generator

Claude Code native pipeline for publication-quality academic diagrams and plots.
Claude Code acts as the thinking engine — analysis, planning, styling, and critique are all performed by you directly.
Only image generation uses external APIs (OpenAI / Gemini) or manual web generation.

**Pipeline:** Input Enrichment -> Reference Retrieval -> Plan + Style + Generate -> Critic Loop

## Key Principles

- **Cross-phase context**: You maintain full conversation state across all phases. Later phases (Planner, Stylist, Critic) can and should reference outputs from earlier phases. The Critic should compare the generated image against the original methodology, not just the final description.
- **Ask when uncertain**: If the methodology text is ambiguous about a component's role, connection, or visual representation, ask the user for clarification rather than guessing. A brief question now prevents a full regeneration cycle later.
- **Diagram vs Plot awareness**: Diagrams and plots follow different rules throughout the pipeline — especially for color specification (natural language vs HEX codes) and generation method (image API vs matplotlib code). Pay attention to which type you are working with at each phase.

---

## Before Starting

### Step 0: Resolve paths

This skill uses two directory roots:

- **`{PLUGIN_DIR}`** — where PaperBanana CC is installed (contains `prompts/`, `style_guides/`, `data/`). All pipeline resource files are read from here.
- **`{CWD}`** — the user's current working directory. Output artifacts are saved here.

To find `{PLUGIN_DIR}`, locate the directory containing this SKILL.md file, then go up 3 levels:

```bash
# This SKILL.md is at {PLUGIN_DIR}/.claude/skills/paperbanana/SKILL.md
# Find the plugin root by searching for the project marker
PLUGIN_DIR=$(dirname "$(dirname "$(dirname "$(find ~/.claude/plugins -path '*/paperbanana-cc/prompts/context_enricher.md' 2>/dev/null | head -1)")")")
```

If running locally (inside the paperbanana-cc directory itself), `{PLUGIN_DIR}` equals `{CWD}`.

**Shorthand used below:**
- `{P}/prompts/...` means `{PLUGIN_DIR}/prompts/...`
- `{P}/style_guides/...` means `{PLUGIN_DIR}/style_guides/...`
- `{P}/data/...` means `{PLUGIN_DIR}/data/...`
- `output/...` means `{CWD}/output/...` (user's project)

### Step 1: Check reference data (auto-download)

```bash
ls {P}/data/references/diagram/ref.json {P}/data/references/plot/ref.json 2>/dev/null
```

If either file is missing, automatically run the download — do not ask the user:

```bash
uvx paperbanana-cc download --target "{P}/data/references"
```

This downloads ~300MB from HuggingFace on first run. Subsequent runs skip if data exists.

### Step 2: Create run directory

Generate a run ID (timestamp-based) and create the output directory in the **user's current working directory**:

```
output/{run_id}/
```

Save all artifacts to this directory throughout the pipeline.

---

## Phase 0: Input Enrichment

**Always runs. User confirmation required.**

### Step 0-1: Receive input

The user provides:
- **Methodology text**: The method section or description (inline text or file path)
- **Caption**: The figure caption or communicative intent

If a file path is given, Read the file. Save originals to `output/{run_id}/input.md`.

### Step 0-2: Context Enricher

Read `{P}/prompts/context_enricher.md` and follow its instructions.

Apply the enricher to the methodology text, restructuring it along 7 axes:
1. Components
2. Data Flow
3. Groupings
4. Input/Output
5. Key Relationships
6. Sequential vs Parallel
7. Mathematical Operations

### Step 0-3: Caption Sharpener

Read `{P}/prompts/caption_sharpener.md` and follow its instructions.

Transform the caption into a detailed visual specification (under 150 words) covering:
1. Diagram type
2. Key elements
3. Visual narrative
4. Scope
5. Emphasis
6. Flow direction

### Step 0-4: User confirmation

Present the results side-by-side:

```
## Original Input
[methodology text]
[caption]

## Enriched
[enriched context — 7-axis structured]
[sharpened caption — 6-spec enhanced]

## Changes
[brief explanation of what was changed and why]
```

Ask: "Is this direction correct? Any modifications?"

- User approves -> proceed to Phase 1
- User requests changes -> apply modifications and re-confirm
- Save result to `output/{run_id}/enriched.md`

---

## Phase 1: Reference Retrieval

**Retrieves top-10 similar examples for few-shot guidance.**

### Step 1-1: Determine type

Based on the enriched input, determine whether this is a **diagram** or **plot**:
- Diagram: architecture, pipeline, framework, block diagram, data flow, comparison
- Plot: bar chart, line plot, scatter, heatmap, confusion matrix, ablation table

### Step 1-2: Load reference data (2-stage retrieval)

ref.json files are large (~4MB). Use a 2-stage approach to save context:

**Stage 1: Python pre-filter** — Narrow the candidate pool using keyword/category matching:

```bash
uvx paperbanana-cc filter-refs \
  --ref-json "{P}/data/references/{type}/ref.json" \
  --keywords "{keyword1},{keyword2},..." \
  --limit 100
```

**Stage 2: Semantic ranking** — Read the ~50-100 pre-filtered candidates in context, then apply 2-axis matching semantically to select the final top-10.

### Step 1-3: 2-axis matching

Read `{P}/prompts/retriever_system.md` and follow its matching logic on the pre-filtered candidates.

Select top-10 references using 2-axis matching:

**For Diagrams:**
- Axis 1: Research Topic (same domain)
- Axis 2: Visual Intent (same diagram type)
- Priority: Same Topic + Same Visual Intent > Same Visual Intent only > Avoid different Visual Intent
- Key principle: "Structure is more important than Topic for drawing"

**For Plots:**
- Axis 1: Data Characteristics (same data type)
- Axis 2: Plot Type (same visualization)
- Priority: Same Data + Same Plot Type > Same Plot Type > Avoid different Plot Type

### Step 1-4: Display references

For each of the top-10, display:
- Reference ID
- Caption / visual intent
- The reference image (Read the image file from `{P}/data/references/{type}/images/`)

### Step 1-5: User selection

Use **AskUserQuestion** tool for selection:

```
question: "Which references do you want to use?"
options:
  - "Use all 10"
  - "Let me pick specific ones"
  - "Re-search with different criteria"
```

If "Let me pick specific ones": ask which numbers (e.g., "1,3,5,7").

Save selection to `output/{run_id}/references.json`.

---

## Phase 2: Settings + Plan + Style + Generate

**Three internal phases executed in sequence after user selects settings.**

### Step 2-0: User settings

Use **AskUserQuestion** tool for each setting:

**Venue:**
```
question: "Which venue style?"
options:
  - "NeurIPS (default)"
  - "ICML"
  - "ACL"
  - "IEEE"
```

**Generation method:**
```
question: "How should the image be generated?"
options:
  - "OpenAI API (gpt-image-1)"
  - "Gemini API (Imagen 3)"
  - "Manual (I'll generate from the prompt myself)"
```

Save to `output/{run_id}/settings.json`.

### Step 2-1: Plan (Internal Phase 2)

Read `{P}/prompts/planner_system.md` and follow its instructions.

Read the selected reference images (vision) as few-shot examples.

Generate a detailed 7-item structured plan:
1. **Overall layout** — flow direction, major sections
2. **Components** — exact labels for each box/module
3. **Connections** — arrows, data flow direction
4. **Groupings** — how components are grouped
5. **Labels and annotations** — text labels, math notation
6. **Input/Output** — system entry and exit points
7. **Styling** — background, color palette (natural language for diagrams, NEVER hex codes; exact HEX codes for plots)

Include `RECOMMENDED_RATIO` based on the generation method:

| Method | Supported Ratios |
|--------|-----------------|
| OpenAI | 1:1, 3:2, 2:3 |
| Gemini | 1:1, 2:3, 3:2, 3:4, 4:3, 9:16, 16:9, 21:9 |
| Manual | Any |

Save to `output/{run_id}/plan.md`.

### Step 2-2: Style (Internal Phase 3)

Read `{P}/prompts/stylist_system.md` and follow its 6 instructions.

Load the venue-specific style guide:

```
{P}/style_guides/{venue}/diagram.md   # for diagrams
{P}/style_guides/{venue}/plot.md      # for plots
```

If the style guide file is missing, use the fallback guidelines embedded in the stylist prompt.

Apply styling rules to the plan. The 6 crucial rules:
1. **Preserve Aesthetics** — NEVER hex codes, pixel dimensions, CSS
2. **Intervene Only When Necessary** — preserve what's already good
3. **Respect Diversity** — adapt to domain-specific conventions
4. **Enrich Details** — add specific natural-language visual descriptions
5. **Preserve Content** — no adding/removing components
6. **Handle Icons with Care** — preserve semantic meaning

Save to `output/{run_id}/styled_plan.md`.

### Step 2-3: Generate (Internal Phase 4)

#### For Diagrams

Compose the final image generation prompt from the styled plan.

**CRITICAL**: Prepend role preamble and append text garbling prevention:
> "You are an expert scientific diagram illustrator. Generate high-quality scientific diagrams based on the following description. Note that do not include figure titles in the image.
>
> CRITICAL: All text labels in the diagram must be rendered in clear, readable English. Use the EXACT label names specified in the description. Do NOT generate garbled, misspelled, or non-English text."

Save prompt to `output/{run_id}/prompt.md`.

**Always display the full prompt to the user.**

**If OpenAI API:**
```bash
uvx paperbanana-cc generate \
  --provider openai \
  --prompt-file "{CWD}/output/{run_id}/prompt.md" \
  --output "{CWD}/output/{run_id}/iter_1/image.png" \
  --ratio "{recommended_ratio}"
```

**If Gemini API:**
```bash
uvx paperbanana-cc generate \
  --provider gemini \
  --prompt-file "{CWD}/output/{run_id}/prompt.md" \
  --output "{CWD}/output/{run_id}/iter_1/image.png" \
  --ratio "{recommended_ratio}"
```

**If Manual:**
Display the prompt clearly and ask the user to:
1. Copy the prompt
2. Generate in ChatGPT web / Gemini web / Midjourney / etc.
3. Provide the image file path

Copy or move the user-provided image to `output/{run_id}/iter_1/image.png`.

#### For Plots

Do NOT use image generation APIs. Instead:
1. Write matplotlib code directly based on the styled plan
2. Execute via Bash: `python output/{run_id}/plot_code.py`
3. If error: analyze the error, fix the code, re-execute
4. Requirements: DPI 300, publication-quality, colorblind-friendly palette

Save the generated image to `output/{run_id}/iter_1/image.png`.

---

## Critic Loop (Phase 5)

**Default: 3 iterations maximum. User can request more.**

### Step 5-1: Critique

Read the critic prompt for the current type:
- Diagrams: `{P}/prompts/critic_diagram.md`
- Plots: `{P}/prompts/critic_plot.md`

Read (vision) the generated image at `output/{run_id}/iter_{N}/image.png`.

Evaluate against these criteria:

**Content:**
- Fidelity & Alignment — matches methodology, no hallucination
- Text QA — no typos, garbled text, hex/CSS rendered as text
- Validation — accurate math, attention maps
- Caption Exclusion — figure caption must NOT appear in image
- Gibberish detection — no non-English random characters
- Background check — no black/dark backgrounds (academic publishing)
- Artifact detection — no grid lines, pixelation, blur

**Presentation:**
- Clarity & Readability
- Legend Management — remove redundant legends

**Plot-specific:**
- Data Fidelity — quantitative accuracy
- Overlap & Layout — no element collision
- Generation Failures — simplify description if code keeps failing

### Step 5-2: Decision

**If changes needed:**
- Save critique to `output/{run_id}/iter_{N}/critic.md`
- Generate revised prompt incorporating critic feedback + previous image context
- Save to `output/{run_id}/iter_{N+1}/prompt.md`
- Re-generate image (same method as Step 2-3)
- Increment N, repeat from Step 5-1

**If no changes needed (or max iterations reached):**
- Save final critique to `output/{run_id}/iter_{N}/critic.md`
- Proceed to Step 5-3

### Step 5-3: User satisfaction

Display the final image and critic summary.

Use **AskUserQuestion** tool:

```
question: "Are you satisfied with the result?"
options:
  - "Yes, looks good!"
  - "No, I have feedback for refinement"
```

If "No": ask for specific feedback, then continue the critic loop.

---

## Output Summary

When the pipeline completes, report:

```
Run ID: {run_id}
Type: diagram / plot
Venue: {venue}
Method: {method}
Iterations: {N}
Final image: output/{run_id}/iter_{N}/image.png
Prompt: output/{run_id}/prompt.md
All artifacts: output/{run_id}/
```

## Artifact Structure

```
output/{run_id}/
  input.md              # Original methodology + caption
  enriched.md           # Phase 0: enriched context + sharpened caption
  references.json       # Phase 1: selected reference IDs + paths
  settings.json         # Phase 2: venue, method, ratio
  plan.md               # Phase 2: 7-item structured plan
  styled_plan.md        # Phase 3: style-applied plan
  prompt.md             # Final generation prompt
  iter_1/
    image.png           # Generated image
    prompt.md           # Iteration prompt (includes prior critic)
    critic.md           # Critic evaluation
  iter_2/
    ...
  iter_3/
    ...
```
