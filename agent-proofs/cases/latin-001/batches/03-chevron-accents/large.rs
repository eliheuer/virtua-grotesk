use designbot::prelude::*;
use designbot_render::Renderer;
use std::env;
const W:u32=1600; const H:u32=1200; const WGHT:u32=u32::from_be_bytes(*b"wght");
fn main(){
 let a:Vec<String>=env::args().collect();assert_eq!(a.len(),16);
 let weight:f32=a[1].parse().unwrap();let size:f64=a[2].parse().unwrap();
 let ink=Color{r:222,g:222,b:222,a:255};let mut renderer=Renderer::new(W,H);renderer.load_font(&a[7]).unwrap();
 let mut page=Canvas::new(W as f64,H as f64);page.background(Color{r:68,g:68,b:68,a:255});
 page.fill(ink).font("Virtua Grotesk").font_size(32.0).font_variation("wght",400.0).text(&a[3],64.0,H as f64-64.0);
 page.font_size(22.0).text(&format!("Weight {weight:.0} · {size:.0} px/em · Manual review draft"),64.0,H as f64-104.0);
 for i in 0..3 {
  let y=140.0+i as f64*344.0;let path=&a[7+i*3];let family=&a[8+i*3];let label=&a[9+i*3];
  page.fill(ink).rect(64.0,H as f64-y,1472.0,2.0);page.font_size(24.0).text(label,64.0,H as f64-y-34.0);
  if label.contains("[unavailable]"){page.font_size(22.0).text("Characters unavailable in this reference file",88.0,H as f64-y-170.0);continue;}
  let mut r=Renderer::new(W,H);r.load_font(path).unwrap();
  for (line,text) in [&a[4]].iter().enumerate(){
   let width=r.text_width(text,Some(family),size,&[(WGHT,weight)]);assert!(width<1400.0,"Text too wide {i} {width}");
   let mut c=Canvas::new(W as f64,H as f64);c.background(Color{r:0,g:0,b:0,a:0});c.fill(ink).font(family).font_variation("wght",weight).font_size(size).text(text,88.0,H as f64-y-280.0-line as f64*136.0);
   let mut pixels=r.render_frames(&c).remove(0).0;let mut count=0;
   for (j,p) in pixels.chunks_exact_mut(4).enumerate(){if p[3]!=0{count+=1;let x=(j%W as usize)as f64;let py=(j/W as usize)as f64;assert!(x>=64.0&&x<1536.0&&py>y+44.0&&py<y+334.0,"Ink leaves panel {i} ({x},{py})");}p[0]=ink.r;p[1]=ink.g;p[2]=ink.b;}
   assert!(count>0);page.image_rgba(pixels,W,H,0.0,0.0,1.0);
  }
 }
 renderer.render_to_png(&page,"out.png").unwrap();
}
