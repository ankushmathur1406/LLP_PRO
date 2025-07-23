import streamlit as st
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

st.title("📄 All Parts Availability Results")

def generate_pdf(df, title):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [Paragraph(title, styles['Heading2'])]
    data = [df.columns.tolist()] + df.values.tolist()
    table = Table(data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    elements.append(table)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

if 'merged_df' in st.session_state:
    df = st.session_state['merged_df']
    st.dataframe(df)

    # PDF & CSV downloads
    pdf = generate_pdf(df, "All Parts Availability Results")
    st.download_button("📄 Download Full Result as PDF", pdf, file_name="full_result.pdf")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📄 Download Full Result as CSV", csv, file_name="full_result.csv")
else:
    st.warning("⚠️ Please upload and process data from the Home page.")
