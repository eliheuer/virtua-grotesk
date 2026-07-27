# Virtua Grotesk

_Placeholder article drafted 2026-07-26 from the project blog
(https://elih.net/blog/virtua-grotesk/). Review and finalize before submission._

Virtua Grotesk is a neo-grotesque sans-serif designed as both a finished
typeface and an open research project. It draws on modernist design
history — in particular Karl Gerstner's idea of "designing the system
instead of the final object" — and applies it through contemporary machine
learning.

## The grid system

At the heart of Virtua Grotesk is a dyadic, self-labeling grid: nested grids
built on powers of two up to the typeface's 1024-unit em (2¹⁰). Point
placement defaults to an 8-unit structural grid, with optical refinements
dropping to a 2-unit subgrid. Every coordinate is recorded as a sum of powers
of two — a property that automatically labels each value for machine learning
without extra annotation. A stem width of 96 units reads as 64 + 32; a
correction of 104 reads as 64 + 32 + 8. How many powers of two compose a
measurement ("popcount") signals whether a point is structural (low count) or
corrective (high count).

## A font that is also a dataset

This discipline makes the font sources double as machine-learning training
data by design, not by accident. A small language model — Virtua-12M — trains
on this grid-native data to learn the design system: it reads each glyph as a
sequence of drawing commands and coordinates and predicts the next token. It
can generate new letterforms, interpolate weights, and extend the typeface,
always producing coordinates that snap cleanly to the grid. The model runs on
standard consumer hardware and is released as open weights on Hugging Face.

## Why powers of two

Base-two grids keep normalized coordinates exact across platforms, and they
guarantee that the operations a font pipeline performs — halving for
interpolation, subdividing for rasterization, scaling at different pixel
sizes — land back on the grid. A cap height of 768 units (three-quarters of
1024) scales cleanly at any size, where a decimal grid would accumulate
rounding error.

## Availability

Virtua Grotesk is a first step toward generative fonts — typefaces that are
models rather than tables of static outlines. The sources and the model are
free and open-source; the font is licensed under the SIL Open Font License,
Version 1.1. Designed by Eli Heuer, with tooling from the open-source
Runebender font editor.
