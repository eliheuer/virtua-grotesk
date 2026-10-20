'use strict';
const $ = id => document.getElementById(id);
const glyphs = [
  {key: 'he', char: 'ה', name: 'He'}, {key: 'het', char: 'ח', name: 'Het'}, {key: 'tav', char: 'ת', name: 'Tav'}
];
const codepoint = char => 'U+' + char.codePointAt(0).toString(16).toUpperCase().padStart(4, '0');
const glyphLabel = glyph => `${glyph.char} (${glyph.name}) · ${codepoint(glyph.char)}`;
const presets = {
  ...Object.fromEntries(glyphs.map(glyph => [glyph.key, [glyph.char, glyphLabel(glyph)]])),
  group: ['החת', 'He, Het and Tav'], words: ['היה חיה תחיה', 'Words'],
  marks: ['הָ חַ תֵ הּ חִ תַ', 'Marks'], latin: ['no HO החת', 'Latin and Hebrew']
};
const data = window.REVIEW_DATA;
const proof = $('proof');
// Measurement only: all visible lettering remains native DOM text.
const inkContext = document.createElement('canvas').getContext('2d');
const spacingUnit = () => parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--space'));
const horizontalInset = () => spacingUnit() / 4;
let mode = 'compare', before = false, loaded = false, alignmentFrame;
let glyphSize = 128, readingSize = 24;
const clamp = (value, min, max, fallback) => Math.max(min, Math.min(max, Number(value) || fallback));
function element(tag, text, className) {
  const e = document.createElement(tag);
  if (text !== undefined) e.textContent = text;
  if (className) e.className = className;
  return e;
}
function labelGlyphs() {
  $('study-title').replaceChildren();
  for (const glyph of glyphs) {
    const identity = element('span', undefined, 'glyph-identity');
    const name = element('span', undefined, 'glyph-name');
    const letter = element('bdi', glyph.char); letter.dir = 'rtl'; letter.lang = 'he';
    name.append(letter, document.createTextNode(` (${glyph.name})`));
    identity.append(name, element('span', codepoint(glyph.char), 'glyph-unicode'));
    $('study-title').append(identity);
    document.querySelector(`#sample option[value=${glyph.key}]`).textContent = glyphLabel(glyph);
  }
  document.querySelector('#sample option[value=group]').textContent = 'ה ח ת (He, Het and Tav)';
}
// A single grid-aligned picker fronts the glyph and reading sample values.
let pickerIndex = 0;
const pickerSource = () => mode === 'reading' ? $('reading-sample') : $('sample');
function closePicker(restoreFocus = false) {
  $('sample-menu').hidden = true;
  $('sample-trigger').setAttribute('aria-expanded', 'false');
  if (restoreFocus) $('sample-trigger').focus();
}
function highlightOption(index) {
  const options = [...$('sample-menu').children];
  pickerIndex = Math.max(0, Math.min(options.length - 1, index));
  options.forEach((option, i) => option.classList.toggle('active', i === pickerIndex));
  $('sample-menu').setAttribute('aria-activedescendant', options[pickerIndex].id);
  options[pickerIndex].scrollIntoView({block: 'nearest'});
}
function syncPicker() {
  closePicker();
  const source = pickerSource();
  $('sample-value').textContent = source.selectedOptions[0].textContent;
  $('sample-menu').replaceChildren(...[...source.options].map((item, i) => {
    const option = element('div', item.textContent, 'picker-option');
    option.id = 'sample-option-' + i;
    option.setAttribute('role', 'option');
    option.setAttribute('aria-selected', String(item.selected));
    option.addEventListener('pointermove', () => highlightOption(i));
    option.addEventListener('click', () => chooseOption(i));
    return option;
  }));
  $('sample-menu').removeAttribute('aria-activedescendant');
}
function openPicker(last = false) {
  $('sample-menu').hidden = false;
  $('sample-trigger').setAttribute('aria-expanded', 'true');
  $('sample-menu').focus();
  highlightOption(last ? pickerSource().options.length - 1 : pickerSource().selectedIndex);
}
function chooseOption(index) {
  pickerSource().selectedIndex = index;
  closePicker(true);
  render();
}
$('sample-trigger').addEventListener('click', () => $('sample-menu').hidden ? openPicker() : closePicker());
$('sample-trigger').addEventListener('keydown', event => {
  if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
    event.preventDefault(); openPicker(event.key === 'End');
    if (event.key === 'Home') highlightOption(0);
  }
});
$('sample-menu').addEventListener('keydown', event => {
  if (['ArrowDown', 'ArrowUp', 'Home', 'End', 'Enter', ' ', 'Escape'].includes(event.key)) event.preventDefault();
  if (event.key === 'ArrowDown') highlightOption(pickerIndex + 1);
  else if (event.key === 'ArrowUp') highlightOption(pickerIndex - 1);
  else if (event.key === 'Home') highlightOption(0);
  else if (event.key === 'End') highlightOption(pickerSource().options.length - 1);
  else if (['Enter', ' '].includes(event.key)) chooseOption(pickerIndex);
  else if (event.key === 'Escape') closePicker(true);
  else if (event.key === 'Tab') closePicker();
  else if (event.key.length === 1 && !event.metaKey && !event.ctrlKey && !event.altKey) {
    const options = [...pickerSource().options];
    const index = options.findIndex((_, offset) => options[(pickerIndex + 1 + offset) % options.length].textContent.toLowerCase().startsWith(event.key.toLowerCase()));
    if (index >= 0) highlightOption((pickerIndex + 1 + index) % options.length);
  }
});
document.addEventListener('pointerdown', event => {
  if (!event.target.closest('.sample-picker')) closePicker();
});
document.querySelector('.sample-picker').addEventListener('focusout', event => {
  if (!event.currentTarget.contains(event.relatedTarget)) closePicker();
});
function resizeCustomEditor() {
  if ($('custom-wrap').hidden) return;
  const editor = $('custom');
  editor.style.height = 'auto';
  const style = getComputedStyle(editor);
  const border = parseFloat(style.borderTopWidth) + parseFloat(style.borderBottomWidth);
  // Grow on the spacing grid; CSS caps long passages and enables scrolling.
  editor.style.height = Math.ceil((editor.scrollHeight + border) / spacingUnit()) * spacingUnit() + 'px';
}
let editorWidth = 0;
new ResizeObserver(entries => {
  const width = entries[0].contentRect.width;
  if (width !== editorWidth) { editorWidth = width; resizeCustomEditor(); }
}).observe($('custom-wrap'));
function readingParagraphs() {
  return $('reading-sample').value === 'custom'
    ? $('custom').value.split(/\n\s*\n/).map(text => ({lang: 'he', dir: 'auto', runs: [{text}]}))
    : data.reading[$('reading-sample').value].paragraphs;
}
function activeText() {
  if (mode === 'reading') return readingParagraphs().map(p => p.runs.map(r => r.text).join('')).join('\n\n');
  return $('sample').value === 'custom' ? $('custom').value : presets[$('sample').value][0];
}
function roles() {
  const virtua = mode === 'switch' ? [before ? 'before' : 'after'] : ['before', 'after'];
  return $('references').checked ? [...virtua, 'rubik', 'noto'] : virtua;
}
function specimen(role, text, size) {
  const box = element('div', undefined, 'sample-viewport');
  box.dir = 'auto';
  const missing = [...new Set([...text].map(c => c.codePointAt(0)))].filter(cp => !data.fonts[role].codepoints.includes(cp) && ![10, 13, 9].includes(cp));
  if (missing.length) {
    box.append(element('p', 'Not rendered: missing ' + missing.map(cp => 'U+' + cp.toString(16).toUpperCase().padStart(4, '0')).join(', ') + '.', 'missing'));
    return box;
  }
  const line = element('div', undefined, 'sample-line');
  line.style.fontFamily = `Review-${role}`;
  line.style.fontSize = size + 'px';
  line.lang = 'he'; line.dir = 'auto';
  const marker = element('span', undefined, 'baseline-mark'); marker.setAttribute('aria-hidden', 'true');
  line.append(marker, document.createTextNode(text)); box.append(line);
  return box;
}
function panel(role, text, size) {
  const panel = element('article', undefined, 'font-panel'); panel.dataset.role = role;
  const caption = element('header', undefined, 'font-caption');
  const label = ['before', 'after'].includes(role) ? data.fonts[role].label : data.fonts[role].family;
  caption.append(element('h2', label));
  panel.append(caption, specimen(role, text, size));
  return panel;
}
function readingPanel(role, size) {
  const card = panel(role, '', size);
  card.querySelector('.sample-viewport').remove();
  const body = element('div', undefined, 'reading-body');
  body.style.fontFamily = `Review-${role}`; body.style.fontSize = size + 'px';
  const missing = [...new Set([...activeText()].map(c => c.codePointAt(0)))].filter(cp => !data.fonts[role].codepoints.includes(cp) && ![10, 13, 9].includes(cp));
  if (missing.length) body.append(element('p', 'Not rendered: missing ' + missing.map(cp => 'U+' + cp.toString(16).toUpperCase()).join(', ') + '.', 'missing'));
  else readingParagraphs().forEach((paragraph, index) => {
    const p = element('p'); p.lang = paragraph.lang; p.dir = paragraph.dir;
    if (index === 0) { const marker = element('span', undefined, 'baseline-mark'); marker.setAttribute('aria-hidden', 'true'); p.append(marker); }
    for (const run of paragraph.runs) {
      if (run.dir || (run.lang && run.lang !== paragraph.lang)) {
        const isolated = element('bdi', run.text); isolated.dir = run.dir || 'auto'; isolated.lang = run.lang; p.append(isolated);
      } else p.append(document.createTextNode(run.text));
    }
    body.append(p);
  });
  card.append(body); return card;
}
function alignReading(row) {
  const bodies = [...row.querySelectorAll('.reading-body')], unit = spacingUnit();
  const metrics = bodies.map(body => {
    const marker = body.querySelector('.baseline-mark'), first = body.querySelector('p');
    body.style.paddingTop = unit + 'px'; first.style.marginTop = '0px';
    if (!marker) return null;
    const style = getComputedStyle(body);
    inkContext.font = `${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
    inkContext.direction = first.dir === 'ltr' ? 'ltr' : 'rtl';
    return {first, offset: marker.getBoundingClientRect().top - first.getBoundingClientRect().top,
      ascent: inkContext.measureText(first.textContent).actualBoundingBoxAscent};
  });
  const ascent = Math.max(0, ...metrics.filter(Boolean).map(m => m.ascent));
  metrics.forEach(metric => { if (metric) metric.first.style.marginTop = (ascent - metric.offset) + 'px'; });
}

function measureRun(role, text, size) {
  const probe = element('div', text, 'sample-line');
  probe.setAttribute('aria-hidden', 'true');
  Object.assign(probe.style, {fontFamily: `Review-${role}`, fontSize: size + 'px',
    position: 'fixed', visibility: 'hidden', whiteSpace: 'pre', width: 'max-content', minWidth: '0'});
  probe.dir = 'auto'; document.body.append(probe);
  const width = probe.getBoundingClientRect().width; probe.remove();
  return width;
}
function fittedSize(row) {
  // Measure at one em, then grow or shrink to the narrowest available column.
  // The fixed-size control is independent; it must not cap automatic fitting.
  const measureSize = 1024;
  const panels = [...row.querySelectorAll('.font-panel')];
  const measurements = panels.filter(panel => panel.querySelector('.sample-line')).map(panel => {
    let width = measureRun(panel.dataset.role, activeText(), measureSize);
    // Keep B switching stable even when the two revisions have different advances.
    if (mode === 'switch' && ['before', 'after'].includes(panel.dataset.role)) {
      width = Math.max(width, measureRun(panel.dataset.role === 'before' ? 'after' : 'before', activeText(), measureSize));
    }
    // Fractional widths matter: clientWidth rounding can wrap a fitted glyph.
    return {available: panel.getBoundingClientRect().width - horizontalInset(), width};
  });
  const measured = measurements.filter(m => m.width > 0);
  const fitted = measured.length
    ? Math.max(16, Math.floor(measureSize * Math.min(...measured.map(m => Math.max(0, m.available) / m.width))))
    : 128;
  return fitted;
}
function fitSamples(row) {
  const fitted = fittedSize(row);
  row.querySelectorAll('.sample-line').forEach(line => { line.style.fontSize = fitted + 'px'; });
  $('fitted-size').textContent = fitted;
  $('scale-label').textContent = 'Fit · ' + fitted + ' px · Weight ' + $('weight').value;
}
function waterfallPanel(role) {
  const card = panel(role, activeText(), 128);
  card.querySelector('.sample-viewport').remove();
  const stack = element('div', undefined, 'waterfall-stack');
  stack.append(specimen(role, activeText(), 128));
  card.append(stack);
  return card;
}
function alignCaptions(row) {
  const captions = [...row.querySelectorAll('.font-caption')];
  captions.forEach(caption => { caption.style.height = ''; });
  const height = Math.max(0, ...captions.map(caption => caption.getBoundingClientRect().height));
  captions.forEach(caption => { caption.style.height = height + 'px'; });
}
function alignWaterfall(row) {
  const largest = fittedSize(row);
  // Eight optical steps, largest first. Collapse duplicate sizes in narrow runs.
  const sizes = [...new Set(Array.from({length: 8}, (_, i) =>
    Math.max(16, Math.floor(largest * Math.pow(16 / largest, i / 7)))))];
  row.dataset.sizes = sizes.join(',');
  const panels = [...row.querySelectorAll('.font-panel')];
  for (const card of panels) {
    const stack = card.querySelector('.waterfall-stack');
    if (stack.children.length !== sizes.length) {
      stack.replaceChildren(...sizes.map(size => specimen(card.dataset.role, activeText(), size)));
    }
    [...stack.children].forEach((box, i) => {
      const line = box.querySelector('.sample-line');
      if (line) line.style.fontSize = sizes[i] + 'px';
    });
  }
  alignCaptions(row);
  let overflow = false;
  sizes.forEach((_, i) => {
    const boxes = panels.map(card => card.querySelector('.waterfall-stack').children[i]);
    overflow = alignSampleBoxes(boxes, spacingUnit() / (i === 0 ? 1 : 2),
      spacingUnit() / (i === sizes.length - 1 ? 1 : 2)) || overflow;
  });
  return overflow;
}
function alignSampleBoxes(boxes, beforeSpace = spacingUnit(), afterSpace = spacingUnit()) {
  let overflow = false;
  const samples = boxes.map(box => {
    const line = box.querySelector('.sample-line');
    box.style.height = ''; if (!line) return null;
    line.style.top = '0px';
    const style = getComputedStyle(line);
    box.dir = style.direction;
    inkContext.font = `${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
    inkContext.direction = style.direction;
    const ink = inkContext.measureText(line.textContent.replace(/\n/g, ''));
    const leading = parseFloat(style.lineHeight);
    const lines = Math.max(1, Math.round(line.getBoundingClientRect().height / leading));
    const offset = line.querySelector('.baseline-mark').getBoundingClientRect().top - line.getBoundingClientRect().top;
    return {line, offset, ascent: ink.actualBoundingBoxAscent,
      descent: ink.actualBoundingBoxDescent + (lines - 1) * leading};
  });
  const ascent = Math.max(0, ...samples.filter(Boolean).map(s => s.ascent));
  const descent = Math.max(0, ...samples.filter(Boolean).map(s => s.descent));
  boxes.forEach((box, index) => {
    const sample = samples[index];
    if (sample) {
      sample.line.style.top = (beforeSpace + ascent - sample.offset) + 'px';
      box.style.height = (beforeSpace + afterSpace + ascent + descent) + 'px';
      box.dataset.inkTop = beforeSpace + ascent - sample.ascent;
      box.dataset.inkBottom = afterSpace + descent - sample.descent;
      box.dataset.commonBaseline = beforeSpace + ascent;
    }
    const clipped = box.scrollWidth > box.clientWidth + 1;
    if (clipped) { overflow = true; box.tabIndex = 0; box.setAttribute('aria-label', 'Scroll sample horizontally; comparisons scroll together'); }
    else { box.removeAttribute('tabindex'); box.removeAttribute('aria-label'); }
  });
  return overflow;
}
function alignSamples() {
  let overflow = false;
  for (const row of proof.querySelectorAll('.comparison-grid')) {
    if (mode === 'waterfall') { overflow = alignWaterfall(row) || overflow; continue; }
    if (mode !== 'reading' && $('fit').checked) fitSamples(row);
    alignCaptions(row);
    if (mode === 'reading') { alignReading(row); continue; }
    overflow = alignSampleBoxes([...row.querySelectorAll('.sample-viewport')]) || overflow;
  }
  $('overflow-note').hidden = !overflow;
}
function scheduleAlignment() { cancelAnimationFrame(alignmentFrame); alignmentFrame = requestAnimationFrame(alignSamples); }
function syncScroll(row) {
  let synchronizing = false;
  for (const box of row.querySelectorAll('.sample-viewport')) box.addEventListener('scroll', () => {
    if (synchronizing) return;
    synchronizing = true;
    for (const other of row.querySelectorAll('.sample-viewport')) if (other !== box) other.scrollLeft = box.scrollLeft;
    requestAnimationFrame(() => { synchronizing = false; });
  });
}
function render() {
  const reading = mode === 'reading';
  $('size').max = $('size-slider').max = reading ? 72 : 320;
  const size = clamp($('size').value, 16, reading ? 72 : 320, reading ? 24 : 128), weight = clamp($('weight').value, 400, 700, 400);
  $('size-slider').value = size; $('weight-slider').value = weight;
  document.documentElement.style.setProperty('--weight', weight);
  document.body.classList.toggle('dark', $('dark').checked);
  document.body.classList.toggle('grid', $('grid').checked);
  document.body.classList.toggle('size-study', mode === 'waterfall');
  document.body.classList.toggle('reading', reading);
  $('sample-title').htmlFor = 'sample-trigger';
  syncPicker();
  const fitting = $('fit').checked && mode !== 'waterfall' && !reading;
  document.body.classList.toggle('fit', fitting);
  $('fitted-size').hidden = !fitting;
  $('fit').disabled = mode === 'waterfall' || reading;
  $('custom-wrap').hidden = (reading ? $('reading-sample').value : $('sample').value) !== 'custom';
  resizeCustomEditor();
  $('switch-tools').hidden = mode !== 'switch';
  $('toggle-hint').hidden = mode !== 'switch';
  $('size').disabled = $('size-slider').disabled = mode === 'waterfall';
  $('sample-label').textContent = reading
    ? ($('reading-sample').value === 'custom' ? 'Your Text' : data.reading[$('reading-sample').value].label)
    : ($('sample').value === 'custom' ? 'Your Text' : presets[$('sample').value][1]);
  $('scale-label').textContent = (mode === 'waterfall' ? 'Responsive waterfall' : size + ' px') + ' · Weight ' + weight + (reading ? ' · Line spacing 1.5' : '');
  document.querySelectorAll('[data-mode]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.mode === mode)));
  $('show-before').setAttribute('aria-pressed', String(before)); $('show-after').setAttribute('aria-pressed', String(!before));
  if (!loaded) return;
  proof.replaceChildren();
  const selectedRoles = roles();
  if (reading) {
    const row = element('div', undefined, 'comparison-grid reading-grid');
    row.style.setProperty('--columns', selectedRoles.length);
    selectedRoles.forEach(role => row.append(readingPanel(role, size)));
    proof.append(row); scheduleAlignment(); return;
  }
  if (mode === 'waterfall') {
    const row = element('div', undefined, 'comparison-grid waterfall-grid');
    row.style.setProperty('--columns', selectedRoles.length);
    selectedRoles.forEach(role => row.append(waterfallPanel(role)));
    proof.append(row); scheduleAlignment(); return;
  }
  for (const rowSize of [size]) {
    const section = element('section', undefined, 'proof-row');
    const row = element('div', undefined, 'comparison-grid');
    row.style.setProperty('--columns', selectedRoles.length);
    row.dataset.size = rowSize;
    row.classList.toggle('single', selectedRoles.length === 1);
    row.classList.toggle('switch-references', mode === 'switch' && selectedRoles.length === 3);
    for (const role of selectedRoles) row.append(panel(role, activeText(), rowSize));
    section.append(row); proof.append(section); syncScroll(row);
  }
  scheduleAlignment();
}
for (const id of ['sample', 'reading-sample', 'references', 'dark', 'grid', 'fit']) $(id).addEventListener('change', render);
for (const [id, min, max, fallback] of [['size', 16, 320, 128], ['weight', 400, 700, 400]]) {
  $(id).addEventListener('input', render);
  $(id).addEventListener('change', () => { $(id).value = clamp($(id).value, min, Number($(id).max) || max, fallback); render(); });
  $(id + '-slider').addEventListener('input', () => { $(id).value = $(id + '-slider').value; render(); });
}
$('custom').addEventListener('input', render);
document.querySelectorAll('[data-mode]').forEach(button => button.addEventListener('click', () => { if (mode === 'reading') readingSize = clamp($('size').value, 16, 72, 24);
  else glyphSize = clamp($('size').value, 16, 320, 128);
  mode = button.dataset.mode; $('size').value = mode === 'reading' ? readingSize : glyphSize; render(); }));
$('show-before').addEventListener('click', () => { before = true; render(); });
$('show-after').addEventListener('click', () => { before = false; render(); });
document.addEventListener('keydown', event => {
  if (mode === 'switch' && event.key.toLowerCase() === 'b' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(event.target.tagName) && !event.target.closest('.sample-picker') && !event.metaKey && !event.ctrlKey && !event.altKey) {
    event.preventDefault(); before = !before; render();
  }
});
new ResizeObserver(scheduleAlignment).observe(proof);
async function loadFonts() {
  try {
    await Promise.all(Object.entries(data.fonts).map(async ([role, font]) => {
      const response = await fetch(font.url);
      if (!response.ok) throw new Error(`${font.family}: HTTP ${response.status}`);
      const bytes = await response.arrayBuffer();
      const hash = [...new Uint8Array(await crypto.subtle.digest('SHA-256', bytes))].map(b => b.toString(16).padStart(2, '0')).join('');
      if (hash !== font.sha256) throw new Error(`${font.family}: font hash differs from the review snapshot`);
      const face = new FontFace(`Review-${role}`, bytes, { weight: '400 700', style: 'normal' });
      await face.load(); document.fonts.add(face);
    }));
    for (const font of Object.values(data.fonts)) {
      const p = element('p'); p.append(element('strong', `${font.family} · ${font.label}`), element('br'), element('code', font.sha256)); $('font-info').append(p);
    }
    loaded = true; proof.classList.add('ready'); proof.setAttribute('aria-busy', 'false'); $('status').textContent = ''; render();
  } catch (error) {
    $('status').textContent = 'Font verification failed. ' + error.message + '. Proofs are hidden to avoid showing fallback fonts.';
    proof.setAttribute('aria-busy', 'false');
  }
}
labelGlyphs(); render(); loadFonts();
