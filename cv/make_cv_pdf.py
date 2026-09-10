#!/usr/bin/env python3
"""Generate the CV as a text-extractable PDF.

Drawn as real text with Helvetica rather than rendered to an image, because an
image-only PDF is invisible to every applicant tracking system - the parser
reads nothing and the application is scored on an empty document.

The layout deliberately mirrors the .docx: one column, standard section names,
contact details in the body.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = A4
LEFT, RIGHT, TOP, BOTTOM = 17 * mm, 17 * mm, 15 * mm, 15 * mm
BODY_W = W - LEFT - RIGHT
ACCENT = HexColor("#1F4E33")
GREY = HexColor("#4A5A50")
RULE = HexColor("#C7D2CA")


class CV:
    def __init__(self, path):
        self.c = canvas.Canvas(path, pagesize=A4)
        self.c.setTitle("Oscar Mureti - Curriculum Vitae")
        self.c.setAuthor("Oscar Mureti")
        self.c.setSubject("Software Developer - Mobile, Web, AI and Machine Learning")
        self.c.setKeywords("Flutter, Dart, Android, iOS, React, Python, "
                           "machine learning, PHP, Firebase, mobile developer, Kenya")
        self.y = H - TOP

    def space(self, pts):
        self.y -= pts

    def _page_break_if_needed(self, needed):
        if self.y - needed < BOTTOM:
            self.c.showPage()
            self.y = H - TOP

    def text(self, s, size=9.6, font="Helvetica", color=None, indent=0, leading=None):
        leading = leading or size + 2.6
        avail = BODY_W - indent
        for line in simpleSplit(s, font, size, avail):
            self._page_break_if_needed(leading)
            self.c.setFont(font, size)
            self.c.setFillColor(color or HexColor("#12211a"))
            self.c.drawString(LEFT + indent, self.y - size, line)
            self.y -= leading

    def heading(self, s):
        self.space(7)
        self._page_break_if_needed(20)
        self.c.setFont("Helvetica-Bold", 10.5)
        self.c.setFillColor(ACCENT)
        self.c.drawString(LEFT, self.y - 10.5, s.upper())
        self.y -= 14
        self.c.setStrokeColor(RULE)
        self.c.setLineWidth(0.6)
        self.c.line(LEFT, self.y + 1, W - RIGHT, self.y + 1)
        self.y -= 5

    def role(self, title, org, dates, bullets):
        self.space(5)
        self._page_break_if_needed(30)
        self.c.setFont("Helvetica-Bold", 10)
        self.c.setFillColor(HexColor("#12211a"))
        self.c.drawString(LEFT, self.y - 10, title)
        self.y -= 12.5
        meta = "  |  ".join(x for x in (org, dates) if x)
        if meta:
            self.c.setFont("Helvetica-Oblique", 9.2)
            self.c.setFillColor(GREY)
            self.c.drawString(LEFT, self.y - 9, meta)
            self.y -= 12
        for b in bullets:
            self._page_break_if_needed(12)
            self.c.setFont("Helvetica", 9.6)
            self.c.setFillColor(HexColor("#12211a"))
            self.c.drawString(LEFT + 4, self.y - 9.6, "•")
            self.text(b, indent=14)
            self.y -= 1

    def labelled(self, label, value):
        self._page_break_if_needed(14)
        self.c.setFont("Helvetica-Bold", 9.6)
        self.c.setFillColor(HexColor("#12211a"))
        w = self.c.stringWidth(label + ": ", "Helvetica-Bold", 9.6)
        self.c.drawString(LEFT, self.y - 9.6, label + ":")
        lines = simpleSplit(value, "Helvetica", 9.6, BODY_W - w)
        self.c.setFont("Helvetica", 9.6)
        self.c.drawString(LEFT + w, self.y - 9.6, lines[0])
        self.y -= 12.2
        for line in lines[1:]:
            self._page_break_if_needed(12)
            self.c.drawString(LEFT + w, self.y - 9.6, line)
            self.y -= 12.2

    def save(self):
        self.c.save()


def build(path):
    cv = CV(path)
    c = cv.c

    c.setFont("Helvetica-Bold", 21)
    c.setFillColor(ACCENT)
    c.drawString(LEFT, cv.y - 21, "OSCAR MURETI")
    cv.y -= 25
    cv.text("Software Developer — Mobile, Web, AI & Machine Learning", size=11)
    cv.space(1)
    cv.text("Nairobi, Kenya  |  +254 707 817 900  |  oscarmureti75@gmail.com", size=9.4, color=GREY)
    cv.text("https://oscarmureti.github.io  |  https://github.com/oscarmureti", size=9.4, color=GREY)

    cv.heading("Professional Summary")
    cv.text("Software developer with seven years building and shipping production "
            "applications across mobile, web and machine learning. Published apps on "
            "Google Play and the App Store, including fintech, public-health and "
            "e-commerce systems used by county governments and businesses in Kenya. "
            "Comfortable owning a product end to end: architecture, implementation, "
            "automated testing, CI/CD and store release.")

    cv.heading("Technical Skills")
    for label, value in [
        ("Mobile", "Flutter, Dart, Android, iOS, React Native"),
        ("Web", "React.js, JavaScript, PHP, Bootstrap, REST APIs, HTML/CSS"),
        ("AI & Machine Learning", "Python, machine learning, data analysis"),
        ("Data & Backend", "Firebase, MySQL, DHIS2, Java, REST API design"),
        ("Practices & Tooling", "Git, GitHub Actions, CI/CD, automated testing, "
                                "Google Play Console, App Store Connect, Xcode, "
                                "Android Studio, server management"),
    ]:
        cv.labelled(label, value)

    cv.heading("Work Experience")
    cv.role("Mobile Developer (iOS and Android)", "Nobuk Africa", "May 2022 – Present", [
        "Build and maintain Android and iOS applications for a fintech platform providing loans to small-scale businesses.",
        "Work across the full mobile stack in Flutter, from feature implementation through release to both app stores.",
    ])
    cv.role("Mobile Developer (iOS and Android)", "Bright Coders Factory East Africa", "January 2022 – Present", [
        "Develop Android and iOS applications for a fintech product, working within a distributed team.",
    ])
    cv.role("CRO / Mobile Developer (iOS and Android)", "Cryosoft Corporation", "September 2018 – Present", [
        "Lead mobile development across the company's product portfolio, including Liquid, CoolPam, Ride Africa, Soi Pallets, Muvi and Music Family.",
        "Deliver both customer-facing and staff-facing applications for the same products, covering ordering, fulfilment and reporting.",
        "Built and published multiple applications to Google Play.",
    ])
    cv.role("Software Developer", "Vihiga County Referral Hospital", "January 2021 – August 2021", [
        "Built a Flutter application for tracking diabetes and hypertension patients across Vihiga County under the HealthIT project.",
        "Enabled clinicians to monitor patient health indicators remotely and prompted patients to record readings and attend appointments.",
    ])
    cv.role("Software Developer", "Kisumu County Ministry of Health", "June 2019 – August 2019", [
        "Developed Kisumu Youth, a mobile platform connecting young people with mentors and enabling them to promote their businesses. Published to Google Play.",
    ])
    cv.role("DHIS2 Applications Developer", "HI4Kenya Bootcamp", "2018", [
        "Contributed to Wajibika, a React Native data-collection tool used by the Ministry of Health, storing collected data into DHIS2.",
    ])

    cv.heading("Selected Projects")
    cv.role("Puzzle Game Portfolio — Wordroot, Solitaire Assured, Sudoku Mentor", "Personal project", "2026", [
        "Three Flutter games on a shared engine, with advertising, in-app purchases, localisation and progression implemented once and reused across all three.",
        "Implemented a Klondike solver proving all 4,023 shipped deals winnable before release, and a sudoku engine grading 5,493 puzzles by the solving technique each requires rather than by clue count.",
        "Localised to 12 languages, covered by 44 automated tests, and released through a GitHub Actions pipeline deploying to Google Play and TestFlight on merge.",
    ])
    cv.role("DairyVibes", "Published on Google Play", "", [
        "Dairy farm management application covering milk records, herd, health and feed tracking. Flutter and Firebase.",
    ])
    cv.role("CoolPam Management", "Cryosoft Corporation", "", [
        "Water management system spanning Android and iOS applications, an admin website in React.js and a desktop administration tool.",
    ])
    cv.role("Liquid and Liquid Staff", "Cryosoft Corporation", "", [
        "Food-delivery marketplace plus the staff application handling order receipt, processing, delivery and revenue reporting. Flutter, Firebase, PHP and Google Maps.",
    ])

    cv.heading("Education")
    cv.role("BSc, Mathematics and Computer Science", "Maseno University", "2016 – 2020", [])

    cv.heading("Languages")
    cv.text("English (fluent)  |  Kiswahili (native)")

    cv.save()
    return path


if __name__ == "__main__":
    p = build(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "Oscar-Mureti-CV.pdf"))
    print(f"  wrote {p} ({os.path.getsize(p)/1024:.0f} KB)")
