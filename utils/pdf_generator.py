"""Professional PDF report generator using ReportLab."""

import os
import re
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ── Colour palette ────────────────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#1a237e")
MED_BLUE    = colors.HexColor("#1565c0")
LIGHT_BLUE  = colors.HexColor("#e3f2fd")
DARK_GRAY   = colors.HexColor("#37474f")
LIGHT_GRAY  = colors.HexColor("#f5f5f5")
GREEN       = colors.HexColor("#2e7d32")
ORANGE      = colors.HexColor("#e65100")
RED         = colors.HexColor("#c62828")
WHITE       = colors.white


# ── Style helpers ─────────────────────────────────────────────────────────────

def _build_styles() -> dict:
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle",
            fontSize=30, textColor=WHITE,
            fontName="Helvetica-Bold", alignment=TA_CENTER, leading=38,
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub",
            fontSize=12, textColor=colors.HexColor("#bbdefb"),
            fontName="Helvetica", alignment=TA_CENTER, leading=18,
        ),
        "section": ParagraphStyle(
            "Section",
            fontSize=13, textColor=DARK_BLUE,
            fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4, leading=18,
        ),
        "body": ParagraphStyle(
            "Body",
            fontSize=10, textColor=DARK_GRAY,
            fontName="Helvetica", alignment=TA_JUSTIFY,
            spaceBefore=3, spaceAfter=3, leading=14,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            fontSize=10, textColor=DARK_GRAY,
            fontName="Helvetica", leftIndent=18,
            spaceBefore=2, spaceAfter=2, leading=14,
        ),
        "toc": ParagraphStyle(
            "TOC",
            fontSize=10, textColor=MED_BLUE,
            fontName="Helvetica", spaceBefore=3, spaceAfter=3,
        ),
        "score_label": ParagraphStyle(
            "ScoreLabel",
            fontSize=11, textColor=DARK_GRAY,
            fontName="Helvetica", alignment=TA_CENTER, leading=16,
        ),
    }


def _score_color(score) -> colors.Color:
    if score is None:
        return DARK_BLUE
    if score >= 7.5:
        return GREEN
    if score >= 5.0:
        return ORANGE
    return RED


# ── Text utilities ────────────────────────────────────────────────────────────

def _extract_score(text: str):
    """Return the business health score (float 0-10) if found in text."""
    patterns = [
        r"business health score[:\s]+(\d+(?:\.\d+)?)\s*/\s*10",
        r"health score[:\s]+(\d+(?:\.\d+)?)\s*/\s*10",
        r"overall score[:\s]+(\d+(?:\.\d+)?)\s*/\s*10",
        r"score[:\s]+(\d+(?:\.\d+)?)\s*/\s*10",
        r"(\d+(?:\.\d+)?)\s*/\s*10",
    ]
    for pat in patterns:
        m = re.search(pat, text.lower())
        if m:
            val = float(m.group(1))
            if 0 <= val <= 10:
                return val
    return None


def _md_to_rl(text: str) -> str:
    """Convert minimal markdown markup to ReportLab paragraph XML.

    Order matters: escape XML entities FIRST, then insert tags so the
    added angle-brackets are never double-escaped.
    """
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    # Bold (**text**)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # Italic (*text*) — only single stars remaining
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", text)
    return text


def _safe_para(text: str, style: ParagraphStyle) -> Paragraph:
    """Create a Paragraph, falling back to plain text on XML parse error."""
    try:
        return Paragraph(_md_to_rl(text), style)
    except Exception:
        safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return Paragraph(safe, style)


# ── Section parser ────────────────────────────────────────────────────────────

