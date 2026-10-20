//! Focused rendering diagnostic; not a port of the complete review set.
//! Run from the repository root with the documented explicit input paths:
//! designbot --raw documentation/proofs/designbot_diagnostic.rs --output OUT.png -- light BEFORE.ttf AFTER.ttf LABEL.ttf PILLOW.rgba
//! The Pillow panel is a frozen control. All other text is rendered by DesignBot.
//! Before and after use independent renderer/font contexts to avoid family collisions.
use designbot::prelude::*;
use designbot_render::Renderer;
use std::{env, fs};
const W: u32 = 1600;
const H: u32 = 1280;
const LIGHT: Color = Color { r:222, g:222, b:222, a:255 };
const DARK: Color = Color { r:68, g:68, b:68, a:255 };
fn label(c: &mut Canvas, s: &str, x:f64, baseline:f64, size:f64, ink:Color) {
    c.fill(ink).font("Virtua Grotesk").clear_font_variations().font_variation("wght",400.0).font_size(size);
    c.text(s,x,H as f64-baseline);
}
fn main() {
    let args:Vec<_>=env::args().collect();
    assert_eq!(args.len(),6,"mode before.ttf after.ttf label.ttf pillow-control.rgba");
    assert!(args[1]=="light" || args[1]=="dark");
    let (paper,ink)=if args[1]=="light" {(LIGHT,DARK)} else {(DARK,LIGHT)};
    let mut r=Renderer::new(W,H);
    r.load_font(&args[4]).expect("Explicit caption font");
    if let Ok(dir)=env::var("PROBE_DIR") {
        fs::create_dir_all(&dir).unwrap();
        let mut probe_r=Renderer::new(320,80);
        probe_r.load_font(&args[4]).unwrap();
        for size in [18.0,20.0,40.0] {
            let mut probe=Canvas::new(320.0,80.0);
            probe.background(Color { r:0, g:0, b:0, a:0 });
            probe.fill(DARK).font("Virtua Grotesk").font_size(size);
            for (i,ch) in ["E","I","H","T"].iter().enumerate() {
                probe.text(ch,16.0+i as f64*80.0,20.0);
            }
            let pixels=probe_r.render_frames(&probe).remove(0).0;
            fs::write(format!("{dir}/designbot-{size:.0}.rgba"),pixels).unwrap();
        }
    }
    let mut c=Canvas::new(W as f64,H as f64);c.background(paper);
    label(&mut c,"Virtua Grotesk / Design Review",80.0,120.0,20.0,ink);
    label(&mut c,if args[1]=="light" {"Light"} else {"Dark"},1440.0,120.0,20.0,ink);
    label(&mut c,"Rendering Diagnostic",80.0,200.0,64.0,ink);
    label(&mut c,"Same Virtua File / Same Sizes / Two Rendering Paths",80.0,240.0,24.0,ink);
    c.fill(ink).rect(80.0,H as f64-280.0,1440.0,1.0);
    label(&mut c,"Pillow / Previous Caption Renderer",80.0,320.0,26.0,ink);
    label(&mut c,"DesignBot / Parley And Swash",800.0,320.0,26.0,ink);
    let control=fs::read(&args[5]).expect("Frozen Pillow control");
    assert_eq!(control.len(),640*200*4);
    c.image_rgba(control,640,200,80.0,H as f64-520.0,1.0);
    for (s,baseline,size) in [
        ("Individual Glyphs / Equal Em Scale",360.0,20.0),
        ("Equal Em Scale And Baseline",400.0,18.0),
        ("E I H T / E I H T",480.0,40.0)] {
        label(&mut c,s,800.0,baseline,size,ink);
    }
    c.fill(ink).rect(80.0,H as f64-560.0,1440.0,1.0);
    label(&mut c,"Virtua / Before",80.0,600.0,26.0,ink);
    label(&mut c,"Virtua / Applied",800.0,600.0,26.0,ink);
    for (name,y) in [("400 / Regular",640.0),("700 / Bold",920.0)] {
        label(&mut c,name,80.0,y,20.0,ink);
        label(&mut c,"192 / 32 px Per Em",1280.0,y,20.0,ink);
    }
    // Each isolated full-size transparent layer has exactly one Virtua binary.
    // Composite at integer coordinates and native size: no rescaling or fitting.
    for (font,x) in [(&args[2],80.0),(&args[3],800.0)] {
        let mut glyph_r=Renderer::new(W,H);glyph_r.load_font(font).expect("Explicit Virtua file");
        let mut glyph_c=Canvas::new(W as f64,H as f64);
        glyph_c.background(Color { r:0, g:0, b:0, a:0 });
        glyph_c.fill(ink).font("Virtua Grotesk");
        for (weight,baseline) in [(400.0,800.0),(700.0,1080.0)] {
            glyph_c.clear_font_variations().font_variation("wght",weight);
            glyph_c.font_size(192.0).text("ד ר",x,H as f64-baseline);
            glyph_c.font_size(32.0).text("דרך חדר סדר",x,H as f64-baseline-40.0);
        }
        let mut pixels=glyph_r.render_frames(&glyph_c).remove(0).0;
        // This backend returns premultiplied RGB, while image_rgba expects
        // straight alpha. For this single-color layer, restore the known ink
        // RGB and retain coverage. Otherwise dark mode gains dark edge halos.
        for pixel in pixels.chunks_exact_mut(4) {
            pixel[0]=ink.r;pixel[1]=ink.g;pixel[2]=ink.b;
        }
        c.image_rgba(pixels,W,H,0.0,0.0,1.0);
    }
    c.fill(ink).rect(80.0,H as f64-1160.0,1440.0,1.0);
    label(&mut c,"Fixed Scale And Baselines / DesignBot Hinting Enabled / Weight Remains Provisional",80.0,1200.0,18.0,ink);
    if env::var("GRID_VIEW").as_deref()==Ok("1") {
        for x in (80..=1520).step_by(40) {c.fill(ink).rect(x as f64,80.0,0.25,1120.0);}
        for y in (80..=1200).step_by(40) {c.fill(ink).rect(80.0,y as f64,1440.0,0.25);}
    }
    r.render_to_png(&c,"out.png").expect("Raw diagnostic render");
}
