import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Search by A/C")

st.title("Search Aircraft Parts by A/C")


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
    merged_df = st.session_state['merged_df']
    ac_list = merged_df['A/C'].unique().tolist()

    st.subheader("Select Aircraft and Filter")

    selected_ac = st.selectbox("✈️ Select Aircraft", options=ac_list)
    filter_option = st.radio("Show:", ["All", "Only Imperfect"], horizontal=True)

    
    filtered_df = merged_df[merged_df['A/C'] == selected_ac]
    if filter_option == "Only Imperfect":
        filtered_df = filtered_df[filtered_df['result'] != "ok"]

    if not filtered_df.empty:
        st.subheader(f"Results for A/C: {selected_ac} ({filter_option})")
        st.dataframe(filtered_df)

        
        pdf = generate_pdf(filtered_df, f"Parts for A/C {selected_ac} ({filter_option})")
        st.download_button("📄 Download as PDF", pdf, file_name=f"{selected_ac}_filtered.pdf")

        
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button("📄 Download as CSV", csv, file_name=f"{selected_ac}_filtered.csv")
    else:
        st.warning("No matching records found.")
else:
    st.warning("Please upload and process data from the Home page first.")
