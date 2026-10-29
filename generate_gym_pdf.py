#!/usr/bin/env python3
"""Generate a professional Backyard Calisthenics Fortress PDF."""
import json, sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Image
)
from reportlab.lib.colors import HexColor

# ── Colors ──────────────────────────────────────────
NAVY      = HexColor("#1B2A4A")
BLUE      = HexColor("#2C3E6B")
ACCENT    = HexColor("#E8872A")
LIGHT_BG  = HexColor("#F4F1EC")
ROW_ALT   = HexColor("#EDEAE4")
HEADER_BG = HexColor("#1B2A4A")
WHITE     = colors.white
GRAY      = HexColor("#888888")
LIGHT_GRAY = HexColor("#D5D0C8")
GREEN     = HexColor("#2E7D32")
RED       = HexColor("#C62828")

W, H = letter
LM, RM = 0.75*inch, 0.75*inch

styles = getSampleStyleSheet()
def S(name, fontName="Helvetica", fontSize=10, leading=14, textColor=HexColor("#333333"),
      alignment=TA_JUSTIFY, spaceBefore=0, spaceAfter=5, leftIndent=0, fontBold=False):
    fn = fontName + "-Bold" if fontBold else fontName
    return ParagraphStyle(name, fontName=fn, fontSize=fontSize, leading=leading,
                          textColor=textColor, alignment=alignment,
                          spaceBefore=spaceBefore, spaceAfter=spaceAfter, leftIndent=leftIndent)

def h1(t): return [Paragraph(t, S("h1", fontName="Helvetica", fontSize=20, leading=26, textColor=NAVY, spaceBefore=16, spaceAfter=6, fontBold=True))]
def h2(t): return [Paragraph(t, S("h2", fontName="Helvetica", fontSize=14, leading=18, textColor=BLUE, spaceBefore=12, spaceAfter=4, fontBold=True))]
def h3(t): return [Paragraph(t, S("h3", fontName="Helvetica", fontSize=11, leading=14, textColor=BLUE, spaceBefore=6, spaceAfter=2, fontBold=True))]
def p(t):  return Paragraph(t, S("body"))
def bl(t): return Paragraph("\u2022  " + t, S("bl", leftIndent=16, spaceAfter=2, alignment=TA_JUSTIFY))
def note(t): return Paragraph("\u26A0  " + t, S("note", textColor=RED, fontBold=False, fontSize=9, leading=12, alignment=TA_JUSTIFY, spaceAfter=4))
def div(): return HRFlowable(width="100%", thickness=1, color=LIGHT_GRAY, spaceBefore=5, spaceAfter=5)

def tbl(headers, rows, cw=None):
    hdata = [[Paragraph(h, S("th", fontName="Helvetica-Bold", fontSize=9, textColor=WHITE)) for h in headers]]
    bdata = []
    for i, r in enumerate(rows):
        cells = [Paragraph(str(c), S("tb", fontName="Helvetica", fontSize=9, textColor=HexColor("#333333"))) for c in r]
        bdata.append(cells)
    allr = hdata + bdata
    n = len(headers)
    if not cw:
        cw = [(W - 2*LM - 2*RM) / n] * n
    t = Table(allr, colWidths=cw, repeatRows=1)
    cmds = [
        ("GRID", (0,0), (-1,-1), 0.5, LIGHT_GRAY),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("BACKGROUND", (0,0), (-1,0), HEADER_BG),
    ]
    for i in range(1, len(allr)):
        if i % 2 == 0:
            cmds.append(("BACKGROUND", (0,i), (-1,i), ROW_ALT))
    t.setStyle(TableStyle(cmds))
    return t

def cover_box(rows):
    cols = len(rows[0])
    cw = [(W - 2*LM - 2*RM) / cols] * cols
    t = Table(rows, colWidths=cw, repeatRows=1)
    cmds = [
        ("GRID", (0,0), (-1,-1), 1.5, NAVY),
        ("BACKGROUND", (0,0), (-1,0), LIGHT_BG),
        ("LEFTPADDING", (0,0), (-1,-1), 10), ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("FONTSIZE", (0,0), (-1,-1), 11),
    ]
    for i in range(len(rows)):
        if i == 0:
            cmds += [("FONTNAME", (0,i), (-1,i), "Helvetica-Bold"), ("TEXTCOLOR", (0,i), (-1,i), NAVY)]
    t.setStyle(TableStyle(cmds))
    return t

def checklist(items):
    return [Paragraph(f"<font color='{GREEN}'>&#9744;</font>  {i}", S("bl2", fontName="Helvetica", fontSize=10, leftIndent=16, spaceAfter=2)) for i in items]

