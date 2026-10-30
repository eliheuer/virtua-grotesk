'use strict';
const $=id=>document.getElementById(id);
const presets={he:['ה','He · U+05D4'],het:['ח','Het · U+05D7'],tav:['ת','Tav · U+05EA'],group:['החת','He, Het and Tav'],words:['היה חיה תחיה','Words'],marks:['הָ חַ תֵ הּ חִ תַ','Marks'],latin:['no HO החת','Latin and Hebrew']};
let mode='compare',before=false,loaded=false;
const data=window.REVIEW_DATA;
const proof=$('proof');
function element(tag,text,className){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(className)e.className=className;return e;}
function activeText(){return $('sample').value==='custom'?$('custom').value:presets[$('sample').value][0];}
function roles(){return $('references').checked?['before','after','rubik','noto']:['before','after'];}
function specimen(role,text,size){
 const box=element('div',undefined,'sample-viewport');
 const missing=[...new Set([...text].map(c=>c.codePointAt(0)))].filter(cp=>!data.fonts[role].codepoints.includes(cp)&&![10,13,9].includes(cp));
 if(missing.length){box.append(element('p','Not rendered: this font lacks '+missing.map(cp=>'U+'+cp.toString(16).toUpperCase().padStart(4,'0')).join(', ')+'.','missing'));return box;}
 const line=element('div',text,'sample-line');line.style.fontFamily=`Review-${role}`;line.style.fontSize=size+'px';line.lang='he';line.dir='auto';box.append(line);return box;
}
function panel(role,text,sizes){
 const p=element('article',undefined,'font-panel');p.append(element('h2',data.fonts[role].family),element('p',data.fonts[role].label,'role'));
 for(const size of sizes){if(sizes.length>1)p.append(element('p',`${size} px`,'waterfall-size'));p.append(specimen(role,text,size));}
 return p;
}
function render(){
 const size=Math.max(16,Math.min(320,Number($('size').value)||128));const weight=Number($('weight').value);
 document.documentElement.style.setProperty('--size',size+'px');document.documentElement.style.setProperty('--weight',weight);
 document.body.classList.toggle('dark',$('dark').checked);document.body.classList.toggle('grid',$('grid').checked);
 $('custom-wrap').hidden=$('sample').value!=='custom';$('switch-tools').hidden=mode!=='switch';$('references').disabled=mode==='switch';$('size').disabled=mode==='waterfall';
 $('sample-label').textContent=$('sample').value==='custom'?'Your Text':presets[$('sample').value][1];
 $('scale-label').textContent=(mode==='waterfall'?'24, 32, 48, 72, 96 px':size+' px')+' · Weight '+weight;
 document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===mode)));
 if(!loaded)return;
 proof.replaceChildren();proof.classList.toggle('with-references',$('references').checked&&mode!=='switch');
 if(mode==='switch'){
  const p=panel(before?'before':'after',activeText(),[size]);p.classList.add('switch-panel');proof.append(p);$('flip').textContent=before?'Show Applied':'Show Before';
 }else{for(const role of roles())proof.append(panel(role,activeText(),mode==='waterfall'?[24,32,48,72,96]:[size]));}
 requestAnimationFrame(()=>{
  let overflow=false;
  for(const box of proof.querySelectorAll('.sample-viewport'))if(box.scrollWidth>box.clientWidth+1){overflow=true;box.tabIndex=0;box.setAttribute('aria-label','Scroll horizontally to inspect the full sample');}
  $('overflow-note').hidden=!overflow;
 });
}
for(const id of ['sample','weight','references','dark','grid'])$(id).addEventListener('change',render);
$('size').addEventListener('input',render);$('size').addEventListener('change',()=>{$('size').value=Math.max(16,Math.min(320,Number($('size').value)||128));render();});$('custom').addEventListener('input',render);
document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.mode;render();}));
function flip(){before=!before;render();}$('flip').addEventListener('click',flip);
document.addEventListener('keydown',event=>{if(mode==='switch'&&event.key.toLowerCase()==='b'&&!['INPUT','TEXTAREA','SELECT'].includes(event.target.tagName)&&!event.metaKey&&!event.ctrlKey&&!event.altKey){event.preventDefault();flip();}});
async function loadFonts(){
 try{
  await Promise.all(Object.entries(data.fonts).map(async([role,font])=>{
   const response=await fetch(font.url);if(!response.ok)throw new Error(`${font.family}: HTTP ${response.status}`);
   const bytes=await response.arrayBuffer();const hash=[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(b=>b.toString(16).padStart(2,'0')).join('');
   if(hash!==font.sha256)throw new Error(`${font.family}: font hash differs from the review snapshot`);
   const face=new FontFace(`Review-${role}`,bytes,{weight:'400 700',style:'normal'});await face.load();document.fonts.add(face);
  }));
  for(const [role,font] of Object.entries(data.fonts)){const p=element('p');p.append(element('strong',`${font.family} · ${font.label}`),element('br'),element('code',font.sha256));$('font-info').append(p);}
  loaded=true;proof.classList.add('ready');proof.setAttribute('aria-busy','false');$('status').textContent='';render();
 }catch(error){$('status').textContent='Font verification failed. '+error.message+'. Proofs are hidden to avoid showing fallback fonts.';proof.setAttribute('aria-busy','false');}
}
render();loadFonts();
