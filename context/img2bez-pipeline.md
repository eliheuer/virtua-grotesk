# img2bez: Research References & Alternative Approaches

This document collects research references and alternative vectorization approaches that were evaluated before building img2bez. Kept as reference for future exploration.

## Alternative Autotracing Tools

| Tool | Type | License | Notes |
|------|------|---------|-------|
| [VTracer](https://github.com/visioncortex/vtracer) | Rust/Python | MIT | Good general-purpose, outputs SVG only |
| [Potrace](https://potrace.sourceforge.net/) | C/Python | GPL v2 | Classic, used by FontForge. img2bez uses Potrace's algorithm internally |
| [StarVector-1B](https://huggingface.co/starvector/starvector-1b-im2svg) | Python/GPU | — | Vision-language model, image→SVG, rough but fast |

## AI/ML Approaches for Font Vectorization

### Differentiable Rendering (for refinement)
- **DiffVG** — Differentiable vector renderer. Optimize control points against target image via backprop. ([github](https://github.com/BachiLi/diffvg))
- **Bezier Splatting** (NeurIPS 2025) — 30-150x faster than DiffVG. ([github](https://github.com/WeixiongLin/Bezier-Splatting), [paper](https://arxiv.org/abs/2503.16424))

### Neural Vector Font Generation
- **DeepVecFont-v2** (CVPR 2023) — Transformer-based vector font generation. ([github](https://github.com/yizhiwang96/deepvecfont-v2))
- **VecFusion** (CVPR 2024, Adobe) — Cascaded diffusion for vector fonts
- **Chat2SVG** (CVPR 2025) — LLM + DiffVG hybrid. Stage 3 (coordinate refinement) could be extracted for font use. ([github](https://github.com/kingnobro/Chat2SVG))
- **OmniSVG** (NeurIPS 2025) — Built on Qwen2.5-VL, generates SVG from text/images. ([github](https://github.com/OmniSVG/OmniSVG))

### Variable Font Specific
- **Differentiable Variable Fonts** (Oct 2025) — Makes variable font interpolation differentiable in PyTorch. Could optimize axis values against target images. ([paper](https://arxiv.org/abs/2510.07638))

### What Doesn't Work Well for Fonts
- LLMs writing bezier coordinates from scratch — insufficient spatial precision
- SAM for glyph extraction — overkill, simple thresholding is better
- ControlNet/diffusion alone — generates rasters, not vectors
- Fine-tuning LLMs on SVG data — ACCV 2024 showed worse results than baseline for simple Latin

## Bold Master Generation Strategies

For variable fonts, both masters need identical structure (same contours, point counts, types). Only coordinates and widths differ.

### Approach 1: Trace Both, Match Structure
1. Trace Regular and Bold independently
2. Use DiffVG to optimize one topology against both targets
3. Guarantees compatibility by construction

### Approach 2: Derive Bold from Regular
1. Trace Regular only
2. Apply Virtua Grotesk's counter-reduction rules:
   - Outer contours: keep identical coordinates
   - Inner counters: offset inward by `(bold_stem - regular_stem) / 2`
   - Adjust advance widths proportionally

### Approach 3: DiffVG/Bezier Splatting Optimization
1. Define topology from Regular trace
2. Initialize Bold = Regular coordinates
3. Render differentiably, compare to Bold target image
4. Backpropagate to adjust coordinates
5. Repeat until converged

## Useful Libraries

| Library | Language | Use |
|---------|----------|-----|
| [kurbo](https://github.com/linebender/kurbo) | Rust | Bezier math, curve fitting (used by img2bez) |
| [norad](https://github.com/linebender/norad) | Rust | UFO read/write (used by img2bez) |
| [imageproc](https://github.com/image-rs/imageproc) | Rust | Image processing, thresholding (used by img2bez) |
| [tiny-skia](https://github.com/nickel-org/tiny-skia) | Rust | Path rasterization (used by img2bez render) |
| [fontTools](https://github.com/fonttools/fonttools) | Python | Font manipulation, SVG parsing |
| [beziers.py](https://github.com/simoncozens/beziers.py) | Python | Path operations (offset, tidy, extrema) |
| [svg2glif](https://crates.io/crates/svg2glif) | Rust | SVG→GLIF conversion |

## Key References

- [Raph Levien: Simplifying Bezier Paths](https://raphlinus.github.io/curves/2023/04/18/bezpath-simplify.html) — Math behind kurbo's simplifier
- [OHno Type: Drawing Vectors](https://ohnotype.co/blog/drawing-vectors) — Type design conventions for point placement
- [Typography Research Collection](https://github.com/IShengFang/TypographyResearchCollection) — Index of font/typography AI papers
