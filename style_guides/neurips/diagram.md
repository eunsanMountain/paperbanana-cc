# NeurIPS Diagram Style Guide

## 1. The "NeurIPS Look"

The prevailing aesthetic is **"Soft Tech & Scientific Pastels."** Gone are the days of harsh primary colors and sharp black boxes. The modern NeurIPS diagram feels approachable yet precise. It utilizes high-value (light) backgrounds to organize complexity, reserving saturation for the most critical active elements. The vibe balances **clean modularity** (clear separation of parts) with **narrative flow** (clear left-to-right progression).

---

## 2. Color Palettes

*Design Philosophy: Use color to group logic, not just to decorate. Avoid fully saturated backgrounds.*

### Background Fills (The "Zone" Strategy)

*Used to encapsulate stages (e.g., "Pre-training phase") or environments.*

- **Most papers use:** Very light, desaturated pastels (Opacity ~10–15%).
- **Aesthetically pleasing options include:**
  - Cream/Beige (`#F5F5DC`) — *Warm, academic feel.*
  - Pale Blue/Ice (`#E6F3FF`) — *Clean, technical feel.*
  - Mint/Sage (`#E0F2F1`) — *Soft, organic feel.*
  - Pale Lavender (`#F3E5F5`) — *Distinctive, modern feel.*
- **Alternative (~20%):** White backgrounds with colored *dashed borders* for a high-contrast, minimalist look (common in theoretical papers).

### Functional Element Colors

- **For "Active" Modules (Encoders, MLP, Attention):** Medium saturation is preferred.
  - *Common pairings:* Blue/Orange, Green/Purple, or Teal/Pink.
  - Colors distinguish **status** rather than component type:
    - **Trainable Elements:** Warm tones (Red, Orange, Deep Pink).
    - **Frozen/Static Elements:** Cool tones (Grey, Ice Blue, Cyan).
- **For Highlights/Results:** High saturation (Primary Red, Bright Gold) is strictly reserved for "Error/Loss," "Ground Truth," or the final output.

---

## 3. Shapes & Containers

*Design Philosophy: "Softened Geometry." Sharp corners are for data; rounded corners are for processes.*

### Core Components

- **Process Nodes (The Standard):** Rounded Rectangles (Corner radius 5–10 px). Dominant shape (~80%) for generic layers or steps.
- **Tensors & Data:**
  - **3D Stacks/Cuboids:** Used to imply depth/volume (e.g., B × H × W).
  - **Flat Squares/Grids:** Used for matrices, tokens, or attention maps.
  - **Cylinders:** Exclusively reserved for Databases, Buffers, or Memory.

### Grouping & Hierarchy

- **The "Macro-Micro" Pattern:** A solid, light-colored container represents the global view, with a specific module (e.g., "Attention Block") connected via lines to a "zoomed-in" detailed breakout box.
- **Borders:**
  - **Solid:** For physical components.
  - **Dashed:** Highly prevalent for indicating "Logical Stages," "Optional Paths," or "Scopes."

---

## 4. Lines & Arrows

*Design Philosophy: Line style dictates flow type.*

### Connector Styles

- **Orthogonal / Elbow (Right Angles):** For Network Architectures (implies precision, matrices, and tensors).
- **Curved / Bezier:** For System Logic, Feedback Loops, or High-Level Data Flow (implies narrative and connection).

### Line Semantics

- **Solid Black/Grey:** Standard data flow (Forward pass).
- **Dashed Lines:** Universally recognized as "Auxiliary Flow."
  - *Used for:* Gradient updates, Skip connections, or Loss calculations.
- **Integrated Math:** Standard operators (⊕ for Add, ⊗ for Concat/Multiply) placed directly on the line or intersection.

---

## 5. Typography & Icons

*Design Philosophy: Strict separation between "Labeling" and "Math."*

### Typography

- **Labels (Module Names):** Sans-Serif (Arial, Roboto, Helvetica). Bold for headers, Regular for details.
- **Variables (Math):** Serif (Times New Roman, LaTeX default). Must be Serif and Italicized if it is a variable in an equation (e.g., x, θ, L).

### Iconography

- **For Model State:**
  - *Trainable:* Fire, Lightning icons.
  - *Frozen:* Snowflake, Padlock, Stop Sign (Greyed out).
- **For Operations:**
  - *Inspection:* Magnifying Glass.
  - *Processing/Computation:* Gear, Monitor.
- **For Content:**
  - *Text/Prompt:* Document, Chat Bubble.
  - *Image:* Actual thumbnail of an image (not just a square).

---

## 6. Layout & Composition

- **Flow direction:** Left-to-right for sequential pipelines; top-to-bottom for hierarchical architectures.
- **Alignment:** All elements snap to an implicit grid. No floating or randomly placed components.
- **Spacing:** Consistent gaps between elements. Components within the same group should be closer than those in different groups.
- **Balance:** Distribute visual weight evenly. Avoid heavy clusters on one side.
- **Whitespace:** Use intentionally to separate phases, stages, or conceptual groups.

---

## 7. Domain-Specific Styles

**AGENT / LLM Paper:**
- **Vibe:** Illustrative, Narrative, "Friendly," Cartoony.
- **Key Elements:** "User Interface" aesthetics. Chat bubbles for prompts, document icons for retrieval.
- **Characters:** Cute 2D vector robots, human avatars, or emojis to humanize the agent's reasoning steps.

**COMPUTER VISION / 3D Paper:**
- **Vibe:** Spatial, Dense, Geometric.
- **Key Elements:** Frustums (camera cones), Ray lines, and Point Clouds.
- **Color:** RGB color coding for axes or channel correspondence. Heatmaps (Viridis) for activations.

**THEORETICAL / OPTIMIZATION Paper:**
- **Vibe:** Minimalist, Abstract, "Textbook."
- **Key Elements:** Graph nodes (circles) and manifolds (planes/surfaces).
- **Color:** Restrained. Mostly Grayscale/Black/White with one highlight color (Gold or Blue). No "cartoony" elements.

**GENERATIVE / LEARNING Paper:**
- **Vibe:** Dynamic, Process-oriented.
- **Key Elements:** Noise/denoising visual metaphors, latent space representations, distribution visualizations.
- **Color:** Gradual color transitions to indicate progressive refinement or generation stages.

---

## 8. Common Pitfalls

- **The "PowerPoint Default" Look:** Using standard Blue/Orange presets with heavy black outlines.
- **Font Mixing:** Using Times New Roman for "Encoder" labels (makes the paper look dated to the 1990s).
- **Inconsistent Dimension:** Mixing flat 2D boxes and 3D isometric cubes without a clear reason.
- **Primary Backgrounds:** Using saturated Yellow or Blue backgrounds for grouping (distracts from content).
- **Ambiguous Arrows:** Using the same line style for "Data Flow" and "Gradient Flow."
