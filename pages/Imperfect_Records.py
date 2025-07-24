import streamlit as st
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

st.title("Imperfect Records: Short / More")

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
    filtered = df[df['result'] != 'ok']

    if not filtered.empty:
        st.dataframe(filtered)

        pdf = generate_pdf(filtered, "Imperfect Records (Short / More)")
        st.download_button("📄 Download Imperfect Records as PDF", pdf, file_name="imperfect_result.pdf")

        csv = filtered.to_csv(index=False).encode('utf-8')
        st.download_button("📄 Download Imperfect Records as CSV", csv, file_name="imperfect_result.csv")
    else:
        st.success("All records are OK. No imperfections found.")
else:
    st.warning("Please upload and process data from the Home page.")
