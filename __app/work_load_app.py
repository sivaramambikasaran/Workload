# Required python packages
import streamlit as st
import pandas as pd
import numpy as np

st.title('Work Load Manager')
st.write("Department of Mathematics, IIT Madras")
st.subheader('Data dependencies')
st.write("Please upload the following files in .csv format.")
file1 = st.file_uploader("Upload Course Faculty requirement..")
file2 = st.file_uploader("Upload Faculty preference sheet..")
slider_val = 10
checkbox_val = 100
is_ug_done = False

st.subheader('UG Course allotment')
with st.form("UG allotment"):
   st.write("Proceed with the UG course allotment")
   # Every form must have a submit button.
   submitted = st.form_submit_button("Proceed")
   if submitted:
       st.write("slider", slider_val, "checkbox", checkbox_val)
       is_ug_done = True
with st.form("Update UG allotment"):
   st.write("If modifications needed please upload appropriate files !!")
   file3 = st.file_uploader("Upload Course Faculty modifications..")
   # Every form must have a submit button.
   submitted = st.form_submit_button("Proceed")
   if submitted:
      if is_ug_done:
         pass
      else:
         st.write("Perfom UG allotment ... ")
      

st.subheader('PG Course allotment')
with st.form("PG allotment"):
   st.write("Proceed with the PG course allotment")
   # Every form must have a submit button.
   submitted = st.form_submit_button("Proceed")
   if submitted:
       st.write("slider", slider_val, "checkbox", checkbox_val)
       is_ug_done = True
with st.form("Update PG allotment"):
   st.write("If modifications needed please upload appropriate files !!")
   file3 = st.file_uploader("Upload Course Faculty modifications..")
   # Every form must have a submit button.
   submitted = st.form_submit_button("Proceed")
   if submitted:
      if is_ug_done:
         pass
      else:
         st.write("Perfom PG allotment ... ")


st.subheader('Provisional allotment')
st.write("Following formats are available for download")
df = pd.read_csv('Teaching_Preference.csv')


@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.download_button(
    "Download .csv",
    csv,
    "WorkLoad.csv",
    "text/csv",
    key='download-csv'
)

with open("sample.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="Download .pdf",
                   data=PDFbyte,
                   file_name="WorkLoad.pdf",
                   mime='application/octet-stream')

