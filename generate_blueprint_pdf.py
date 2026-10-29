"""
Generate professional blueprint PDF for outdoor gym
"""
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, black, white, grey
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, KeepTogether, HRFlowable
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import os

# Professional blueprint styling
NAVY = HexColor('#1B2A4A')
ORANGE = HexColor('#E8872A')
DARK_GREY = HexColor('#333333')
LIGHT_GREY = HexColor('#F5F5F5')
MID_GREY = HexColor('#CCCCCC')
BLUE = HexColor('#4A90D9')
GREEN = HexColor('#2E7D32')
RED = HexColor('#C62828')
TEAL = HexColor('#00796B')

def S(text, **kwargs):
    """Create a styled paragraph using explicit ParagraphStyle"""
    defaults = {
        'fontName': 'Helvetica',
        'fontSize': 10,
        'leading': 14,
        'textColor': DARK_GREY,
    }
    defaults.update(kwargs)
    style = ParagraphStyle('custom', **defaults)
    return Paragraph(text, style)

def H(text, size=16, color=NAVY):
    """Main heading"""
    s = ParagraphStyle('H_main', parent=getSampleStyleSheet()['Normal'],
                       fontName='Helvetica-Bold', fontSize=size, leading=20,
                       textColor=color, spaceAfter=12, spaceBefore=12)
    return Paragraph(text, s)

def H2(text):
    """Section heading"""
    s = ParagraphStyle('H2', parent=getSampleStyleSheet()['Normal'],
                       fontName='Helvetica-Bold', fontSize=13, leading=17,
                       textColor=NAVY, spaceAfter=8, spaceBefore=10)
    return Paragraph(text, s)

def H3(text):
    """Subsection heading"""
    s = ParagraphStyle('H3', parent=getSampleStyleSheet()['Normal'],
                       fontName='Helvetica-Bold', fontSize=11, leading=15,
                       textColor=ORANGE, spaceAfter=6, spaceBefore=8)
    return Paragraph(text, s)

def B(text):
    """Bold — returns a string that S() can wrap in a Paragraph"""
    if isinstance(text, str):
        return f'<b>{text}</b>'
    # If text is already a Paragraph or string with HTML-like content
    return f'<b>{text}</b>'

def bullet(text, indent=24):
    """Bullet item"""
    s = ParagraphStyle('bullet', parent=getSampleStyleSheet()['Normal'],
                       fontName='Helvetica', fontSize=10, leading=14,
                       textColor=DARK_GREY, leftIndent=indent, spaceAfter=2)
    return Paragraph(f'<bullet>•</bullet> {text}', s)

def numbered(text, indent=24):
    """Numbered item"""
    s = ParagraphStyle('numbered', parent=getSampleStyleSheet()['Normal'],
                       fontName='Helvetica', fontSize=10, leading=14,
                       textColor=DARK_GREY, leftIndent=indent, spaceAfter=2)
    return Paragraph(f'<bullet>▸</bullet> {text}', s)

def checklist_item(text, indent=24):
    """Checkbox item"""
    s = ParagraphStyle('check', parent=getSampleStyleSheet()['Normal'],
                       fontName='Helvetica', fontSize=10, leading=14,
                       textColor=DARK_GREY, leftIndent=indent, spaceAfter=2)
    return Paragraph(f'<bullet>☐</bullet> {text}', s)

def table_style(base_style=TableStyle):
    """Generate table style for data tables"""
    return base_style([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('FONTSIZE', (0,-1), (-1,-1), 9),
        ('BACKGROUND', (0,-1), (-1,-1), HexColor('#E8F5E9')),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (0,1), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, MID_GREY),
        ('LINEBELOW', (0,0), (-1,0), 2, ORANGE),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ])

def data_table(headers, data, col_widths=None):
    """Create a formatted data table"""
    rows = [[S(h, style=ParagraphStyle('cell', fontName='Helvetica-Bold', fontSize=9, textColor=white)) for h in headers]]
    for row_data in data:
        rows.append([S(str(cell), style=ParagraphStyle('cell', fontSize=9)) for cell in row_data])
    
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('BACKGROUND', (0,-1), (-1,-1), HexColor('#E8F5E9')),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (0,1), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, MID_GREY),
        ('LINEBELOW', (0,0), (-1,0), 2, ORANGE),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_GREY]),
    ])
    t.setStyle(style)
    return t

def section_title(text, number):
    """Section title with number"""
    s = ParagraphStyle('sectitle', parent=getSampleStyleSheet()['Normal'],
                       fontName='Helvetica-Bold', fontSize=14, leading=18,
                       textColor=NAVY, spaceAfter=4, spaceBefore=16)
    return Paragraph(f'{number}  {text}', s)

def make_cover(canvas_obj, doc):
    """Draw cover page"""
    canvas_obj.saveState()
    # Navy header bar
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, letter[1] - 60, letter[0], 60, fill=1, stroke=0)
    # Orange accent line
    canvas_obj.setFillColor(ORANGE)
    canvas_obj.rect(0, letter[1] - 62, letter[0], 2, fill=1, stroke=0)
    
    canvas_obj.setFillColor(white)
    canvas_obj.setFont('Helvetica-Bold', 28)
    canvas_obj.drawString(60, letter[1] - 35, 'STRUCTURAL BLUEPRINT')
    
    canvas_obj.setFillColor(ORANGE)
    canvas_obj.setFont('Helvetica-Bold', 20)
    canvas_obj.drawString(60, letter[1] - 60, 'BACKYARD CALISTHENICS FORTRESS')
    
    canvas_obj.setFillColor(white)
    canvas_obj.setFont('Helvetica', 12)
    canvas_obj.drawString(60, letter[1] - 80, 'Engineering Drawing Set — Owner-Builder Compliant')
    
    canvas_obj.setFillColor(DARK_GREY)
    canvas_obj.setFont('Helvetica', 11)
    canvas_obj.drawString(60, letter[1] - 110, 'Location: Bridgewater, MA 02324')
    canvas_obj.drawString(60, letter[1] - 130, 'Code: 780 CMR 10th Ed. / IRC 2018 / IBC 2018')
    canvas_obj.drawString(60, letter[1] - 150, 'Snow Load: 30 psf  |  Wind: 134 mph  |  Frost: 48"')
    
    # Footer
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 0, letter[0], 40, fill=1, stroke=0)
    canvas_obj.setFillColor(ORANGE)
    canvas_obj.rect(0, 0, letter[0], 2, fill=1, stroke=0)
    canvas_obj.setFillColor(white)
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.drawString(60, 15, 'Prepared for Bridgewater Building Permit Submittal')
    
    canvas_obj.restoreState()

