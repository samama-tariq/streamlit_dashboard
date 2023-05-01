import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gspread

service_account = gspread.service_account(filename="service_file.json")
sh = service_account.open("data")
ws = sh.worksheet("data")

products = pd.Series(ws.col_values(1), name="products")[1:]
issues = pd.Series(ws.col_values(2), name="issues")[1:]
sub_product = pd.Series(ws.col_values(3), name="sub_products")[1:]
timely = pd.Series(ws.col_values(4), name="timely")[1:]
company_response = pd.Series(ws.col_values(5), name="company_response")[1:]
submitted_via = pd.Series(ws.col_values(6), name="submitted_via")[1:]
company = pd.Series(ws.col_values(7), name="company")[1:]
month_end = pd.Series(ws.col_values(8), name="month_end")[1:]
state = pd.Series(ws.col_values(9), name="state")[1:]
sub_issue = pd.Series(ws.col_values(10), name="sub_issue")[1:]
count_distinct = pd.Series(ws.col_values(11), name="count_distinct")[1:]

df = pd.concat([products, issues, sub_product, timely, company_response,
               submitted_via, company, month_end, state, sub_issue, count_distinct], axis=1)
# st.write(df)
st.set_page_config(
    page_title="Financial Consumer Complaints",
    layout="wide"
)
st.header('Financial Consumer Complaints')
st.markdown('Select a state')
state_list = df["state"].drop_duplicates()
option = st.selectbox('All States', state_list)

st.subheader(f'Display Data For {option}')

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    sum_value = df["count_distinct"]
    summ = 0
    for i in sum_value:
        summ = summ+int(i)
    st.metric(label="Number of Complaints",
              value=str(summ))

with col2:
    having_close = df["company_response"].str.contains("Close", regex=False)
    st.metric(label="Number of Complaints with Closed status",
              value=str(having_close.sum()))

with col3:
    num_of_yes_response = df["timely"].str.contains("Yes", regex=False)
    st.metric(label=" % of Timely Response Complaints",
              value=str(round((num_of_yes_response.sum()*100)/summ, 2)))

with col4:
    in_progress = df["company_response"].str.contains(
        "In progress", regex=False)
    st.metric(label="Number of Complaints with In Progress",
              value=str(in_progress.sum()))

with col5:
    option2 = st.selectbox('Select State',
                           state_list,
                           )

col6, col7 = st.columns(2)
with col6:
    product_count_df = df.groupby('products')['count_distinct'].count()
    st.bar_chart(product_count_df)

with col7:
    df['month_end'] = pd.to_datetime(df['month_end'])
    df['month_year'] = df['month_end'].dt.strftime('%Y-%m')
    month_year_count_df=df.groupby('month_year')['count_distinct'].count()
    st.line_chart(month_year_count_df)

col8, col9 = st.columns(2)

with col8:
    df['count_distinct'] = pd.to_numeric(df['count_distinct'])
    submitted_via_complaints_df = df.groupby('submitted_via')['count_distinct'].count()
    pie_chart = px.pie(submitted_via_complaints_df, values='count_distinct', names=['Phone','Postal mail','Referral','Web','Web Referral'])
    pie_chart.update_traces( textinfo='value')
    pie_chart.update_layout(title='Total Number of Complaints by Channel')
    col8.plotly_chart(pie_chart, use_container_width=True)


with col9:
    group_df = df.groupby(["issues", "sub_issue"])["count_distinct"].count().reset_index()
    tree_chart = px.treemap(group_df, path=['issues', 'sub_issue'], values='count_distinct')
    tree_chart.update_layout(title='Number of Complaints by Issue and Sub-Issue', 
                  xaxis_title='Issue', 
                  yaxis_title='Sub-Issue' 
                  )
    col9.plotly_chart(tree_chart, use_container_width=True)

st.write("Designed by Muhammad Samama CDE B4")