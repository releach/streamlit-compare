import pandas as pd
import datetime
import streamlit as st

st.title("Compare")
categories = st.file_uploader("Upload categories CSV file", type=["csv"])
grouper = st.file_uploader("Upload grouper CSV file", type=["csv"])

if categories is not None:
    df1 = pd.read_csv(categories)
else:
    st.write("Please upload a categories CSV file.")
    
if grouper is not None:
    df2 = pd.read_csv(grouper)
else:
    st.write("Please upload a grouper CSV file.")


    
unique_to_first = df1[~df1['hwid'].isin(df2['hwid'])]
unique_to_first_count = len(unique_to_first)

concepts_unique_to_first = (
    unique_to_first['concepts']
    .str.split(';', expand=True)
    .stack()
    .str.strip()
    .reset_index(drop=True)
    .drop_duplicates()
    .to_frame(name='concepts')
)

unique_to_second = df2[~df2['hwid'].isin(df1['hwid'])]
unique_to_second_count = len(unique_to_second)

concepts_unique_to_second = (
    unique_to_second['concepts']
    .str.split(';', expand=True)
    .stack()
    .str.strip()
    .reset_index(drop=True)
    .drop_duplicates()
    .to_frame(name='concepts')
)


common_ids = df1[df1['hwid'].isin(df2['hwid'])]
common_to_both_count = len(common_ids)

count_df = pd.DataFrame({'unique to categories': [unique_to_first_count], 'unique to grouper': [unique_to_second_count], 'common to both': [common_to_both_count]})

var = datetime.datetime.now().strftime("%Y%m%d-%H%M")
output_var = f"grouper-compare-{var}.xlsx"

with pd.ExcelWriter(output_var) as writer:
    unique_to_first.to_excel(writer, sheet_name='assets unique to category', index=False)
    concepts_unique_to_first.to_excel(writer, sheet_name='concepts unique to category', index=False)
    unique_to_second.to_excel(writer, sheet_name='assets unique to grouper', index=False)
    common_ids.to_excel(writer, sheet_name='assets common to both', index=False)
    count_df.to_excel(writer,sheet_name='counts', index=False)


with open(output_var, 'rb') as file:
    st.download_button(label="Download the results", 
                    data=file, 
                    file_name=output_var, 
                    mime="application/vnd.ms-excel")
        