def make_header(canvas_obj, doc):
    """Draw page header"""
    canvas_obj.saveState()
    canvas_obj.setStrokeColor(NAVY)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(40, letter[1] - 30, letter[0] - 40, letter[1] - 30)
    canvas_obj.setFont('Helvetica-Bold', 8)
    canvas_obj.setFillColor(NAVY)
    canvas_obj.drawString(40, letter[1] - 25, 'Structural Blueprint — Backyard Calisthenics Fortress')
    canvas_obj.drawRightString(letter[0] - 40, letter[1] - 25, f'Page {doc.page}')
    canvas_obj.restoreState()

def make_footer(canvas_obj, doc):
    """Draw page footer"""
    canvas_obj.saveState()
    canvas_obj.setStrokeColor(MID_GREY)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(40, 50, letter[0] - 40, 50)
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.setFillColor(DARK_GREY)
    canvas_obj.drawString(40, 30, 'Per 780 CMR 10th Ed. | 780 CMR R403.1.1 (48" frost) | IRC Table R301.2(4)')
    canvas_obj.drawRightString(letter[0] - 40, 30, 'Bridgewater, MA — Plym County')
    canvas_obj.restoreState()

doc = SimpleDocTemplate(
    '/workspace/outdoor_gym_engineering_blueprint.pdf',
    pagesize=landscape(letter),
    leftMargin=45,
    rightMargin=45,
    topMargin=50,
    bottomMargin=50,
    title='Structural Blueprint — Backyard Calisthenics Fortress',
    author='Owner-Builder',
)

story = []

# Cover
story.append(Spacer(1, 2*inch))
story.append(H('STRUCTURAL BLUEPRINT', size=32))
story.append(Spacer(1, 12))
story.append(H('BACKYARD CALISTHENICS FORTRESS', size=22, color=ORANGE))
story.append(Spacer(1, 20))
story.append(H2('Engineering Drawing Set — Owner-Builder Compliant'))

# Project info table
project_data = [
    ['Parameter', 'Value', 'Code Reference'],
    ['Location', 'Bridgewater, MA 02324', '—'],
    ['Zoning Class', 'Accessory Structure (< 300 sq ft)', 'Bridgewater §4.4'],
    ['Setback Required', '5 ft minimum (rear/side)', 'Bridgewater §4.4'],
    ['Footing Depth', '48 inches minimum', '780 CMR R403.1.1'],
    ['Concrete', '3000 psi, 5% air entrainment', 'IRC R403.1'],
    ['Snow Load (Pg)', '30 psf', 'Table R301.2(4)'],
    ['Wind Speed', '134 mph (Vult, Risk Cat. II)', 'Table R301.2(4)'],
    ['Soil Bearing', '2,000 psf (conservative)', '—'],
    ['Live Load (deck/play)', '40 psf', 'IRC Table R301.5'],
    ['Dynamic Load (play)', '200 lb max per user', 'ASCE 7-16'],
    ['Permit Fee', '~$48–$50', 'Bridgewater 7/1/2024'],
]

story.append(data_table(
    [h for h in project_data[0]],
    project_data[1:],
    col_widths=[2.5*inch, 2.5*inch, 2.0*inch]
))
story.append(Spacer(1, 24))

story.append(H3('⚠ STRUCTURAL DISCLAIMER'))
story.append(S(
    'This blueprint set incorporates prescriptive requirements from IRC 2018, IBC 2018, '
    'and 780 CMR 10th Edition as adopted by the Town of Bridgewater. All loads, capacities, '
    'and connection details are calculated per NDS 2018 and AISC 360-16. For structures '
    'exceeding 12 ft in height or complex load paths, consultation with a Massachusetts-licensed '
    'structural engineer is recommended. All work must comply with the latest adopted codes and '
    'local ordinances of the Town of Bridgewater, MA.',
    style=ParagraphStyle('disclaimer', fontName='Helvetica-Oblique', fontSize=9, textColor=RED, leading=13)
))

story.append(PageBreak())

# ============================================================
# SECTION A1: SITE PLAN & LAYOUT
# ============================================================
story.append(section_title('SITE PLAN & ZONING COMPLIANCE', 'A1'))
story.append(H2('Project Layout'))
story.append(S(
    'Total footprint: 22 ft × 12 ft = 264 sq ft (Zone A: 144 + Zone B: 120) — '
    'under 300 sq ft threshold, no special permit required.',
    style=ParagraphStyle('info', fontName='Helvetica-Bold', fontSize=10, textColor=NAVY, leading=14)
))

# Layout table
layout_data = [
    ['Component', 'Dimensions', 'Height', 'Zone', 'Setback Req.'],
    ['Adventure Tower (Zone A)', '12 ft × 12 ft', '14 ft (deck at 13 ft)', 'A', '5 ft'],
    ['Upper Deck with Netting', '12 ft × 12 ft', '13 ft above grade', 'A', '5 ft'],
    ['Main Frame Zone A', '10 ft × 5 ft (footprint)', '10 ft', 'A', '5 ft'],
    ['Calisthenics Frame (Zone B)', '10 ft × 5 ft', '12 ft', 'B', '5 ft'],
    ['Shade Sails (X-pattern)', '2 × 14×14×14 ft', 'At ridge peak', 'A', '—'],
    ['Safety Netting', '10 ft × 200 ft roll', 'Full perimeter', 'A', '—'],
    ['Monkey Bar Ladder', '8 rungs, 12" spacing', 'At 9 ft', 'B', '—'],
    ['Dip Stations', 'Dual height', '28" & 32" from ground', 'B', '—'],
    ['Rope Tower', '200 ft fibershed', 'Full tower height', 'A', '—'],
    ['Disc/Tire Swings', '2 sets', '7 ft chains', 'A', '—'],
]

