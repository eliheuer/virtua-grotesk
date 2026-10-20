"""Fixed-page modular layout shared by reference and revision proofs.

1600 x 1280; margin 80; unit 40. Glyphs keep their em scale and common origin.
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, MARGIN, UNIT = 1600, 1280, 80, 40
INK, PAPER, RULE, ACCENT = '#444444', '#dedede', '#a8a8a8', '#9b4038'


def label_font(size, bold=False):
    candidates = [('/System/Library/Fonts/Helvetica.ttc', int(bold)),
                  ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else
                   '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 0)]
    for path, index in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size, index=index)
    return ImageFont.load_default(size=size)


def text(draw, xy, value, size=20, bold=False, fill=INK, right=False, limit=None):
    font=label_font(size,bold)
    if limit is not None and draw.textlength(value,font=font)>limit:
        raise ValueError(f'Caption too long for the grid: {value!r}')
    draw.text(xy,value,font=font,fill=fill,anchor='rs' if right else 'ls')


def render_pages(rows, columns, output, title='Type study', subtitle='Shape / spacing / weight',
                 footnote='Equal em scale and baseline. Weight coordinates are not optical matches.',
                 grid=False, folio=None):
    """Rows contain label, images, baseline (inside each image), and optional note."""
    if not rows or not 1<=len(columns)<=4:
        raise ValueError('Use nonempty rows and one to four columns')
    output=Path(output)
    cell=(WIDTH-2*MARGIN)//len(columns)
    if cell%UNIT:
        raise ValueError('Column count must divide the modular grid')
    maximum=cell-UNIT
    for row in rows:
        if len(row['images'])!=len(columns):raise ValueError('Row/column mismatch')
        if any(im.width>maximum for im in row['images']):
            raise ValueError(f"Sample too wide for {maximum}px cell: {row['label']}. Shorten text or choose a smaller explicit size; no auto-fitting.")
    rise=max(row['baseline'] for row in rows)
    descent=max(im.height-row['baseline'] for row in rows for im in row['images'])
    required=math.ceil((rise+80)/UNIT)*UNIT
    if descent>64:required+=math.ceil((descent-64)/UNIT)*UNIT
    per_page=min(3,max(1,720//required))
    if required>720 or descent>80:
        raise ValueError('Sample too tall for this page; choose a smaller explicit size')
    total=math.ceil(len(rows)/per_page)
    if folio and total!=1:raise ValueError("A series folio requires a single-page study")
    paths=[];placements=[]
    for page,start in enumerate(range(0,len(rows),per_page),1):
        chunk=rows[start:start+per_page]
        im=Image.new('RGB',(WIDTH,HEIGHT),PAPER);d=ImageDraw.Draw(im)
        text(d,(MARGIN,120),'VIRTUA GROTESK  /  DESIGN REVIEW',20,fill=ACCENT)
        text(d,(WIDTH-MARGIN,120),folio or f'{page:02d} / {total:02d}',20,right=True)
        text(d,(MARGIN,200),title,64,bold=True,limit=WIDTH-2*MARGIN)
        text(d,(MARGIN,240),subtitle,22,limit=WIDTH-2*MARGIN)
        d.line((MARGIN,280,WIDTH-MARGIN,280),fill=INK,width=2)
        for col,label in enumerate(columns):
            x=MARGIN+col*cell
            text(d,(x,320),label,26,bold=True,limit=cell-20)
            text(d,(x,360),f'{col+1:02d}',18,fill=ACCENT)
        rowheight=720//per_page//UNIT*UNIT
        for index,row in enumerate(chunk):
            top=360+index*rowheight
            text(d,(MARGIN,top+40),row['label'],20,bold=True,limit=1000)
            if row.get('note'):
                text(d,(WIDTH-MARGIN,top+40),row['note'],18,right=True,limit=400)
            baseline=top+rowheight
            for col,panel in enumerate(row['images']):
                x=MARGIN+col*cell
                # Preserve the shared font origin; do not optically realign each font.
                y=baseline-row['baseline']
                if y<top+64:raise ValueError('Glyph collides with its row heading')
                im.paste(panel,(x,y))
                d.line((x,baseline,x+8,baseline),fill=RULE,width=1)
                placements.append({'page':page,'row':start+index,'column':col,'x':x,
                                   'y':y,'baseline':baseline,'width':panel.width,'height':panel.height})
        d.line((MARGIN,1160,WIDTH-MARGIN,1160),fill=RULE,width=1)
        text(d,(MARGIN,1200),footnote,18,limit=WIDTH-2*MARGIN)
        if grid:
            for x in range(MARGIN,WIDTH-MARGIN+1,UNIT):d.line((x,MARGIN,x,HEIGHT-MARGIN),fill='#b8c0c0')
            for y in range(MARGIN,HEIGHT-MARGIN+1,UNIT):d.line((MARGIN,y,WIDTH-MARGIN,y),fill='#b8c0c0')
        path=output if page==1 else output.with_name(f'{output.stem}-{page:02d}{output.suffix}')
        path.parent.mkdir(parents=True,exist_ok=True);im.save(path);paths.append(str(path))
    return {'pages':paths,'page_size':[WIDTH,HEIGHT],'margin':MARGIN,'unit':UNIT,
            'folio':folio, 'columns':columns,'placements':placements,'grid_overlay':grid,
            'label_typeface':label_font(20).getname(),'title':title,'subtitle':subtitle}
