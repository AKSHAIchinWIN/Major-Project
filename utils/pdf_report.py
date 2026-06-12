from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf_report(score, advice):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "AI Resume Analysis Report",
        styles["Title"]
    )

    content.append(title)

    content.append(Spacer(1, 12))

    score_text = Paragraph(
        f"<b>Resume Match Score:</b> {score}%",
        styles["Normal"]
    )

    content.append(score_text)

    content.append(Spacer(1, 12))

    advice_title = Paragraph(
        "<b>AI Career Advice</b>",
        styles["Heading2"]
    )

    content.append(advice_title)

    content.append(Spacer(1, 12))

    advice_para = Paragraph(
        advice.replace("\n", "<br/>"),
        styles["Normal"]
    )

    content.append(advice_para)

    doc.build(content)

    buffer.seek(0)

    return buffer