//! The section-03 technical-drawing language, as a reusable preset.
//!
//! Ported from the blog-figure crate's `technical.rs`. A binary should specify
//! only content (which outlines, where, which fills, which measurements). Grid
//! appearance, point language, pen weights, and point size belong here so every
//! social sheet reads as the same drawing that `fig-system-no` established.

use designbot::prelude::Color;

use crate::{
    draw_body, draw_points_gridlevel, draw_points_neutral, line, role, source_grid, Format, Frame,
    Outline, PointStyle, Sheet,
};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum PointPalette {
    /// The canonical `no`/`HO` treatment: two light-gray point tiers.
    Neutral,
    /// Green on the 8-unit structure grid, red off it (optical correction).
    GridLevel,
}

/// One reviewed technical-drawing language shared by all glyph sheets.
#[derive(Clone, Copy, Debug)]
pub struct TechnicalStyle {
    pub pen: f64,
    pub grid_stroke: f64,
    pub grid_unit: f64,
    pub point_size: f64,
    pub palette: PointPalette,
}

impl TechnicalStyle {
    /// The canonical preset established by `fig-system-no`/`fig-system-ho`,
    /// scaled for social canvases (heavier pen, larger points for phone view).
    pub const fn section_three() -> Self {
        Self {
            pen: line::HERO,
            grid_stroke: line::FINE,
            grid_unit: 8.0,
            point_size: 26.0,
            palette: PointPalette::Neutral,
        }
    }

    /// Preserve the geometry and typography, make grid membership the point
    /// color's explicit job (green machine grid / red hand correction).
    pub const fn with_grid_level_points(mut self) -> Self {
        self.palette = PointPalette::GridLevel;
        self
    }

    pub const fn with_grid(mut self, unit: f64, stroke: f64) -> Self {
        self.grid_unit = unit;
        self.grid_stroke = stroke;
        self
    }

    pub const fn with_point_size(mut self, size: f64) -> Self {
        self.point_size = size;
        self
    }

    /// Fit one source run inside a format, reserving optional title/caption
    /// bands (in pixels) at the top and bottom of the live area.
    pub fn frame(&self, format: Format, run: f64, bottom: f64, top: f64, band_top: f64, band_bottom: f64) -> Frame {
        Frame::fit(format, run, bottom, top, band_top, band_bottom)
    }

    /// Draw the real uniform source grid across the glyph run.
    pub fn grid(&self, sheet: &mut Sheet, f: &Frame, glyphs: &[(&Outline, f64)], bottom: f64, top: f64) {
        source_grid(
            sheet,
            f,
            glyphs,
            bottom,
            top,
            self.grid_unit,
            role::grid::faint(),
            self.grid_stroke,
        );
    }

    /// Draw one opaque glyph with the canonical pen and point language.
    pub fn glyph(&self, sheet: &mut Sheet, o: &Outline, f: &Frame, fill: Color) {
        draw_body(sheet, o, f, fill, role::figure::pen(), self.pen);
        let style = PointStyle {
            size: self.point_size,
            stroke_width: self.pen,
        };
        match self.palette {
            PointPalette::Neutral => draw_points_neutral(sheet, o, f, style),
            PointPalette::GridLevel => draw_points_gridlevel(sheet, o, f, style),
        }
    }

    /// Draw only the point language (no body), for morph frames where the body
    /// is already filled.
    pub fn points(&self, sheet: &mut Sheet, o: &Outline, f: &Frame) {
        let style = PointStyle {
            size: self.point_size,
            stroke_width: self.pen,
        };
        match self.palette {
            PointPalette::Neutral => draw_points_neutral(sheet, o, f, style),
            PointPalette::GridLevel => draw_points_gridlevel(sheet, o, f, style),
        }
    }
}