def _parse_report(text: str, styles: dict):
    """Return (flowables_list, section_titles_list)."""
    sections: list[tuple[str, list[str]]] = []
    cur_title: str | None = None
    cur_lines: list[str] = []

    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("## ") or line.startswith("# "):
            if cur_title is not None:
                sections.append((cur_title, cur_lines))
            cur_title = line.lstrip("#").strip()
            cur_lines = []
        else:
            cur_lines.append(line)

    if cur_title is not None:
        sections.append((cur_title, cur_lines))
    elif cur_lines:
        sections.append(("Report", cur_lines))

    section_names = [s[0] for s in sections]
    story = []

    for title, lines in sections:
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=1.5, color=LIGHT_BLUE, spaceAfter=2))
        story.append(Paragraph(title.upper(), styles["section"]))
        story.append(Spacer(1, 2))

        for line in lines:
            if not line:
                story.append(Spacer(1, 4))
                continue
            if line.startswith(("- ", "* ", "• ")):
                story.append(_safe_para("• " + line[2:], styles["bullet"]))
            elif re.match(r"^\d+\.\s", line):
                story.append(_safe_para("• " + re.sub(r"^\d+\.\s", "", line), styles["bullet"]))
            else:
                story.append(_safe_para(line, styles["body"]))

    return story, section_names


# ── Page decoration ───────────────────────────────────────────────────────────

def _footer(canvas, doc):
    canvas.saveState()
    w, _ = letter
    canvas.setFillColor(DARK_BLUE)
    canvas.rect(0, 0, w, 28, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(
        w / 2, 9,
        "Generated by AI Company Research Agent  •  Powered by CrewAI & Gemini AI",
    )
    canvas.drawRightString(w - 40, 9, f"Page {doc.page}")
    canvas.restoreState()


# ── Public API ────────────────────────────────────────────────────────────────

def generate_pdf(company_name: str, report_text: str) -> str:
    """Generate a professional PDF report and return the file path."""
    os.makedirs("output", exist_ok=True)

    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = re.sub(r"[^\w\s-]", "", company_name).strip().replace(" ", "_")
    path = os.path.join("output", f"{safe}_report_{ts}.pdf")

    margin = 0.75 * inch
    pw     = letter[0] - 2 * margin  # usable page width

    doc = SimpleDocTemplate(
        path,
        pagesize=letter,
        rightMargin=margin,
        leftMargin=margin,
        topMargin=margin,
        bottomMargin=margin + 10,
    )

    styles = _build_styles()
    story  = []

    # ── Cover header banner ───────────────────────────────────────────────────
    cover_rows = [
        [Paragraph(company_name, styles["cover_title"])],
        [Paragraph("Business Intelligence Report", styles["cover_sub"])],
        [Paragraph(datetime.now().strftime("Generated on %B %d, %Y"), styles["cover_sub"])],
    ]
    cover_tbl = Table(cover_rows, colWidths=[pw])
    cover_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), DARK_BLUE),
        ("TOPPADDING",    (0, 0), (-1, 0),  24),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 24),
        ("ROWPADDING",    (0, 1), (-1, 1),   8),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(cover_tbl)
    story.append(Spacer(1, 16))

    # ── Business health score box ─────────────────────────────────────────────
    score     = _extract_score(report_text)
    s_color   = _score_color(score)
    s_display = f"{score}/10" if score is not None else "N/A"

    score_val_style = ParagraphStyle(
        "ScoreVal",
        fontSize=44, fontName="Helvetica-Bold",
        textColor=s_color, alignment=TA_CENTER, leading=52,
    )
    score_rows = [
        [Paragraph("BUSINESS HEALTH SCORE", styles["score_label"])],
        [Paragraph(s_display, score_val_style)],
        [Paragraph("Overall Assessment", styles["score_label"])],
    ]
    score_tbl = Table(score_rows, colWidths=[pw])
    score_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_GRAY),
        ("TOPPADDING",    (0, 0), (-1, 0),  12),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 12),
        ("ROWPADDING",    (0, 1), (-1, 1),   4),
        ("BOX",           (0, 0), (-1, -1),  1.5, MED_BLUE),
        ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
    ]))
    story.append(score_tbl)
    story.append(Spacer(1, 16))

    # ── Parse body content ────────────────────────────────────────────────────
    content, section_names = _parse_report(report_text, styles)

    # ── Table of contents ─────────────────────────────────────────────────────
    if section_names:
        story.append(HRFlowable(width="100%", thickness=1.5, color=LIGHT_BLUE, spaceAfter=2))
        story.append(Paragraph("TABLE OF CONTENTS", styles["section"]))
        for i, name in enumerate(section_names, 1):
            story.append(Paragraph(f"  {i}.  {name}", styles["toc"]))
        story.append(Spacer(1, 12))
        story.append(PageBreak())

    story.extend(content)

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return path
