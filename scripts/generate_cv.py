#!/usr/bin/env python3
"""Generate the downloadable CV from the public portfolio pages."""

from argparse import ArgumentParser
from html.parser import HTMLParser
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import HRFlowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer
import reportlab


def clean(value: str) -> str:
    value = re.sub(r"[\U00010000-\U0010ffff]", "", value)
    return re.sub(r"\s+", " ", value).strip()


class TimelineCardParser(HTMLParser):
    """Extracts visible timeline cards from the static portfolio HTML."""

    def __init__(self):
        super().__init__()
        self.cards = []
        self.card_depth = 0
        self.current = None
        self.capture = None
        self.buffer = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "")
        if tag == "div" and "card" in classes and "exp-card" in classes and self.current is None:
            self.current = {"title": "", "meta": "", "items": []}
            self.card_depth = 1
            return
        if self.current is not None and tag == "div":
            self.card_depth += 1
        if self.current is not None and tag in {"h3", "p", "li"}:
            self.capture = tag
            self.buffer = []

    def handle_data(self, data):
        if self.capture:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        if self.current is not None and tag == self.capture:
            value = clean("".join(self.buffer))
            if value:
                if self.capture == "h3":
                    self.current["title"] = value
                elif self.capture == "p":
                    self.current["meta"] = value
                elif self.capture == "li":
                    self.current["items"].append(value)
            self.capture = None
            self.buffer = []
        if self.current is not None and tag == "div":
            self.card_depth -= 1
            if self.card_depth == 0:
                if self.current["title"]:
                    self.cards.append(self.current)
                self.current = None


def read_cards(path: Path):
    parser = TimelineCardParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.cards


def paragraph(text, style):
    return Paragraph(text.replace("&", "&amp;"), style)


def section(title, body, styles):
    return [
        Spacer(1, 0.18 * cm),
        paragraph(title.upper(), styles["section"]),
        HRFlowable(width="100%", thickness=0.7, color=colors.HexColor("#7ec4cf"), spaceBefore=2, spaceAfter=6),
        *body,
    ]


def card_block(card, styles):
    content = [paragraph(card["title"], styles["role"])]
    if card["meta"]:
        content.append(paragraph(card["meta"], styles["meta"]))
    for item in card["items"]:
        content.append(paragraph(f"• {item}", styles["bullet"]))
    return KeepTogether(content + [Spacer(1, 0.10 * cm)])


