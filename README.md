# PaperBanana CC

A **Claude Code Skill/Plugin** for generating publication-quality academic diagrams and plots.

Built entirely upon [PaperBanana](https://arxiv.org/abs/2601.23265) — this project re-implements the full pipeline from the original research as a Claude Code-native skill, where **Claude Code itself acts as the orchestrating VLM** (Vision-Language Model) for every stage: paper analysis, reference retrieval, structured planning, venue-specific styling, and iterative vision-based critique.

## Based On

This project is a Claude Code adaptation of the following works:

| | |
|---|---|
| **Paper** | [PaperBanana: A Multi-Modal Academic Figure Generation Framework](https://arxiv.org/abs/2601.23265) |
| **Original Repos** | [dwzhu-pku/PaperBanana](https://github.com/dwzhu-pku/PaperBanana) (research prototype) · [llmsresearch/paperbanana](https://github.com/llmsresearch/paperbanana) (production package) |

All prompts, reference datasets, style guides, and pipeline design are derived from the above. **PaperBanana CC** restructures them into a Claude Code Skill so that Claude Code subscribers can generate academic figures through natural conversation — no separate VLM server or complex setup required.

## Why Claude Code?

Claude Code already includes a state-of-the-art VLM with tool use, vision, and long-context capabilities. Instead of running a separate inference server, PaperBanana CC leverages **Claude Code as both the reasoning engine and the orchestrator**:

- **Zero infrastructure** — no GPU server, no model downloads, no Docker
- **Full context across phases** — the Critic can compare the generated image against the *original* methodology, not just the final prompt
- **Interactive refinement** — the user confirms direction at each stage via natural conversation
- **Plugin distribution** — install once, use in any project

## Image Generation Options

| Method | Requirement | Best For |
|--------|-------------|----------|
| **OpenAI API** (gpt-image-1) | `OPENAI_API_KEY` | Highest quality diagrams |
| **Gemini API** (Imagen 3) | `GOOGLE_API_KEY` | Fast iteration, flexible ratios |
| **Manual generation** | Any image AI subscription | **No API key needed** — use ChatGPT, Gemini, or any web-based image generator |

The **manual generation mode** is designed for users who have a subscription to Google AI Pro, ChatGPT Plus, or similar services but don't want to set up API keys. PaperBanana CC generates the optimized prompt, you paste it into your preferred web UI, and provide the resulting image back for critique.

## Pipeline

```
[Phase 0] Input Enrichment
  Methodology text + caption → 7-axis structuring + 6-spec caption enhancement
  ← User confirms direction

[Phase 1] Reference Retrieval
  538 reference examples → 2-axis semantic matching → top-10 with images
  ← User selects references

[Phase 2] Plan → Style → Generate
  Venue (NeurIPS/ICML/ACL/IEEE) + generation method selection
  → 7-item structured plan → venue-specific styling → image generation
  Prompt always displayed and saved

[Critic Loop] Iterative Refinement (default 3 rounds)
  Claude Code vision critique → revision or completion
  ← User can provide additional feedback at any point
```

All phases except image generation are performed directly by Claude Code. Prompts and style guides from the original PaperBanana research are used to instruct Claude Code at each stage.

## Installation

### Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) subscription (Claude Pro / Max / Team)
- [uv](https://docs.astral.sh/uv/) (for `uvx` — Python dependencies are installed automatically)
- **Optional**: OpenAI API key and/or Google API key (not required for manual generation)

### Install via Plugin Marketplace

```bash
# 0. Install uv (if not installed) — required for image generation
curl -LsSf https://astral.sh/uv/install.sh | sh

# 1. Add marketplace (one-time)
/plugin marketplace add eunsanMountain/paperbanana-cc

# 2. Install plugin
/plugin install paperbanana-cc@paperbanana-marketplace

# 3. (Optional) Set API keys — not required for manual generation mode
echo "OPENAI_API_KEY=sk-..." >> .env
echo "GOOGLE_API_KEY=AI..." >> .env
```

That's it. No `git clone`, no `uv sync` — the plugin loads skills directly, and Python dependencies are fetched on-demand via `uvx`.

Reference data (~300MB) is downloaded automatically on first run.

### Alternative: Local Development

```bash
git clone https://github.com/eunsanMountain/paperbanana-cc.git
cd paperbanana-cc && uv sync
claude --plugin-dir ./
```

## Usage

Since Claude Code runs inside your project, PaperBanana CC can **read your codebase directly** — no copy-pasting needed. Just point it at the relevant source files:

```
> /paperbanana

Analyze src/model/transformer.py and generate an architecture diagram
showing the data flow from input embedding through the attention layers.

Caption: "Overview of the proposed multi-modal transformer architecture."
```

Claude Code reads the code, understands the architecture, enriches the context, retrieves similar reference figures, and generates a publication-ready diagram — all within your project's context.

### More examples

```bash
# Generate from a method description
/paperbanana A 4-layer CNN with batch normalization for image classification

# Create a plot from experimental results
/paperbanana Plot the accuracy comparison from results/ablation.csv

# Analyze multiple files for a system diagram
/paperbanana Read src/pipeline/ and create a data flow diagram of the entire inference pipeline
```

## Supported Venues

| Venue | Diagram Style | Plot Style |
|-------|--------------|------------|
| NeurIPS | Clean, minimal, blue-tone | Publication DPI, colorblind-safe |
| ICML | Similar to NeurIPS | Same conventions |
| ACL | NLP-focused conventions | Same conventions |
| IEEE | Two-column optimized | IEEE figure standards |

## License

Apache-2.0

## Citation

If you use PaperBanana CC in your research, please cite the original paper:

```bibtex
@article{zhu2025paperbanana,
  title={PaperBanana: A Multi-Modal Academic Figure Generation Framework},
  author={Zhu, Dewei and others},
  journal={arXiv preprint arXiv:2601.23265},
  year={2025}
}
```

## Acknowledgments

This project is built entirely upon the [PaperBanana](https://arxiv.org/abs/2601.23265) framework by [dwzhu-pku](https://github.com/dwzhu-pku/PaperBanana) and [llmsresearch](https://github.com/llmsresearch/paperbanana). All core prompts, reference datasets, evaluation criteria, and style guides originate from their work. PaperBanana CC restructures these into a Claude Code Skill to make the pipeline accessible to Claude Code subscribers without additional infrastructure.
