import streamlit as st
import pandas as pd

st.set_page_config(page_title="Parts Availability Checker", layout="wide")
st.title("Upload & Process Files")

table1 = st.file_uploader("Upload Parts Count Table (Excel or CSV)", type=['xlsx', 'csv'])
table2 = st.file_uploader("Upload Part Details Table (Excel or CSV)", type=['xlsx', 'csv'])

if table1 and table2:
    try:
        df1 = pd.read_excel(table1) if table1.name.endswith('.xlsx') else pd.read_csv(table1)
        df2 = pd.read_excel(table2) if table2.name.endswith('.xlsx') else pd.read_csv(table2)

        df1.columns = df1.columns.str.strip().str.lower()
        df2.columns = df2.columns.str.strip().str.lower()

        df2.rename(columns={
            'desc': 'part_desc',
            'part_nu': 'part_number',
            'serial_r': 'serial_number'
        }, inplace=True)

        required_cols = ['a/c', 'part_number', 'part_desc']
        missing = [col for col in required_cols if col not in df2.columns]

        if missing:
            st.error(f"Missing columns: {missing}")
        else:
            llp_row = df1[df1['a/c'].str.lower().str.contains('llp')].iloc[0].drop('a/c')
            df1_clean = df1[~df1['a/c'].str.lower().str.contains('llp')]

            results = []
            for _, row in df2.iterrows():
                ac = row['a/c']
                part_number = row['part_number']
                part_desc = row['part_desc'].strip()
                required = int(llp_row.get(part_desc.lower(), 0))

                match = df1_clean[df1_clean['a/c'] == ac]
                available = int(match[part_desc.lower()].values[0]) if not match.empty and part_desc.lower() in match.columns else 0

                if available == required:
                    result = "ok"
                elif available > required:
                    result = "more"
                else:
                    result = "short"

                results.append({
                    "A/C": ac,
                    "part_number": part_number,
                    "part_desc": part_desc,
                    "required": required,
                    "available": available,
                    "result": result
                })

            merged_df = pd.DataFrame(results)
            st.session_state['merged_df'] = merged_df

            st.success("✅ Data processed successfully!")
            st.info("Go to the sidebar and open 'Full Result' or 'Imperfect Records' to view results.")
    except Exception as e:
        st.error(f"❌ Error: {e}")