def build(site_root: Path, output: Path):
    experiences = read_cards(site_root / "esperienze.html")
    technical_experiences = [card for card in experiences if "Sistemista" in card["title"]]
    complementary_experiences = [card for card in experiences if card not in technical_experiences]
    learning = read_cards(site_root / "formazione.html")
    certificates = []
    education = []
    certificate_keywords = ("Sophos", "Sangfor", "Veeam")
    for card in learning:
        (certificates if card["title"].startswith(certificate_keywords) else education).append(card)

    contacts = (site_root / "contatti.html").read_text(encoding="utf-8")
    email_match = re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", contacts)
    email = email_match.group(0) if email_match else ""

    output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(output), pagesize=A4, rightMargin=1.55 * cm, leftMargin=1.55 * cm,
        topMargin=1.35 * cm, bottomMargin=1.35 * cm,
        title="Curriculum - Diego Serpelloni", author="Diego Serpelloni",
    )
    font_directory = Path(reportlab.__file__).resolve().parent / "fonts"
    pdfmetrics.registerFont(TTFont("Portfolio", str(font_directory / "Vera.ttf")))
    pdfmetrics.registerFont(TTFont("Portfolio-Bold", str(font_directory / "VeraBd.ttf")))
    sample = getSampleStyleSheet()
    styles = {
        "name": ParagraphStyle("name", parent=sample["Title"], fontName="Portfolio-Bold", fontSize=24, leading=28, textColor=colors.HexColor("#2f3e46"), spaceAfter=3),
        "headline": ParagraphStyle("headline", parent=sample["Normal"], fontName="Portfolio-Bold", fontSize=10.5, leading=14, textColor=colors.HexColor("#5ca4b0"), spaceAfter=8),
        "contact": ParagraphStyle("contact", parent=sample["Normal"], fontName="Portfolio", fontSize=8.7, leading=12, textColor=colors.HexColor("#47565e"), spaceAfter=10),
        "section": ParagraphStyle("section", parent=sample["Heading2"], fontName="Portfolio-Bold", fontSize=10, leading=12, textColor=colors.HexColor("#2f3e46"), spaceAfter=0),
        "role": ParagraphStyle("role", parent=sample["Normal"], fontName="Portfolio-Bold", fontSize=10.2, leading=13, textColor=colors.HexColor("#2f3e46"), spaceAfter=1),
        "meta": ParagraphStyle("meta", parent=sample["Normal"], fontName="Portfolio", fontSize=8.8, leading=11, textColor=colors.HexColor("#5b6a72"), spaceAfter=3),
        "body": ParagraphStyle("body", parent=sample["Normal"], fontName="Portfolio", fontSize=9.1, leading=13, textColor=colors.HexColor("#2f3e46"), spaceAfter=4),
        "bullet": ParagraphStyle("bullet", parent=sample["Normal"], fontName="Portfolio", fontSize=8.7, leading=11.5, leftIndent=7, firstLineIndent=-7, textColor=colors.HexColor("#35464f"), spaceAfter=1),
        "compact": ParagraphStyle("compact", parent=sample["Normal"], fontName="Portfolio", fontSize=8.8, leading=12, textColor=colors.HexColor("#35464f"), spaceAfter=2),
    }
    story = [
        paragraph("Diego Serpelloni", styles["name"]),
        paragraph("Sistemista Junior | Sistemi, Cloud, Backup e Cybersecurity", styles["headline"]),
        paragraph(f"Verona, Italia  |  {email}  |  linkedin.com/in/diego-serpelloni-31ba80235  |  github.com/serpico3", styles["contact"]),
        HRFlowable(width="100%", thickness=1.4, color=colors.HexColor("#7ec4cf"), spaceBefore=0, spaceAfter=8),
    ]
    story += section("Profilo", [paragraph("Sistemista junior in apprendistato presso Infoteam Verona. Mi occupo di infrastrutture Windows e Linux, Microsoft 365, virtualizzazione, backup e sicurezza di rete, con un approccio pratico alla risoluzione dei problemi e alla documentazione tecnica.", styles["body"])], styles)
    story += section("Competenze principali", [paragraph("Windows Server, Active Directory, DNS, DFS, Linux, Microsoft 365, Entra ID, Intune, Microsoft Defender, VMware vSphere, ESXi, vCenter, Hyper-V, Veeam, Sophos, WatchGuard, Cisco Meraki, VLAN, VPN, Docker, Nextcloud e LDAP.", styles["body"])], styles)
    experience_body = [card_block(card, styles) for card in technical_experiences]
    if complementary_experiences:
        experience_body.append(paragraph("Esperienze complementari", styles["role"]))
        experience_body.extend(
            paragraph(f"• {card['title']} - {card['meta']}", styles["compact"])
            for card in complementary_experiences
        )
    story += section("Esperienze professionali", experience_body, styles)
    story += [PageBreak()]
    story += section("Formazione", [card_block(card, styles) for card in education], styles)
    story += section("Certificazioni", [paragraph(f"• {card['title']} - {card['meta']}", styles["compact"]) for card in certificates], styles)
    story += [Spacer(1, 0.16 * cm), paragraph("Curriculum generato automaticamente dalle sezioni Esperienze e Formazione del sito diegoserpelloni.com.", ParagraphStyle("footer", parent=styles["compact"], fontName="Portfolio", fontSize=7.4, textColor=colors.HexColor("#708089")))]
    document.build(story)


if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument("--site-root", default=".")
    args.add_argument("--output", default="assets/curriculum-diego-serpelloni.pdf")
    parsed = args.parse_args()
    build(Path(parsed.site_root), Path(parsed.output))