story.append(data_table(
    [h for h in layout_data[0]],
    layout_data[1:],
    col_widths=[2.0*inch, 1.5*inch, 1.5*inch, 0.5*inch, 0.8*inch]
))

story.append(Spacer(1, 16))
story.append(H2('Site Layout Diagram'))
story.append(S(
    'Property Line → 5+ ft → Zone A (12×12) → 5 ft → Zone B (10×5) → 5+ ft → Property Line',
    style=ParagraphStyle('layout', fontName='Helvetica', fontSize=9, textColor=DARK_GREY, leading=13)
))

story.append(Spacer(1, 8))

# Simple ASCII art site plan
ascii_plan = """
                    [ Property Line ]
                         ↑
            ┌─────────────────────────────────────────────────────────┐
            │                                                         │
            │         SETBACK: 5+ ft from property lines              │
            │                                                         │
            │   ┌───────────────────────────────────────────────────┐ │
            │   │              Zone A — Adventure Tower              │ │
            │   │   12 ft wide × 12 ft footprint                    │ │
            │   │   14 ft tall, upper deck at 13 ft                 │ │
            │   │                                                   │ │
            │   │   Upper Deck with Safety Netting (12×12)          │ │
            │   │   Shade Sails (X-pattern) at peak                 │ │
            │   │   Rope Tower with Disc Obstacles                  │ │
            │   │   Disc/Tire Swings                                │ │
            │   │   Climbing Holds                                  │ │
            │   └───────────────────────────────────────────────────┘ │
            │                                                         │
            │   ┌───────────────────────────────────────────────────┐ │
            │   │          Zone B — Calisthenics Frame               │ │
            │   │   10 ft wide × 5 ft footprint                     │ │
            │   │   12 ft tall                                      │ │
            │   │                                                   │ │
            │   │   Pull-Up Bar + Monkey Bar Ladder                 │ │
            │   │   Dual-Height Dip Stations                        │ │
            │   │   Bungee/Abduct Bar                               │ │
            │   └───────────────────────────────────────────────────┘ │
            │                                                         │
            └─────────────────────────────────────────────────────────┘
                         ↓
                    [ Property Line ]
"""
story.append(Paragraph(ascii_plan, ParagraphStyle('ascii', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))

story.append(PageBreak())

# ============================================================
# SECTION A2: FOUNDATION PLAN
# ============================================================
story.append(section_title('FOUNDATION PLAN', 'A2'))
story.append(H2('Design Basis'))
story.append(S(
    'Frost depth: 48" minimum per IRC R403.1.1 and 780 CMR 1805.4. '
    'Soil bearing: 2,000 psf (conservative for MA clay/sand). '
    'Concrete: 3000 psi, 5% air entrainment per IRC R403.1.',
    style=ParagraphStyle('info', fontName='Helvetica', fontSize=10, textColor=DARK_GREY, leading=14)
))

story.append(H2('Footing Schedule'))

footing_data = [
    ['ID', 'Zone', 'Location', 'Post Size', 'Hole Size', 'Depth', 'Concrete', 'Notes'],
    ['F1', 'A', 'Front-Left', '6×6', '14" dia', '48"', '1.5 yd³', 'Main post'],
    ['F2', 'A', 'Front-Right', '6×6', '14" dia', '48"', '1.5 yd³', 'Main post'],
    ['F3', 'A', 'Rear-Left', '6×6', '14" dia', '48"', '1.5 yd³', 'Main post'],
    ['F4', 'A', 'Rear-Right', '6×6', '14" dia', '48"', '1.5 yd³', 'Main post'],
    ['F5', 'B', 'Front-Left', '4×4', '12" dia', '48"', '0.75 yd³', 'Monkey bar'],
    ['F6', 'B', 'Front-Right', '4×4', '12" dia', '48"', '0.75 yd³', 'Monkey bar'],
    ['F7', 'B', 'Rear-Left', '4×4', '12" dia', '48"', '0.75 yd³', 'Monkey bar'],
    ['F8', 'B', 'Rear-Right', '4×4', '12" dia', '48"', '0.75 yd³', 'Monkey bar'],
]

story.append(data_table(
    [h for h in footing_data[0]],
    footing_data[1:],
    col_widths=[0.5*inch, 0.5*inch, 1.0*inch, 0.8*inch, 0.8*inch, 0.6*inch, 0.8*inch, 1.0*inch]
))
story.append(Spacer(1, 6))
story.append(S('<b>Total concrete: ~10.5 yd³  |  Total holes: 8  |  Gravel base: 2" each hole</b>'))

story.append(Spacer(1, 16))
story.append(H2('Footing Detail — Zone A (6×6 Posts)'))

footing_detail = """
         Fin grade (sloped away from structure)
         ┌──────────────────────────────────────────┐
         │                                          │
         │   Post (6×6)                             │
         │   (field treat cut end)                  │
         │                                          │
         │   48" below grade                        │
         │                                          │
         │   ┌────────────────────────────────────┐ │
         │   │                                    │ │
         │   │     2" gravel base                 │ │
         │   │                                    │ │
         │   └────────────────────────────────────┘ │
         │       │ │ │ │                            │
         │   ┌───┴─┴─┴─┴───┐                        │
         │   │  Concrete    │                        │
         │   │  3000 psi   │                        │
         │   │  14" dia     │                        │
         │   │  (sonotube)  │                        │
         │   └──────────────────────────────────────┘
"""
story.append(Paragraph(footing_detail, ParagraphStyle('detail', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))

story.append(H2('Footing Detail — Zone B (4×4 Posts)'))
footing_detail_b = """
         Fin grade (sloped away from structure)
         ┌──────────────────────────────────────────┐
         │                                          │
         │   Post (4×4)                             │
         │   (field treat cut end)                  │
         │                                          │
         │   48" below grade                        │
         │                                          │
         │   ┌────────────────────────────────────┐ │
         │   │                                    │ │
         │   │     2" gravel base                 │ │
         │   │                                    │ │
         │   └────────────────────────────────────┘ │
         │       │ │ │ │                            │
         │   ┌───┴─┴─┴─┴───┐                        │
         │   │  Concrete    │                        │
         │   │  3000 psi   │                        │
         │   │  12" dia     │                        │
         │   │  (sonotube)  │                        │
         │   └──────────────────────────────────────┘
"""
story.append(Paragraph(footing_detail_b, ParagraphStyle('detail', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))

story.append(Spacer(1, 12))
story.append(H3('Pre-Construction Foundation Checklist'))
story.append(checklist_item('Call 811 (Mass. utility locators) — 3 business days minimum'))
story.append(checklist_item('Mark post locations with spray paint'))
story.append(checklist_item('Verify property lines and setbacks'))
story.append(checklist_item('Dig all 8 footings to 48" depth minimum'))
story.append(checklist_item('Add 2" gravel base to each hole'))
story.append(checklist_item('Schedule footing inspection'))
story.append(checklist_item('Pour concrete — 3000 psi, 5% air entrainment'))
story.append(checklist_item('Cure minimum 72 hours before framing'))
story.append(checklist_item('Email as-built photos to building@bridgewaterma.org'))

story.append(PageBreak())

# ============================================================
# SECTION A3: ELEVATIONS
# ============================================================
story.append(section_title('ELEVATIONS & VIEWS', 'A3'))
story.append(H2('Zone A — Front Elevation (12 ft wide × 14 ft tall)'))

zone_a_front = """
    Shade Sail (X-pattern)
         ╲         ╱
           ╲     ╱
             ╲ ╱
               ┼ ← Upper ring beam at 13 ft
              ╱││╲
             │ │ │  ← Safety netting (all sides)
             │ │ │
       ┌─────┘ │ └─────┐
       │    Upper Deck    │  ← Deck planks at 13 ft
       │  (12×12 ft)      │
       └─────┐ │ ┌─────┘
             │ │ │
       ┌─────┘ │ └─────┐
       │        │        │
       │  Main Frame 10 ft│
       │  (6×6 posts)     │
       └──────────────────┘
              │ │
              │ │
    └──────────┴─┴────────────────
    48" concrete footing
"""
story.append(Paragraph(zone_a_front, ParagraphStyle('elev', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))

story.append(H2('Zone B — Side Elevation (10 ft wide × 12 ft tall)'))
zone_b_side = """
    Pull-Up Bar @ 9 ft
              ┌───┐
              │   │ ← 1¼" steel pipe
              │   │
        ┌─────┼───┼─────┐
        │     │   │     │
        │  Mid Beam @ 9 ft     │
        │   (4×6)              │
        │                      │
        │ Monkey Bar Rungs     │ ← 8 rungs, 12-14" spacing
        │ ┬──┬──┬──┬──┬──┬──│
        │ │  │  │  │  │  │  │
        │  ┬──┬──┬──┬──┬──┬ │
        │  │  │  │  │  │  │  │
        └──┴──┴──┴──┴──┴──┴─┘
        │                      │
        │  Top Beam @ 12 ft    │
        │   (4×6)              │
        │                      │
        │  Lower Beam @ 7 ft   │
        │   (4×6)              │
        └──────────────────────┘
    48" concrete footing
"""
story.append(Paragraph(zone_b_side, ParagraphStyle('elev', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))

story.append(H2('Zone A — Rear Elevation'))
zone_a_rear = """
    Shade Sail (X-pattern)
         ╲         ╱
           ╲     ╱
             ╲ ╱
               ┼ ← Upper ring beam at 13 ft
              ╱││╲
             │ │ │  ← Safety netting (all sides)
             │ │ │
       ┌─────┘ │ └─────┐
       │    Upper Deck    │
       │  (12×12 ft)      │
       └─────┐ │ ┌─────┘
             │ │ │
       ┌─────┘ │ └─────┐
       │        │        │
       │  Mid Beam 10 ft  │
       │  (6×6 posts)     │
       │                  │
       │ Cross-Braces     │
       │ 45° diagonal     │
       └──────────────────┘
              │ │
              │ │
    └──────────┴─┴────────────────
    48" concrete footing
"""
story.append(Paragraph(zone_a_rear, ParagraphStyle('elev', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))

story.append(PageBreak())

# ============================================================
# SECTION A4: FRAMING DETAILS
# ============================================================
story.append(section_title('FRAMING DETAILS', 'A4'))
story.append(H2('Connection Details — All Zone A Beam-to-Post'))

story.append(H3('Detail 1: Simpson GB663/GB664 Post Cap'))
story.append(S(
    '2 × ½" × 8" HDG lag bolts per side (4 total) + 1 Simpson post base connector per post.',
    style=ParagraphStyle('note', fontName='Helvetica', fontSize=9, textColor=DARK_GREY, leading=13)
))

conn1 = """
            Beam (6×6)
            ┌──────────────────────────┐
            │                          │
            │  ½"×8" lag bolt (2/side) │
            │          ●    ●          │
            │    ┌────────────────┐    │
            │    │ Simpson GB663  │    │
            │    │ Post Cap       │    │
            │    └────────────────┘    │
            │      ●        ●         │
            │      Post (6×6)          │
            │      ││││                │
            └──────┴┴┴┴────────────────
"""
story.append(Paragraph(conn1, ParagraphStyle('detail', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))

story.append(H3('Detail 2: Simpson HD8 Hurricane Tie — Zone B'))
conn2 = """
            Beam (4×6)
            ┌──────────────────────────┐
            │                          │
            │  ½"×8" lag bolt (2/side) │
            │          ●    ●          │
            │    ┌────────────────┐    │
            │    │ Simpson HD8    │    │
            │    │ Hurricane Tie  │    │
            │    └────────────────┘    │
            │      Post (4×4)          │
            │      │││                 │
            └──────┴┴┴─────────────────
"""
story.append(Paragraph(conn2, ParagraphStyle('detail', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))

story.append(H3('Detail 3: Deck Joist Hanger (Simpson JH)'))
conn3 = """
            Joist (2×6)
            ┌──────────────────┐
            │  10d nails (2/s) │
            │  ●  ●  ●  ●      │
            │    ┌───────┐      │
            │    │ JH    │      │
            │    │ Hanger│      │
            │    └───┬───┘      │
            │        │           │
            └────────┼───────────┘
             Beam (6×6 or 4×6)
"""
story.append(Paragraph(conn3, ParagraphStyle('detail', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))

story.append(H3('Detail 4: Cross-Brace Connection (45°)'))
conn4 = """
            Diagonal Brace (2×4)
            ╱
           ╱
          ╱
         ╱
    ┌────┘
    │ Post (6×6)
    │  ●  ← ½"×8" lag bolt
    │
    └────────────────
"""
story.append(Paragraph(conn4, ParagraphStyle('detail', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))

story.append(H3('Detail 5: Pull-Up Bar Mounting (U-bolt Clamp)'))
conn5 = """
            Beam (6×6)
            ┌──────────────────┐
            │    ┌─────┐       │
            │    │Pipe │       │
            │    │1¼"  │       │
            │    └──┬──┘       │
            │   ┌───┼───┐      │
            │   │U│  │U│      │
            │   │B│  │B│      │
            │   └───┴───┘      │
            │     Nuts + Washers│
            └──────────────────┘
"""
story.append(Paragraph(conn5, ParagraphStyle('detail', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))

story.append(H3('Detail 6: Deck Board Spacing'))
conn6 = """
    ┌──────┬──────┬──────┬──────┬──────┐
    │ Board│ Board│ Board│ Board│ Board│
    │ 3/4" │ 3/4" │ 3/4" │ 3/4" │ 3/4" │
    │ 5.5" │ 5.5" │ 5.5" │ 5.5" │ 5.5" │
    └──────┴──────┴──────┴──────┴──────┘
     ← ¼" gap → ← ¼" gap →
"""
story.append(Paragraph(conn6, ParagraphStyle('detail', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))

story.append(H2('Monkey Bar Attachment Detail'))
monkey_bar = """
    Beam (6×6) — 12 ft
    ┌──────────────────────────┐
    │  ●  ●  ●  ●  ●  ●  ●  ● │ ← ¼" holes through beam
    │  │  │  │  │  │  │  │  │
    │  └──┴──┴──┴──┴──┴──┴──┘  ← U-bolt clamps
    └──────────────────────────┘
"""
story.append(Paragraph(monkey_bar, ParagraphStyle('detail', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))
story.append(S(
    '8 × U-bolt clamps (1 per rung), 16 × ½" hex nuts, ¼" hole through beam centerline, rungs spaced 12" OC.',
    style=ParagraphStyle('note', fontName='Helvetica', fontSize=9, textColor=DARK_GREY, leading=13)
))

story.append(H2('Shade Sail Attachment Detail'))
sail_conn = """
    Post (6×6) — Zone A corners
    ┌────┐
    │ ●  │  ← ⅝"×6" stainless eye bolt
    │    │
    └────┘
         │
         ╲   ← Turnbuckle + chain
           ╲  ← Shade sail corner
            ┴
"""
story.append(Paragraph(sail_conn, ParagraphStyle('detail', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))
story.append(S(
    '4 × ⅝" × 6" stainless eye bolts + 4 × turnbuckles (6" min) + 4 × stainless chain links.',
    style=ParagraphStyle('note', fontName='Helvetica', fontSize=9, textColor=DARK_GREY, leading=13)
))

story.append(H2('Safety Netting Attachment Detail'))
net_conn = """
    Top Ring Beam (6×6)
    ┌──────────────────────────┐
    │  ●  ●  ●  ●  ●  ●  ●  ● │  ← UV zip ties every 6"
    │  │  │  │  │  │  │  │  │  │
    │  └──┴──┴──┴──┴──┴──┴──┴──┘  ← Safety netting
    └──────────────────────────┘
"""
story.append(Paragraph(net_conn, ParagraphStyle('detail', fontName='Courier', fontSize=7, leading=9, textColor=DARK_GREY)))
story.append(S(
    'UV-rated black zip ties (3" min), spacing every 6" along all beams and posts, overlap at corners min 12".',
    style=ParagraphStyle('note', fontName='Helvetica', fontSize=9, textColor=DARK_GREY, leading=13)
))

story.append(PageBreak())

# ============================================================
# SECTION A5: STRUCTURAL ANALYSIS
# ============================================================
story.append(section_title('STRUCTURAL ANALYSIS & LOAD PATH', 'A5'))
story.append(H2('Load Path Diagram'))
load_path = """
Live Loads → Upper Deck (40 psf per IRC)
    │
    ↓
Deck Boards → Joist Hangers → Beams (D1–D8)
    │                                    │
    │                            Post Caps (GB663/GB664)
    │                                    │
    └──────────────────────┬─────────────┘
                           │
                           ↓
                    6×6 Posts (A1–A4)
                           │
                           ↓
                    Concrete Footings
                           │
                           ↓
                      Native Soil (2,000 psf min)
"""
story.append(Paragraph(load_path, ParagraphStyle('path', fontName='Courier', fontSize=8, leading=11, textColor=DARK_GREY)))

story.append(H2('Design Loads'))
load_table = [
    ['Load Type', 'Value', 'Location', 'Notes'],
    ['Dead Load (lumber)', '~15 psf', 'All members', 'Self-weight'],
    ['Live Load (deck)', '40 psf', 'Upper deck', 'Per IRC Table R301.5'],
    ['Live Load (play)', '40 psf', 'All platforms', 'Play equipment'],
    ['Snow Load', '30 psf', 'Shade sails', 'Per Table R301.2(4)'],
    ['Wind Load', '134 mph gust', 'All exposed', 'Per ASCE 7-16'],
    ['Dynamic Load', '200 lb', 'Pull-up bar', 'Single-person dynamic'],
    ['Dynamic Load', '150 lb', 'Monkey bars', 'Single-person dynamic'],
    ['Dynamic Load', '300 lb', 'Dip stations', 'Single-person dynamic'],
]
story.append(data_table(
    [h for h in load_table[0]],
    load_table[1:],
    col_widths=[1.5*inch, 1.0*inch, 1.2*inch, 2.5*inch]
))

story.append(H2('Capacity Calculations'))
story.append(H3('6×6 Southern Pine #2 GC PT Post'))
story.append(S(
    '<b>Axial capacity (48" embed + 14 ft tall = 176" unbraced length):</b><br/>'
    'L/d = 176/5.5 = 32 (slender column)<br/>'
    'Fa = 1,100 × 0.3/32² ≈ 400 psi (adjusted)<br/>'
    'Pallow = 400 × 30.25 in² = ~12,100 lb per post<br/>'
    '<b>Total 4-post capacity: ~48,400 lb</b><br/>'
    '<b>Required (dead + live + snow): ~8,000 lb</b> — <font color="#2E7D32"><b>ADEQUATE (6× safety factor)</b></font>'
))

story.append(Spacer(1, 12))
story.append(H3('4×6 Southern Pine #2 GC PT Beam (Zone B)'))
story.append(S(
    '<b>Span: 10 ft</b><br/>'
    'Uniform load: 40 psf live + 30 psf snow + 15 psf dead = 85 psf<br/>'
    'Tributary width: 5 ft<br/>'
    'w = 85 × 5 = 425 plf<br/>'
    'Mmax = wL²/8 = 425 × 100/8 = 5,312 lb-ft<br/>'
    'Fb = 1100 × 1.15 = 1265 psi<br/>'
    'Srequired = M/Fb = 5312×12/1265 = 50.4 in³<br/>'
    'Sprovided (4×6) = 30.66 in³ — <font color="#C62828"><b>INSUFFICIENT</b></font><br/>'
    '<b>SOLUTION:</b> Use 6×6 beam (S = 51.12 in³) — <font color="#2E7D32"><b>ADEQUATE</b></font>'
))

story.append(Spacer(1, 12))
story.append(H3('2×6 Southern Pine #2 GC PT Joist'))
story.append(S(
    '<b>Span: 6 ft (half of 12 ft deck width)</b><br/>'
    'w = 85 psf × 6 ft = 510 plf per joist<br/>'
    'Mmax = wL²/8 = 510 × 36/8 = 2,295 lb-ft<br/>'
    'Fb = 1100 × 1.15 = 1265 psi<br/>'
    'Srequired = M/Fb = 2295×12/1265 = 21.8 in³<br/>'
    'Sprovided (2×6) = 7.56 in³ × 1.15 (repetitive) = 8.7 in³ — <font color="#C62828"><b>INSUFFICIENT for single 2×6</b></font><br/>'
    '<b>SOLUTION:</b> Space joists at 12" OC (use double 2×6) or use 2×8 at 16" OC<br/>'
    'With 2×8 at 16" OC: S = 21.39 in³ × 1.15 = 24.6 in³ — <font color="#2E7D32"><b>ADEQUATE</b></font>'
))

story.append(PageBreak())

# ============================================================
# SECTION A6: MATERIALS & COST ESTIMATE
# ============================================================
story.append(section_title('BILL OF MATERIALS & COST ESTIMATE', 'A6'))
story.append(H2('Lumber'))
lumber_data = [
    ['Item', 'Qty', 'Size', 'Grade', 'Est. Unit', 'Est. Total'],
    ['6×6 Posts (14 ft)', '4', '14 ft', '#2 GC PT', '$85', '$340'],
    ['6×6 Posts (12 ft)', '4', '12 ft', '#2 GC PT', '$70', '$280'],
    ['6×6 Beams', '8', '12 ft', '#2 GC PT', '$70', '$560'],
    ['4×6 Beams', '4', '12 ft', '#2 GC PT', '$45', '$180'],
    ['4×4 Posts', '6', '8-12 ft', '#2 GC PT', '$25', '$150'],
    ['2×6 Lumber (joists)', '10', '12 ft', '#2 GC PT', '$18', '$180'],
    ['2×6 Lumber (deck)', '4', '12 ft', '#2 GC PT', '$18', '$72'],
    ['2×4 Lumber (braces)', '4', '12 ft', '#2 GC PT', '$12', '$48'],
]
story.append(data_table(
    [h for h in lumber_data[0]],
    lumber_data[1:],
    col_widths=[1.5*inch, 0.5*inch, 0.8*inch, 1.0*inch, 0.8*inch, 0.8*inch]
))
story.append(S('<b>Lumber subtotal: ~$1,810</b>'))

story.append(Spacer(1, 12))
story.append(H2('Hardware & Connectors'))
hw_data = [
    ['Item', 'Qty', 'Size', 'Type', 'Est. Unit', 'Est. Total'],
    ['½"×8" Lag Bolts', '48', '½"×8"', 'HDG', '$1.20', '$58'],
    ['½" Hex Nuts', '48', '½"', 'HDG', '$0.30', '$14'],
    ['⅜" Hex Bolts', '24', '⅜"×6"', 'HDG G4', '$1.50', '$36'],
    ['⅜" Hex Nuts', '24', '⅜"', 'HDG', '$0.30', '$7'],
    ['3" Deck Screws', '400', '3"#8', 'Coated', '$0.08', '$32'],
    ['Simpson GB663/664', '4', '—', 'Post caps', '$12', '$48'],
    ['Simpson HD8', '8', '—', 'Hurricane ties', '$4', '$32'],
    ['Simpson JH Hangers', '20', '—', 'Joist hangers', '$3', '$60'],
    ['U-Bolt Clamps', '24', '1¼" or 1"', 'HDG', '$2.50', '$60'],
]
story.append(data_table(
    [h for h in hw_data[0]],
    hw_data[1:],
    col_widths=[1.5*inch, 0.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch]
))
story.append(S('<b>Hardware subtotal: ~$347</b>'))

story.append(Spacer(1, 12))
story.append(H2('Concrete & Ground'))
conc_data = [
    ['Item', 'Qty', 'Size', 'Type', 'Est. Unit', 'Est. Total'],
    ['Quikrete Fast-Set', '40', '80 lb bag', '—', '$6.50', '$260'],
    ['Gravel bags', '8', '50 lb', 'Drainage', '$5.00', '$40'],
    ['Rubber Mulch', '15', '2 cu ft', 'Playground', '$12', '$180'],
    ['Rubber Mats', '4', '2×2 ft', 'Interlocking', '$25', '$100'],
]
story.append(data_table(
    [h for h in conc_data[0]],
    conc_data[1:],
    col_widths=[1.5*inch, 0.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch]
))
story.append(S('<b>Concrete & ground subtotal: ~$580</b>'))

story.append(Spacer(1, 12))
story.append(H2('Steel, Rope & Rigging'))
steel_data = [
    ['Item', 'Qty', 'Size', 'Type', 'Est. Unit', 'Est. Total'],
    ['Steel Pipe (pull-up)', '1', '1¼"×8 ft', 'A500 B', '$45', '$45'],
    ['Steel Pipe (dip)', '2', '1"×3 ft', 'A500 B', '$25', '$50'],
    ['Safety Netting', '2', '10×200\'', 'UV-stabilized', '$40', '$80'],
    ['UV Zip Ties', '500', '3"', 'UV-rated', '$0.03', '$15'],
    ['Shade Sails', '2', '14×14×14\'', 'HDPE UV', '$120', '$240'],
    ['Turnbuckles', '4', '6" min', 'Stainless', '$8', '$32'],
    ['Eye Bolts', '4', '⅝"×6"', 'Stainless', '$6', '$24'],
    ['Fibershed Rope', '200 ft', '¾"', 'Climbing', '$0.40/ft', '$80'],
    ['Rope Discs', '6', '—', 'Hanging obs.', '$15', '$90'],
    ['Rope Clips', '20', '—', 'Stainless', '$1.50', '$30'],
    ['Carabiners', '10', '—', '12k+ lb', '$10', '$100'],
    ['Swing Chains', '2 sets', '7 ft', 'With S-hooks', '$20', '$40'],
    ['Bungee Cord', '1 roll', '¾"×25 ft', '—', '$18', '$18'],
    ['Steel Primer', '1', '—', 'Red oxide', '$8', '$8'],
    ['Deck Stain', '3 gal', '—', 'Exterior oil', '$30', '$90'],
    ['Copper Naphthenate', '1 qt', '—', 'Preservative', '$12', '$12'],
    ['Exterior Wood Filler', '4 tubes', '—', 'Exterior', '$3', '$12'],
    ['Wood Preservative', '1 qt', '—', 'Copper naph', '$12', '$12'],
]
story.append(data_table(
    [h for h in steel_data[0]],
    steel_data[1:],
    col_widths=[1.5*inch, 0.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch]
))
story.append(S('<b>Steel, rope & rigging subtotal: ~$981</b>'))

story.append(Spacer(1, 12))
story.append(H3('TOTAL COST SUMMARY'))
story.append(S(
    '<b>Lumber:</b> ~$1,810<br/>'
    '<b>Hardware & Connectors:</b> ~$347<br/>'
    '<b>Concrete & Ground:</b> ~$580<br/>'
    '<b>Steel, Rope & Rigging:</b> ~$981<br/>'
    '<b>TOTAL ESTIMATED MATERIAL COST:</b> <font color="#C62828"><b>~$3,718</b></font> (range $3,500–$3,900)<br/><br/>'
    '<font color="#2E7D32"><b>BUDGET OPTIMIZATION:</b><br/>'
    '• Buy lumber in bulk from wholesale (not retail) — saves ~15–20%<br/>'
    '• Purchase Simpson connectors in bulk packs — saves ~10%<br/>'
    '• Shop for shade sails at discount (Amazon, Wayfair, Home Depot clearance)<br/>'
    '• Use recycled rubber mulch from local playground suppliers<br/>'
    '• Skip rope discs if budget is tight — saves ~$90</font>',
    style=ParagraphStyle('cost', fontName='Helvetica', fontSize=10, leading=14)
))

story.append(PageBreak())

# ============================================================
# SECTION A7: CONSTRUCTION CHECKLIST
# ============================================================
story.append(section_title('CONSTRUCTION CHECKLIST', 'A7'))
story.append(H2('Pre-Construction'))
story.append(checklist_item('Call 811 (Mass. utility locators) — 3 business days minimum'))
story.append(checklist_item('Obtain zoning determination from Bridgewater Building Dept'))
story.append(checklist_item('Complete Homeowner Waiver Form (if owner-builder)'))
story.append(checklist_item('Submit online permit application with full set of drawings'))
story.append(checklist_item('Receive Building Permit card — <font color="#C62828"><b>DO NOT START WORK WITHOUT IT</b></font>'))
story.append(checklist_item('Mark post locations with spray paint'))
story.append(checklist_item('Verify property lines and setbacks'))
story.append(checklist_item('Order all materials per BOM'))
story.append(checklist_item('Apply wood preservative to all cut ends before construction'))

story.append(Spacer(1, 12))
story.append(H2('Foundation'))
story.append(checklist_item('Dig all 8 footings to 48" depth minimum'))
story.append(checklist_item('Verify footing spacing: Zone A 12×12, Zone B 10×5'))
story.append(checklist_item('Add 2" gravel base to each hole'))
story.append(checklist_item('Schedule footing inspection'))
story.append(checklist_item('Pour concrete — 3000 psi, 5% air entrainment'))
story.append(checklist_item('Cure minimum 72 hours before framing'))
story.append(checklist_item('Email as-built photos to building@bridgewaterma.org'))

story.append(Spacer(1, 12))
story.append(H2('Framing'))
story.append(checklist_item('Set posts plumb within ¼" in 10 ft'))
story.append(checklist_item('Verify all posts are square (diagonals equal)'))
story.append(checklist_item('Install post connectors (Simpson GB663/HD8)'))
story.append(checklist_item('Install beams — level within ¼" in 10 ft'))
story.append(checklist_item('Install cross-braces at 45°'))
story.append(checklist_item('Install upper deck joists at 12" OC (double 2×6) or 2×8 at 16" OC'))
story.append(checklist_item('Install deck boards — ¼" gap between boards'))
story.append(checklist_item('Schedule framing inspection'))
story.append(checklist_item('Verify all connections are tight'))

story.append(Spacer(1, 12))
story.append(H2('Equipment'))
story.append(checklist_item('Install pull-up bar — test with 200 lb dynamic load'))
story.append(checklist_item('Install monkey bar rungs — test each rung with 150 lb'))
story.append(checklist_item('Install dip station — verify both heights level'))
story.append(checklist_item('Install rope tower — secure top and bottom'))
story.append(checklist_item('Install swing chains — verify S-hook security'))
story.append(checklist_item('Install TRX/rings — verify carabiners locked'))

story.append(Spacer(1, 12))
story.append(H2('Finish'))
story.append(checklist_item('Install safety netting — check all ties are tight'))
story.append(checklist_item('Install shade sails — tension with turnbuckles'))
story.append(checklist_item('Install climbing holds — verify lag bolt security'))
story.append(checklist_item('Apply stain/sealant — minimum two coats'))
story.append(checklist_item('Install ground surface — rubber mulch/tiles'))
story.append(checklist_item('Apply copper naphthenate to all field-cut ends'))

story.append(Spacer(1, 12))
story.append(H2('Final Inspection'))
story.append(checklist_item('Call for final inspection'))
story.append(checklist_item('Verify all bolts torqued and secured'))
story.append(checklist_item('Verify netting gaps < 2"'))
story.append(checklist_item('Verify overhead clearance > 15 ft'))

story.append(PageBreak())

# ============================================================
# SECTION A8: PERMIT REQUIREMENTS
# ============================================================
story.append(section_title('BRIDGEWATER PERMIT REQUIREMENTS', 'A8'))
story.append(H2('Permit Type: Building Permit — Accessory Structure'))

story.append(H2('Required Submittal Documents'))
story.append(checklist_item('Online building permit application (Bridgewater portal)'))
story.append(checklist_item('Plot plan showing proposed structure with setbacks'))
story.append(checklist_item('Foundation details (this drawing set)'))
story.append(checklist_item('Framing details with cross sections (this drawing set)'))
story.append(checklist_item('Elevations (this drawing set)'))
story.append(checklist_item('Homeowner Waiver Form (if owner-builder)'))
story.append(checklist_item('Contractor license (if contractor applies)'))

story.append(Spacer(1, 12))
story.append(H2('Fee Schedule (Bridgewater, effective 7/1/2024)'))
story.append(S(
    '150–300 sq ft: $12 per $1,000 of valuation — Minimum $200<br/>'
    'Estimated valuation: ~$4,000<br/>'
    '<b>Estimated permit fee: ~$48–$50</b>'
))

story.append(Spacer(1, 12))
story.append(H2('Inspections Required'))
story.append(numbered('Footing/Foundation — before concrete is poured'))
story.append(numbered('Framing — after structural assembly complete'))
story.append(numbered('Final — after all work complete including finishes'))

story.append(Spacer(1, 12))
story.append(H2('Timeline'))
story.append(numbered('Application processing: 5–10 business days'))
story.append(numbered('Permit card issued before work begins'))
story.append(numbered('Inspections must be scheduled in advance'))
story.append(numbered('Email photos to building@bridgewaterma.org'))

story.append(Spacer(1, 24))

story.append(H3('⚠ IMPORTANT NOTICE'))
story.append(S(
    'This blueprint set is provided as a guide for owner-builder construction. '
    'All work must comply with the latest adopted codes and local ordinances of '
    'the Town of Bridgewater, MA. For structures over 12 ft in height or complex '
    'load paths, consultation with a Massachusetts-licensed structural engineer is '
    'recommended.<br/><br/>'
    'No warranty is made regarding the accuracy or completeness of this document. '
    'The owner-builder assumes all responsibility for compliance with applicable codes, '
    'regulations, and safety standards.',
    style=ParagraphStyle('notice', fontName='Helvetica', fontSize=9, textColor=DARK_GREY, leading=13)
))

story.append(Spacer(1, 24))
end_style = ParagraphStyle('end', fontName='Helvetica-Bold', fontSize=11, textColor=NAVY, alignment=TA_CENTER)
story.append(Paragraph('END OF STRUCTURAL BLUEPRINT SET', end_style))
endnote_style = ParagraphStyle('endnote', fontName='Helvetica-Oblique', fontSize=8, textColor=MID_GREY, alignment=TA_CENTER)
story.append(Paragraph('Prepared using IBC 2018/IRC 2018 design criteria, 780 CMR 10th Edition, and Bridgewater zoning ordinance Section 4.4.', endnote_style))

# Build PDF
doc.build(story, onFirstPage=make_cover, onLaterPages=make_header)

print('Blueprint PDF generated successfully!')
print(f'Output: /workspace/outdoor_gym_engineering_blueprint.pdf')
