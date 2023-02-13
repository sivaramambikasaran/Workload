# Required python packages
import streamlit as st
import pandas as pd
import numpy as np
import workLoad as wl
from pathlib import Path


st.title('Work Load Manager')
st.write("Department of Mathematics, IIT Madras")
st.subheader('Data dependencies')
st.write("Please upload the following files in .csv format")
file1 = st.file_uploader("Upload Course Faculty requirement")
file2 = st.file_uploader("Upload Faculty preference sheet")

odd2023 = wl.allotment()
df_pref = pd.DataFrame()
df_allot = pd.DataFrame()
odd2023.set_faculty()
odd2023.set_courses()


with st.form("Process data"):
   # Every form must have a submit button.
   submitted = st.form_submit_button("Process")
   if submitted:
       odd2023.update_requirements(file1)  # 'facultyRequirement_ug.csv'
       odd2023.extract_preferences(file2)
       pre_out = odd2023.show_course_fac_preference_table()
       st.write(len(pre_out))
       df_pref = pd.DataFrame(pre_out)
       df_pref.replace(str(np.nan), " ")

st.write(df_pref)


def convert_df(df_):
   return df_.to_csv(index=False).encode('utf-8')


csv_pref = convert_df(df_pref)

st.write("To download the above table in csv format")
st.write("click below to download in csv format")
st.download_button(
    ".csv",
    csv_pref,
    "Course_Faculty_Preference.csv",
    "text/csv",
    key='download-csv'
)
del df_pref

st.subheader('UG Course allotment')
with st.form("UG allotment"):
   st.write("Proceed with the UG course allotment based on above preference")
   # Every form must have a submit button.
   submitted = st.form_submit_button("Proceed")
   if submitted:
       odd2023.update_requirements(file1)  # 'facultyRequirement_ug.csv'
       odd2023.extract_preferences(file2)
       odd2023.compute_provisional_allotment_ug()
       df_allot = odd2023.generate_allotment()
       st.dataframe(df_allot)
       odd2023.get_tab_course_fac()
       is_ug_done = True

st.subheader("Download allotment")
my_file1 = Path("./output_file_1.pdf")
if my_file1.is_file():
    with open("output_file_1.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Course - Faculty pdf",
                       data=PDFbyte,
                       file_name="WorkLoad.pdf",
                       mime='application/octet-stream')
my_file2 = Path("./output_file_2.pdf")
if my_file2.is_file():
    with open("output_file_2.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(label="Faculty - Course pdf",
                       data=PDFbyte,
                       file_name="WorkLoad.pdf",
                       mime='application/octet-stream')
