import pandas as pd
import datetime
import streamlit as st
import plotly.express as px
import openpyxl



#setting the title
st.set_page_config(page_title='Data Quality Dashboard',page_icon='C://Users/CZ0202/OneDrive - cozentus.com/tasks/image.png',layout='wide')

#background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #e5e5f7;
opacity: 0.9;
background-image:  repeating-radial-gradient( circle at 0 0, transparent 0, #e5e5f7 4px ), repeating-linear-gradient( #fafafe55, #fafafe );
    }
    </style>
    """,
    unsafe_allow_html=True
)

data = pd.read_excel("C:/Users/CZ0202/Tracker.xlsx")
data['Issue raised date'] = pd.to_datetime(data['Issue raised date'])

#creating image sidebar
st.sidebar.video("C://Users/CZ0202/OneDrive - cozentus.com/tasks/cargo.mp4",start_time=0)
#creating sidebar widgets
status_filter = st.sidebar.selectbox("Status", ["ALL"] + list(data['Status'].unique()), index=0)
carrier_filter = st.sidebar.selectbox("Source of Shipment", ["ALL"] + list(data["Source of Shipment"].unique()), index=0)
issue_type_filter = st.sidebar.selectbox("Issue Type", ["ALL"] + list(data["Issue type"].unique()), index=0)
#category_filter = st.sidebar.selectbox("Generic Issue Category", data["Generic Issue Category"].unique(), index=0)




# Making the filter work
#data_selection = data.query("Status == @status_filter and `Source of Shipment` == @carrier_filter and `Issue Type` == @issue_type_filter")

filtered_data = data.copy()
if status_filter != "ALL":
    filtered_data = filtered_data[filtered_data["Status"] == status_filter]
if carrier_filter != "ALL":
    filtered_data = filtered_data[filtered_data["Source of Shipment"] == carrier_filter]
if issue_type_filter != "ALL":
    filtered_data = filtered_data[filtered_data["Issue type"] == issue_type_filter]
#if category_filter:
    #filtered_data = filtered_data[filtered_data["Generic Issue Category"] == category_filter]

#Title and modifing the main page
st.title("Data Quality Dashboard")

#Fetching the plots based on the category
if status_filter == "ALL" and carrier_filter == "ALL" and issue_type_filter == "ALL":
    total_counts = len(data)
    total_error_count = len(data[data["Status"] == "Error"])
    fine_count = len(data[data["Status"] == "Fine"])
    error_percentage = (total_error_count/total_counts) * 100
    fine_percentage = (fine_count / total_counts) * 100

    plot_data = pd.DataFrame({
    'Status':['Error','Fine'],
    'Percentage':[error_percentage,fine_percentage]
    })

    color_new = {'Error': 'red' , 'Fine': 'green'}
    error_percentage_plot = px.bar(plot_data,x="Status",y="Percentage",title="Error/Fine %",color='Status', color_discrete_map= color_new)
    source_of_shipment = data['Source of Shipment'].value_counts().reset_index()
    source_of_shipment.columns = ['Source of shipment','Number of Shipments']
    source_of_shipment_plot = px.pie(source_of_shipment,values="Number of Shipments",names="Source of shipment",title="Shipment_Source_Count")
    issue_type = data['Issue type'].value_counts().reset_index()
    issue_type.columns = ['Issue_type','Frequency']
    fig = px.scatter(issue_type ,x="Issue_type",y="Frequency",color='Frequency',hover_data=['Issue_type','Frequency'],title="Issue_type_Count",labels={'Frequency': 'Frequency'})
    
    fig.update_layout(
    showlegend=True,
    plot_bgcolor='red',
    xaxis=dict(title='Issue_Type'),
    yaxis=dict(title='Frequency'),
    font=dict(size=30),
    width=950,
    height=500
    )

    generic_issue = data["Generic Issue Category"].value_counts().reset_index()
    generic_issue.columns = ['Generic Issue','Frequency']
    category_plot = px.sunburst(data, path=["Generic Issue Category"], title="Generic Issue Category Count")

#Error/Fine Percentage plot
#calculating the error/Fine percentage 
else:
    total_counts = len(filtered_data)
    total_error_count = len(filtered_data[filtered_data["Status"] == "Error"])
    fine_count = len(filtered_data[filtered_data["Status"] == "Fine"])
    error_percentage = (total_error_count/total_counts) * 100
    fine_percentage = (fine_count / total_counts) * 100

    plot_data = pd.DataFrame({
    'Status':['Error','Fine'],
    'Percentage':[error_percentage,fine_percentage]
    })

    color_new = {'Error': 'red' , 'Fine': 'green'}
    error_percentage_plot = px.bar(plot_data,x="Status",y="Percentage",title="Error/Fine %",color='Status', color_discrete_map= color_new)
    source_of_shipment = filtered_data['Source of Shipment'].value_counts().reset_index()
    source_of_shipment.columns = ['Source of shipment','Number of Shipments']
    source_of_shipment_plot = px.pie(source_of_shipment,values="Number of Shipments",names="Source of shipment",title="Shipment_Source_Count")
    issue_type = filtered_data['Issue type'].value_counts().reset_index()
    issue_type.columns = ['Issue_type','Frequency']
    #creating bubble chart
    fig = px.scatter(issue_type ,x="Issue_type",y="Frequency",color='Frequency',hover_data=['Issue_type','Frequency'],title="Issue_type_Count",labels={'Frequency': 'Frequency'})
    
    fig.update_layout(
    showlegend=True,
    plot_bgcolor='red',
    xaxis=dict(title='Issue_Type'),
    yaxis=dict(title='Frequency'),
    font=dict(size=30),
    width=950,
    height=500
    )

#creating sunburst chart
    generic_issue = filtered_data["Generic Issue Category"].value_counts().reset_index()
    generic_issue.columns = ['Generic Issue','Frequency']
    category_plot = px.sunburst(data, path=["Generic Issue Category"], title="Generic Issue Category Count")

#displaying side by side
#column1,column2 = st.columns(2)
#column1.plotly_chart(error_percentage_plot)
#column1.plotly_chart(fig)
#column2.plotly_chart(source_of_shipment_plot)
#column2.plotly_chart(category_plot)
#Displaying in separate lines
st.plotly_chart(error_percentage_plot)
st.plotly_chart(source_of_shipment_plot)
st.plotly_chart(fig)
st.plotly_chart(category_plot)
st.dataframe(filtered_data)

#hiding the default streamlit things like Made with streamlit,Menu button etc
hide_style = """
             <style>
             #MainMenu {visibility: hidden}
             footer {visibility: hidden;}
             header {visibility: hidden}
             </style>
             """

st.markdown(hide_style,unsafe_allow_html=True)

#changing the background color