def header(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 8)
    canvas.setFillColor(NAVY)
    canvas.drawString(LM, H - 0.5*inch, "DIY BACKYARD CALISTHENICS FORTRESS")
    canvas.restoreState()

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(W/2, 0.4*inch, f"Backyard Calisthenics Fortress Build Plan  |  Page {doc.page}")
    canvas.setStrokeColor(LIGHT_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(LM, 0.6*inch, W - RM, 0.6*inch)
    canvas.restoreState()

def build():
    filename = "/workspace/outdoor_gym_professional.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
        leftMargin=LM, rightMargin=RM, topMargin=0.6*inch, bottomMargin=0.6*inch,
        title="Backyard Calisthenics Fortress — Complete Building Plan", author="Stark Tower Workshop")
    story = []

    # ── COVER ──
    story.append(Spacer(1, 1.2*inch))
    story.append(cover_box([[r"\U0001f3cb\ufe0f  DIY BACKYARD CALISTHENICS FORTRESS"]]))
    story.append(Spacer(1, 10))
    cs_style = S("cs", fontName="Helvetica", fontSize=16, leading=20, textColor=BLUE, spaceBefore=0, spaceAfter=6, alignment=TA_CENTER)
    story.append(Paragraph("Complete Outdoor Gym Building Plan", cs_style))
    story.append(Spacer(1, 6))
    ct_style = S("ct", fontName="Helvetica-Oblique", fontSize=11, leading=15, textColor=ACCENT, spaceBefore=0, spaceAfter=0, alignment=TA_CENTER)
    story.append(Paragraph("Pull-up Station &bull; Monkey Bars &bull; Rope Tower &bull; Swings<br/>&bull; Upper Deck with Netting &amp; Shade", ct_style))
    story.append(Spacer(1, 20))
    img1 = Image("/workspace/img/cover_overview.png", width=500, height=320)
    story.append(img1)
    story.append(Spacer(1, 15))
    story.append(cover_box([
        ["<b>Footprint</b>", "~22 ft &times; 12 ft"],
        ["<b>Height</b>", "14 ft (Zone A), 12 ft (Zone B)"],
        ["<b>Build Time</b>", "4&ndash;6 Weekends"],
        ["<b>Materials Cost</b>", "~$3,000&ndash;$3,900"],
        ["<b>Zones</b>", "Adventure Tower + Calisthenics Frame"],
    ]))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Based on the reference build from @calistenics.withkaylee Instagram.", S("cn", fontName="Helvetica-Oblique", fontSize=9, textColor=GRAY, alignment=TA_CENTER)))
    story.append(Paragraph("Always consult local building codes and call 811 before digging.", S("cw", fontName="Helvetica", fontSize=9, textColor=RED, alignment=TA_CENTER)))
    story.append(PageBreak())

    # ── TOC ──
    story.append(Paragraph("Table of Contents", S("toc", fontName="Helvetica-Bold", fontSize=20, textColor=NAVY, spaceBefore=12, spaceAfter=10)))
    for i, item in enumerate([
        "Section 1 &mdash; Structure Overview",
        "Section 2 &mdash; Tools Required",
        "Section 3 &mdash; Complete Materials List",
        "Section 4 &mdash; Materials Cost Summary",
        "Section 5 &mdash; Cut List",
        "Section 6 &mdash; Assembly Instructions",
        "Section 7 &mdash; Safety Checklist",
        "Section 8 &mdash; Maintenance Schedule",
        "Section 9 &mdash; Budget Optimization Tips",
    ], 1):
        story.append(Paragraph(f"<b>{i}. {item}</b>", S("ti", fontName="Helvetica", fontSize=11, textColor=BLUE, leftIndent=12, spaceAfter=4)))
    story.append(PageBreak())

    # ── SEC 1: OVERVIEW ──
    story.extend(h1("Section 1 &mdash; Structure Overview"))
    story.append(p("Two-zone wooden adventure structure. Zone A is the main adventure tower with upper deck, safety netting, and shade canopy. Zone B is a dedicated calisthenics training frame with monkey bars, pull-up bar, and dip stations. Built entirely from ground-contact rated pressure-treated lumber with galvanized hardware throughout."))
    story.append(Spacer(1, 6))
    img_tower = Image("/workspace/img/tower_closeup.png", width=500, height=340)
    story.append(img_tower)
    story.append(Spacer(1, 6))
    story.extend(h2("Configuration"))
    story.append(tbl(["Zone", "Dimensions"], [
        ["Zone A &mdash; Main Adventure Tower", "~12 ft &times; 12 ft, 14 ft tall"],
        ["Zone B &mdash; Calisthenics Frame", "~10 ft &times; 5 ft, 12 ft tall"],
        ["Total Footprint", "~22 ft &times; 12 ft (plus 5+ ft clearance)"],
    ], [160, 300]))
    story.append(Spacer(1, 6))
    story.extend(h2("Features"))
    for f in ["Pull-up bar (chin-ups, toe-to-bar, ball slams)", "Monkey bar ladder (8 rungs, 16&ndash;21.5\" green powder-coated)", "Dip station at 2 heights (low + high)", "Rope tower with climbing rope and hanging disc obstacles", "TRX / gymnastic ring suspension system", "2&ndash;3 disc/tire swings with chain hardware", "Hammock attachment point", "Upper level with full perimeter safety netting", "Black shade sail canopy (X-pattern overlap)", "Wood climbing holds mounted on posts", "Bungee / abduct bar for core training"]:
        story.append(bl(f))
    story.append(Spacer(1, 8))
    img_frame = Image("/workspace/img/frame_closeup.png", width=500, height=340)
    story.append(img_frame)
    story.append(PageBreak())

    # ── SEC 2: TOOLS ──
    story.extend(h1("Section 2 &mdash; Tools Required"))
    story.extend(h2("Power Tools"))
    story.append(tbl(["Tool", "Purpose", "Cost"], [
        ["Miter Saw (10\" or 12\")", "Cross-cut all lumber", "$100&ndash;$200"],
        ["Cordless Drill/Driver (20V)", "Pre-drill, drive screws", "$50&ndash;$150"],
        ["Impact Driver", "Sink &frac12;&rdquo; lag bolts into 6&times;6", "$60&ndash;$120"],
        ["Circular Saw", "Trim posts, cut angles", "$40&ndash;$100"],
    ], [120, 240, 80]))
    story.append(Spacer(1, 6))
    story.extend(h2("Hand Tools"))
    story.append(tbl(["Tool", "Purpose"], [
        ["4-foot Level", "Check posts plumb, beams level"],
        ["Tape Measure (25&ndash;50 ft)", "All measurements"],
        ["Speed Square", "Mark 90&deg;/45&deg; cuts"],
        ["Wrench Set (9/16\", &frac12;, 3/4\")", "Tighten lag bolts and nuts"],
        ["Post-Hole Digger / Auger", "Dig 4&ndash;5 ft deep holes"],
        ["Shovel", "Dig, backfill, move materials"],
        ["Wheelbarrow", "Transport concrete, gravel"],
        ["Hammer", "General assembly"],
        ["Pliers / Locking Pliers", "Wire ties, hardware work"],
    ], [150, 350]))
    story.append(Spacer(1, 6))
    story.extend(h2("Specialized"))
    story.append(tbl(["Tool", "Purpose", "Cost"], [
        ["Forstner Bit Set (1&frac14;\")", "Drill holes for monkey bar bolts", "$20&ndash;$40"],
        ["Chain Saw (optional)", "Trim posts at ground", "Rent $40/day"],
        ["Drill Press (optional)", "Clean holes in timber", "Shop rental"],
    ], [130, 270, 100]))
    story.append(PageBreak())

    # ── SEC 3: MATERIALS ──
    story.extend(h1("Section 3 &mdash; Complete Materials List"))
    story.append(note("All lumber: Ground Contact rated PT. All hardware: galvanized or stainless."))
    story.append(Spacer(1, 4))

    story.extend(h2("3A &mdash; 6&times;6 &amp; 4&times;6 Structural Timber"))
    story.append(tbl(["Item", "Qty", "Dimensions", "Unit", "Total"], [
        ["6&times;6 Posts", "8", "14 ft", "~$75", "$600.00"],
        ["6&times;6 Posts", "4", "12 ft", "~$52.48", "$209.92"],
        ["4&times;6 Beams (main)", "6", "12 ft", "~$32.88", "$197.28"],
        ["4&times;6 Beams (upper)", "4", "12 ft", "~$32.88", "$131.52"],
    ], [80, 30, 65, 55, 55]))
    story.append(p("<b>Subtotal &mdash; 6&times;6 &amp; 4&times;6 Timbers:</b> $1,138.72"))
    story.append(Spacer(1, 4))

    story.extend(h2("3B &mdash; 4&times;4 Lumber"))
    story.append(tbl(["Item", "Qty", "Dimensions", "Unit", "Total"], [
        ["4&times;4 Posts", "8", "10 ft", "~$16.58", "$132.64"],
        ["4&times;4 Posts", "6", "8 ft", "~$19.48", "$116.88"],
        ["4&times;4 Posts", "4", "6 ft", "~$10.28", "$41.12"],
    ], [80, 30, 65, 55, 55]))
    story.append(p("<b>Subtotal &mdash; 4&times;4 Lumber:</b> $290.64"))
    story.append(Spacer(1, 4))

    story.extend(h2("3C &mdash; 2&times; Lumber"))
    story.append(tbl(["Item", "Qty", "Dimensions", "Unit", "Total"], [
        ["2&times;6 Lumber", "10", "12 ft", "~$14.18", "$141.80"],
        ["2&times;6 Lumber", "6", "8 ft", "~$8.48", "$50.88"],
        ["2&times;4 Lumber", "12", "10 ft", "~$5.50", "$66.00"],
        ["2&times;4 Lumber", "8", "8 ft", "~$4.58", "$36.64"],
        ["2&times;6 Deck Boards", "6", "12 ft", "~$10.50", "$63.00"],
    ], [90, 25, 60, 55, 55]))
    story.append(p("<b>Subtotal &mdash; 2&times; Lumber:</b> $358.32"))
    story.append(Spacer(1, 4))

    story.extend(h2("3D &mdash; Steel, Hardware &amp; Fasteners"))
    story.append(tbl(["Item", "Qty", "Purpose", "Unit", "Total"], [
        ["&frac12;&rdquo;&times;8&rdquo; Lag Bolts", "60", "6&times;6 connections", "~$0.80", "$48.00"],
        ["&frac12;&rdquo; Hex Nuts", "60", "For lag bolts", "~$0.35", "$21.00"],
        ["&frac38;&rdquo;&times;6&rdquo; Lag Bolts", "40", "4&times;4 connections", "~$0.50", "$20.00"],
        ["&frac38;&rdquo; Hex Nuts", "40", "For &frac38;&rdquo; bolts", "~$0.25", "$10.00"],
        ["3&rdquo; Deck Screws", "500", "General assembly", "~$0.06", "$30.00"],
        ["2.5&rdquo; Deck Screws", "300", "Lighter connections", "~$0.05", "$15.00"],
        ["Post Base Connectors", "12", "Simpson GB series", "~$4.00", "$48.00"],
        ["3/4&rdquo; G4 Hex Bolts", "40", "Steel connections", "~$1.50", "$60.00"],
        ["Metal Beam Clamps", "16", "Pipe-to-wood mount", "~$2.50", "$40.00"],
    ], [100, 25, 85, 45, 45]))
    story.append(p("<b>Subtotal &mdash; Steel &amp; Hardware:</b> $392.00"))
    story.append(Spacer(1, 4))

    story.extend(h2("3E &mdash; Monkey Bars &amp; Pull-Up Hardware"))
    story.append(tbl(["Item", "Qty", "Details", "Unit", "Total"], [
        ["Metal Bar Rungs (set of 8)", "2 sets", "16&ndash;21.5\" green", "~$35", "$70.00"],
        ["1&frac14;&rdquo; Steel Round Tube", "1", "Schedule 40, ~8 ft", "~$28", "$28.00"],
        ["1&rdquo; Galvanized Pipe", "2", "3 ft each (dip bars)", "~$15", "$30.00"],
        ["&frac12;&rdquo; Steel Rod", "2", "4 ft each", "~$12", "$24.00"],
        ["U-bolts", "8", "1&frac14;&rdquo; or 1&rdquo; bore", "~$3", "$24.00"],
    ], [100, 25, 85, 45, 45]))
    story.append(p("<b>Subtotal &mdash; Monkey Bars &amp; Bars:</b> $176.00"))
    story.append(Spacer(1, 4))

    story.extend(h2("3F &mdash; Rope &amp; Swing Equipment"))
    story.append(tbl(["Item", "Qty", "Details", "Unit", "Total"], [
        ["&frac34;&rdquo; Fibershed Rope", "200 ft", "100 ft roll &times; 2", "~$70", "$70.00"],
        ["Rope Pulley System", "1", "Flying fox / zipline", "~$25", "$25.00"],
        ["Rope Climbing Discs", "6", "Hanging rope course", "~$12", "$72.00"],
        ["Gymnastic Rings (pair)", "1", "Wooden or rubber", "~$40", "$40.00"],
        ["TRX Suspension Straps", "1", "Outdoor-rated", "~$175", "$175.00"],
        ["Disc/Tire Swings", "2", "36&rdquo;&ndash;42&rdquo;", "~$30", "$60.00"],
        ["Swing Chains w/S-hooks", "2 sets", "7 ft per swing", "~$15", "$30.00"],
        ["Bungee Cord", "1 roll", "&frac34;&rdquo; &times; 25 ft", "~$15", "$15.00"],
        ["Carabiners / Swivel", "10", "12k+ lb rated", "~$8", "$80.00"],
        ["Turnbuckles", "4", "Tensioning lines", "~$8", "$32.00"],
    ], [90, 25, 80, 45, 45]))
    story.append(p("<b>Subtotal &mdash; Rope &amp; Swings:</b> $619.00"))
    story.append(Spacer(1, 4))

    story.extend(h2("3G &mdash; Safety Netting &amp; Shade Sail"))
    story.append(tbl(["Item", "Qty", "Details", "Unit", "Total"], [
        ["Black Safety Netting", "2 rolls", "10 ft &times; 200 ft", "~$80", "$160.00"],
        ["Black Shade Sail", "2", "14&times;14&times;14 ft", "~$45", "$90.00"],
        ["Rope &amp; Hardware Kit", "1", "Eye bolts + turnbuckles", "~$30", "$30.00"],
    ], [90, 25, 85, 45, 45]))
    story.append(p("<b>Subtotal &mdash; Netting &amp; Shade:</b> $280.00"))
    story.append(Spacer(1, 4))

    story.extend(h2("3H &mdash; Climbing Holds &amp; Hammock"))
    story.append(tbl(["Item", "Qty", "Details", "Unit", "Total"], [
        ["Wooden Climbing Holds", "10", "Rock grips", "~$12", "$120.00"],
        ["Heavy-Duty Carabiners", "4", "Attach holds", "~$6", "$24.00"],
        ["Hammock + Hanging Kit", "1", "With chain/rope", "~$60", "$60.00"],
        ["&frac38;&rdquo;&times;4&rdquo; Eye Bolts", "2", "Hammock mount", "~$5", "$10.00"],
    ], [90, 20, 80, 45, 45]))
    story.append(p("<b>Subtotal &mdash; Holds &amp; Hammock:</b> $214.00"))
    story.append(Spacer(1, 4))

    story.extend(h2("3I &mdash; Concrete &amp; Foundation"))
    story.append(tbl(["Item", "Qty", "Details", "Unit", "Total"], [
        ["Quikrete Fast-Setting", "28 bags", "80 lb &times; 12 posts", "~$7.50", "$210.00"],
        ["Gravel for drainage", "3 bags", "50 lb bags", "~$5", "$15.00"],
    ], [110, 30, 80, 45, 45]))
    story.append(p("<b>Subtotal &mdash; Concrete:</b> $225.00"))
    story.append(Spacer(1, 4))

    story.extend(h2("3J &mdash; Finish &amp; Protection"))
    story.append(tbl(["Item", "Qty", "Details", "Unit", "Total"], [
        ["Exterior Wood Stain/Sealant", "2 gal", "Deck stain, oil-based", "~$35", "$70.00"],
        ["Exterior Wood Filler", "2 tubes", "Cracks before stain", "~$6", "$12.00"],
        ["Steel Primer + Paint", "1 can", "Red oxide primer", "~$12", "$12.00"],
    ], [110, 20, 80, 45, 45]))
    story.append(p("<b>Subtotal &mdash; Finish:</b> $94.00"))
    story.append(Spacer(1, 4))

    story.extend(h2("3K &mdash; Ground Surface"))
    story.append(tbl(["Item", "Qty", "Details", "Unit", "Total"], [
        ["Rubber Playground Tiles", "4&ndash;6", "2&times;2 ft interlocking", "~$15", "$90.00"],
        ["Playground/Rubber Mulch", "12 bags", "2 cu ft bags", "~$8", "$96.00"],
        ["Rubber Horse Stall Mats", "2", "4&times;6 ft &times; &frac34;&rdquo;", "~$50", "$100.00"],
    ], [100, 30, 80, 45, 45]))
    story.append(p("<b>Subtotal &mdash; Ground Surface:</b> ~$170.00"))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Complete Layout Overview</b>", S("cv", fontName="Helvetica-Bold", fontSize=13, textColor=NAVY, spaceBefore=6, spaceAfter=4)))
    story.append(Paragraph("<i>All 12 labeled components of the backyard calisthenics fortress</i>", S("ci", fontName="Helvetica-Oblique", fontSize=9, textColor=GRAY, spaceAfter=8)))
    img_layout = Image("/workspace/img/complete_layout.png", width=500, height=340)
    story.append(img_layout)
    story.append(PageBreak())

    # ── SEC 4: COST SUMMARY ──
    story.extend(h1("Section 4 &mdash; Materials Cost Summary"))
    story.append(Spacer(1, 6))
    story.append(tbl(["Category", "Estimated Cost"], [
        ["6&times;6 &amp; 4&times;6 Structural Timber", "$1,139"],
        ["4&times;4 Lumber", "$291"],
        ["2&times; Lumber (rails, bracing, decking)", "$358"],
        ["Steel, Hardware &amp; Fasteners", "$392"],
        ["Monkey Bars &amp; Bar Hardware", "$176"],
        ["Rope &amp; Swing Equipment", "$619"],
        ["Safety Netting &amp; Shade Sail", "$280"],
        ["Climbing Holds &amp; Hammock", "$214"],
        ["Concrete &amp; Foundation", "$225"],
        ["Finish &amp; Protection", "$94"],
        ["Ground Surface", "$170"],
    ], [300, 100]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b style='font-size:14pt;color:#1B2A4A'>TOTAL MATERIALS: ~$3,913</b>", S("total", fontName="Helvetica-Bold", fontSize=14, textColor=NAVY)))
    story.append(Spacer(1, 6))
    story.append(p("Range: <b>$3,000&ndash;$3,900</b> depending on pricing and new vs. used. Can be reduced to <b>~$2,200</b> with reclaimed wood, lumber yard pricing, and bulk hardware."))
    story.append(PageBreak())

    # ── SEC 5: CUT LIST ──
    story.extend(h1("Section 5 &mdash; Cut List"))
    story.append(note("Cut all pieces per labels. Sand edges. Seal all cut ends with preservative."))
    story.append(Spacer(1, 4))

    story.extend(h2("6&times;6 Main Posts &mdash; 12 pieces"))
    story.append(tbl(["Label", "Description", "Length", "Qty", "Notes"], [
        ["A1&ndash;A4", "Main tower posts (front &amp; rear)", "14 ft 0 in", "4", "Tower legs &mdash; bury 3 ft"],
        ["B1&ndash;B4", "Rear tower posts", "14 ft 0 in", "4", "Tower legs &mdash; bury 3 ft"],
        ["C1&ndash;C4", "Upper level posts", "12 ft 0 in", "4", "Sit atop A1&ndash;A4"],
    ], [45, 120, 55, 25, 90]))
    story.append(Spacer(1, 4))

    story.extend(h2("6&times;6 Horizontal Beams"))
    story.append(tbl(["Label", "Description", "Length", "Qty", "Notes"], [
        ["D1", "Main span beam (front)", "12 ft 0 in", "1", "A1&ndash;A4 @ ~10 ft"],
        ["D2", "Main span beam (rear)", "12 ft 0 in", "1", "B1&ndash;B4 @ ~10 ft"],
        ["D3", "Side span beam (left)", "12 ft 0 in", "1", "A1&ndash;B1"],
        ["D4", "Side span beam (right)", "12 ft 0 in", "1", "A4&ndash;B4"],
        ["D5&ndash;D8", "Upper level ring beams", "12 ft 0 in", "4", "C1&ndash;C4 @ ~13 ft"],
        ["D9&ndash;D12", "Cross-brace beams", "10 ft 6 in", "4", "Interior @ ~7 ft"],
    ], [45, 120, 55, 25, 80]))
    story.append(Spacer(1, 4))

    story.extend(h2("4&times;6 Beams &mdash; Zone B"))
    story.append(tbl(["Label", "Description", "Length", "Qty", "Notes"], [
        ["E1", "Main span (front)", "10 ft 0 in", "1", "Top of Zone B"],
        ["E2", "Main span (rear)", "10 ft 0 in", "1", "Top of Zone B"],
        ["E3", "Mid beam (pull-up)", "10 ft 0 in", "1", "~9 ft height"],
    ], [45, 130, 55, 25, 65]))
    story.append(Spacer(1, 4))

    story.extend(h2("4&times;4 Posts"))
    story.append(tbl(["Label", "Description", "Length", "Qty", "Notes"], [
        ["F1&ndash;F4", "Zone B main posts", "12 ft 0 in", "4", "Monkey bar frame"],
        ["G1&ndash;G2", "Dip station front posts", "8 ft 0 in", "2", "Low dip bars"],
        ["G3&ndash;G4", "Dip station rear posts", "7 ft 0 in", "2", "High dip bars"],
        ["H1&ndash;H2", "Hammock support posts", "6 ft 0 in", "2", "Side hammock"],
    ], [45, 130, 55, 25, 65]))
    story.append(Spacer(1, 4))

    story.extend(h2("4&times;4 Rails"))
    story.append(tbl(["Label", "Description", "Length", "Qty", "Notes"], [
        ["I1", "Top rail (Zone A front)", "12 ft 0 in", "1", "~11 ft height"],
        ["I2", "Top rail (Zone A rear)", "12 ft 0 in", "1", "~11 ft height"],
        ["I3&ndash;I4", "Top rail (Zone A sides)", "10 ft 0 in", "2", "~11 ft height"],
        ["I5", "Mid rail (Zone B pull-up)", "10 ft 0 in", "1", "Reinforce pull-up"],
        ["I6", "Mid rail (Zone B dip)", "5 ft 0 in", "1", "Connect dip posts"],
    ], [45, 130, 55, 25, 65]))
    story.append(Spacer(1, 4))

    story.extend(h2("2&times; Lumber &mdash; Bracing &amp; Decking"))
    story.append(tbl(["Label", "Description", "Length", "Qty", "Notes"], [
        ["J1&ndash;J4", "Upper deck joists", "10 ft 0 in", "4", "Support upper platform"],
        ["K1&ndash;K4", "Diagonal cross-braces", "12 ft 0 in", "4", "45&deg; angle"],
        ["L1&ndash;L6", "Dip bar rails", "6 ft 0 in", "6", "Horizontal rails"],
        ["M1&ndash;M4", "Deck planks (upper level)", "11 ft 6 in", "4", "Walking surface"],
    ], [45, 130, 55, 25, 65]))
    story.append(Spacer(1, 4))

    story.extend(h2("Steel &amp; Rope"))
    story.append(tbl(["Label", "Description", "Length", "Qty", "Notes"], [
        ["N1", "Pull-up steel pipe", "7 ft 6 in (1&frac14;&rdquo; OD)", "1", "Center of Zone B"],
        ["N2&ndash;N9", "Monkey bar rungs", "16&ndash;21.5 in each", "8", "Green powder-coated"],
        ["N10&ndash;N11", "Dip steel pipes", "3 ft 0 in (1&rdquo; OD)", "2", "Beam clamps"],
        ["O1", "Climbing rope", "100 ft roll", "1 roll", "&frac34;&rdquo; or 1&rdquo; fibershed"],
        ["O2&ndash;O3", "Swing chains", "7 ft each", "2", "With S-hooks"],
    ], [45, 120, 65, 25, 65]))
    story.append(PageBreak())

    # ── SEC 6: BUILD INSTRUCTIONS ──
    story.extend(h1("Section 6 &mdash; Assembly Instructions"))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Photorealistic Assembly Guide</b>", S("cv", fontName="Helvetica-Bold", fontSize=13, textColor=NAVY, spaceBefore=4, spaceAfter=4)))
    story.append(Paragraph("<i>Visual reference for each construction phase</i>", S("ci", fontName="Helvetica-Oblique", fontSize=9, textColor=GRAY, spaceAfter=8)))
    
    # Phase 1
    story.append(Spacer(1, 4))
    story.extend(h2("Phase 1 &mdash; Layout &amp; Foundation (Weekend 1)"))
    img_foundation = Image("/workspace/img/foundation_phase.png", width=500, height=340)
    story.append(img_foundation)
    story.append(Spacer(1, 8))
    story.extend(h3("Step 1 &mdash; Mark the footprint"))
    for b in ["Lay out Zone A (12&times;12 ft) and Zone B (10&times;5 ft) side-by-side", "Use spray paint or string line. Add 5 ft clearance on all sides", "CALL 811 before digging &mdash; mark underground utilities", "Mark post locations for all 12 main posts"]:
        story.append(bl(b))
    story.extend(h3("Step 2 &mdash; Dig all footings"))
    for b in ["Diameter: 12&ndash;14 in | Depth: 36 in minimum (48 in in frost areas)", "Add 2 in of gravel at bottom of each hole", "Zone B posts (lighter): 30 in deep is acceptable"]:
        story.append(bl(b))
    story.extend(h3("Step 3 &mdash; Set 6&times;6 posts (Zone A)"))
    for b in ["Place posts into holes, check plumb with level on two sides", "Brace each post with temporary 2&times;4 stakes", "Ensure posts are square (measure diagonals &mdash; must be equal)", "Pour fast-setting concrete (2&ndash;3 bags per hole), poke to release air", "Slope concrete top away from post for drainage"]:
        story.append(bl(b))
    story.append(note("Cure 48&ndash;72 hours before proceeding"))
    story.extend(h3("Step 4 &mdash; Set 4&times;4 posts (Zone B)"))
    for b in ["Same process, 30 in deep", "Align top of Zone B frame to ~12 ft finished height"]:
        story.append(bl(b))
    story.append(Spacer(1, 6))
    story.extend(h2("Phase 2 &mdash; Main Frame Assembly (Weekend 2)"))
    img_frame = Image("/workspace/img/frame_phase.png", width=500, height=340)
    story.append(img_frame)
    story.append(Spacer(1, 8))
    story.extend(h3("Step 5 &mdash; Install mid-level beams (D9&ndash;D12 at ~7 ft)"))
    for b in ["Cut 6&times;6 beams to 10 ft 6 in (cross-brace beams)", "Attach between adjacent posts using &frac12;&rdquo;&times;8&rdquo; lag bolts (2 per connection)"]:
        story.append(bl(b))
    story.extend(h3("Step 6 &mdash; Install main span beams (D1&ndash;D4 at ~10 ft)"))
    for b in ["Position front beam (D1) between A1&ndash;A4, rear beam (D2) between B1&ndash;B4", "Side beams (D3, D4) connect A1&ndash;B1 and A4&ndash;B4", "Pre-drill &frac14;&rdquo; pilot holes, use &frac12;&rdquo;&times;8&rdquo; lag bolts (3 per connection)", "Use post base connectors (Simpson GB series) for added strength"]:
        story.append(bl(b))
    story.extend(h3("Step 7 &mdash; Install Zone B beams (E1&ndash;E3)"))
    for b in ["E1, E2: 10 ft beams at 12 ft height (F1&ndash;F2 and F3&ndash;F4)", "E3: Mid beam at ~9 ft height for pull-up bar (F1&ndash;F4)"]:
        story.append(bl(b))
    story.extend(h3("Step 8 &mdash; Add cross-bracing"))
    for b in ["Install diagonal 2&times;4 braces from lower posts to mid-level beams at 45&deg;", "Secure with 3&rdquo; deck screws (2 per brace) + &frac12;&rdquo; lag bolts"]:
        story.append(bl(b))
    story.append(Spacer(1, 6))
    story.extend(h2("Phase 3 &mdash; Upper Level &amp; Monkey Bars (Weekend 3)"))
    img_deck = Image("/workspace/img/deck_phase.png", width=500, height=340)
    story.append(img_deck)
    story.append(Spacer(1, 8))
    story.extend(h3("Step 9 &mdash; Attach upper-level posts (C1&ndash;C4)"))
    for b in ["Bolt 12 ft posts on top of A1&ndash;A4 using steel post caps", "Use 3/4&rdquo; G4 hex bolts (3 per post) through metal connector plates", "Verify all four upper posts are level and square"]:
        story.append(bl(b))
    story.extend(h3("Step 10 &mdash; Install upper level beams (D5&ndash;D8)"))
    for b in ["Build 12&times;12 ft ring at ~13 ft height using 6&times;6 beams", "This is the top ring where netting and shade sail attach"]:
        story.append(bl(b))
    story.extend(h3("Step 11 &mdash; Install upper deck joists (J1&ndash;J4)"))
    for b in ["Place 2&times;6 joists between D5&ndash;D8 at 16&rdquo; OC spacing", "Use joist hangers (Simpson JH series, ~$2/each)"]:
        story.append(bl(b))
    story.extend(h3("Step 12 &mdash; Install upper deck planks (M1&ndash;M4)"))
    for b in ["Lay 2&times;6 deck boards across joists, leave &frac14;&rdquo; gap for drainage", "Secure with 3&rdquo; deck screws (2 per joist per board)"]:
        story.append(bl(b))
    story.extend(h3("Step 13 &mdash; Install monkey bar frame"))
    for b in ["Attach 8 metal rungs across top beam E1/E2", "Rung spacing: 12&ndash;14 in apart | sticks out ~6 in each side", "<b>Test every rung</b> before continuing &mdash; they bear full body weight"]:
        story.append(bl(b))
    story.extend(h3("Step 14 &mdash; Install pull-up bar (N1)"))
    for b in ["Center 1&frac14;&rdquo; steel pipe between Zone B mid-beam (E3)", "Mount using metal beam clamps (U-bolts) &mdash; bar at ~9 ft height"]:
        story.append(bl(b))
    story.append(Spacer(1, 6))
    story.extend(h2("Phase 4 &mdash; Dip Bars, Rope Tower &amp; Swings (Weekend 4)"))
    # No dedicated image for phase 4, components shown in visual reference section above
    story.append(Spacer(1, 4))
    story.extend(h3("Step 15 &mdash; Build dip station"))
    for b in ["Low dip bars (G1&ndash;G2 at 8 ft): Mount 3 ft steel pipes with beam clamps", "High dip bars (G3&ndash;G4 at 7 ft): Similar on rear dip posts", "Dip bar height: 28&ndash;32 in from ground | secure with &frac38;&rdquo;&times;6&rdquo; lag bolts"]:
        story.append(bl(b))
    story.extend(h3("Step 16 &mdash; Install rope tower"))
    for b in ["Drill &frac34;&rdquo; hole through top beam, thread climbing rope through (100 ft roll)", "Secure top with rope thimble + carabiner or wrap + rope clips", "Hang 6 rope course discs every 3&ndash;4 ft"]:
        story.append(bl(b))
    story.extend(h3("Step 17 &mdash; Install TRX / gymnastic rings"))
    for b in ["Mount heavy-duty eye bolts into top beam of Zone A", "Attach TRX straps or wooden rings at ~9&ndash;10 ft for ring dips", "Use swivel carabiners to prevent strap twisting"]:
        story.append(bl(b))
    story.extend(h3("Step 18 &mdash; Install swings"))
    for b in ["Mount 7 ft swing chains with S-hooks to upper beams", "Attach 2 disc/tire swings (36&rdquo;&ndash;42&rdquo;) at ~16 ft clearance", "Space swings 6&ndash;8 ft apart for safety"]:
        story.append(bl(b))
    story.extend(h3("Step 19 &mdash; Install hammock"))
    for b in ["Attach 6 ft support posts or use existing frame", "Install &frac38;&rdquo;&times;4&rdquo; stainless eye bolts at opposite ends", "Hang hammock &mdash; target seat height 18 in from ground"]:
        story.append(bl(b))
    story.extend(h3("Step 20 &mdash; Add bungee / abduct bar"))
    for b in ["Run &frac34;&rdquo; bungee cord between two posts at ~4 ft height", "Attach to &frac14;&rdquo; steel cable or rope for horizontal core exercises"]:
        story.append(bl(b))
    story.append(Spacer(1, 6))
    story.extend(h2("Phase 5 &mdash; Netting, Shade &amp; Finishing (Weekend 5)"))
    img_netting = Image("/workspace/img/netting_phase.png", width=500, height=340)
    story.append(img_netting)
    story.append(Spacer(1, 8))
    story.extend(h3("Step 21 &mdash; Install safety netting"))
    for b in ["Attach black safety netting around all open sides of upper level", "Use UV-rated zip ties or rope &mdash; attach every 6&ndash;8 in along beams", "Netting covers full 12&times;12 ft perimeter up to top ring"]:
        story.append(bl(b))
    story.extend(h3("Step 22 &mdash; Install shade sails"))
    for b in ["Mount stainless eye bolts at each corner of the top ring", "Attach two 14&times;14&times;14 ft black shade sails in X-pattern", "Use turnbuckles for tensioning &mdash; slight sag for water runoff"]:
        story.append(bl(b))
    story.extend(h3("Step 23 &mdash; Install wood climbing holds"))
    for b in ["Bolt wooden holds into 6&times;6 posts at various heights", "Space 12&ndash;18 in apart for climbing path", "Use &frac38;&rdquo; stainless lag bolts &mdash; drill &frac14;&rdquo; pilot holes first"]:
        story.append(bl(b))
    story.extend(h3("Step 24 &mdash; Paint / stain"))
    for b in ["Apply exterior wood stain/sealant to ALL exposed wood (two coats)", "Let first coat dry 24 hours before second", "Paint all steel pipes with red oxide primer + exterior paint"]:
        story.append(bl(b))
    story.extend(h3("Step 25 &mdash; Install ground surface"))
    for b in ["Lay rubber playground tiles or horse stall mats under drop zones", "Spread 3&ndash;4 in of mulch/rubber mulch in high-traffic areas"]:
        story.append(bl(b))
    story.append(PageBreak())

    # ── SEC 7: SAFETY ──
    story.extend(h1("Section 7 &mdash; Safety Checklist"))
    story.append(Spacer(1, 4))
    for item in ["Underground utilities marked (811 call completed)", "All concrete fully cured 72 hours before loading", "All lag bolts torqued and backed up with nuts", "Pull-up bar tested with 300+ lb dynamic load", "Monkey bar rungs tested individually (150+ lb each)", "Posts plumb on two sides &mdash; verified with level", "Frame diagonals equal (square construction)", "Safety netting securely attached &mdash; no gaps wider than 2 in", "Shade sails tensioned properly &mdash; no sag to trap water", "All swings have 6+ ft clearance from other equipment", "Impact-absorbing ground surface under all drop zones", "Overhead clearance of 15+ ft (no trees, wires, structures)", "All hardware is galvanized or stainless (NO regular steel)", "All cut ends of lumber sealed with preservative"]:
        story.extend(checklist([item]))
    story.append(Spacer(1, 8))

    # ── SEC 8: MAINTENANCE ──
    story.extend(h1("Section 8 &mdash; Maintenance Schedule"))
    story.append(Spacer(1, 4))
    story.append(tbl(["Task", "Frequency"], [
        ["Re-tighten ALL bolts and nuts", "Every 3 mo (1st year), then every 6 mo"],
        ["Inspect concrete footings for cracks/shift", "Annually"],
        ["Check safety netting for tears/loose ties", "Monthly during season"],
        ["Check shade sail tension", "After storms"],
        ["Re-apply stain/sealant", "Every 2 years"],
        ["Inspect steel pipes and hardware for rust", "Monthly"],
        ["Check rope for fraying", "Monthly"],
        ["Inspect swing chains and S-hooks", "Monthly"],
        ["Clean and oil moving parts", "Every 3 months"],
        ["Inspect climbing holds for looseness", "Monthly"],
    ], [280, 160]))
    story.append(PageBreak())

    # ── SEC 9: BUDGET TIPS ──
    story.extend(h1("Section 9 &mdash; Budget Optimization Tips"))
    story.append(Spacer(1, 4))
    for t in [
        "<b>Lumber yard vs. Home Depot:</b> Local yards price 6&times;6s at $35&ndash;45 vs. HD's $52&ndash;75. Save $200+ on timber.",
        "<b>Buy surplus lumber:</b> Home Depot surplus section often has 6&times;6s at 50% off.",
        "<b>Used equipment:</b> Facebook Marketplace for ropes, rings, swings, rubber mats.",
        "<b>Galvanized hardware:</b> Buy in bulk from Fastenal or Grainger vs. retail.",
        "<b>Reclaimed wood:</b> For decking, bracing, and non-critical pieces.",
        "<b>DIY monkey bar rungs:</b> Buy galvanized steel conduit (&frac34;&rdquo; EMT) at ~$8/10 ft and cut to length.",
        "<b>Netting substitute:</b> Construction safety netting from HD can replace expensive playground netting.",
    ]:
        story.append(bl(t))

    story.append(Spacer(1, 15))
    story.append(div())
    story.append(p("<i>This plan is based on verified DIY outdoor playground builds and commercial-grade design principles. Always consult a structural professional for structures above 12 ft. Check local zoning codes and call 811 before digging. Adult supervision recommended during construction.</i>"))

    doc.build(story, onFirstPage=header, onLaterPages=header)
    print(json.dumps({"output": filename, "status": "done"}))
    return 0

if __name__ == "__main__":
    sys.exit(build())
