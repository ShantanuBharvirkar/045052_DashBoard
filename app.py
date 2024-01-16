import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read your CSV data
df = pd.read_csv('/content/marketing_data.csv')

# Data Cleaning
# Check for missing values
missing_values = df.isnull().sum()

# Convert 'Year_Birth' to datetime
df['Year_Birth'] = pd.to_datetime(df['Year_Birth'], format='%Y')

# Convert 'Dt_Customer' to datetime
df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'])

# Convert 'Income' to numerical (remove dollar sign and convert to float)
df['Income'] = df['Income '].str.replace('[\$,]', '', regex=True).astype(float)

# Streamlit app initialization
st.title('Marketing Analytics and Customer Satisfaction Dashboard')

# Marketing Analytics Dashboard components
st.header("Marketing Analytics Dashboard")

# Dropdown for selecting country
selected_country = st.selectbox("Select a Country", df['Country'].unique(), index=0)

# Filter data based on selected country
filtered_marketing_data = df[df['Country'] == selected_country]

# Bar chart: Total spending on different product categories
bar_chart = px.bar(x=['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'],
                  y=[filtered_marketing_data[col].sum() for col in ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']],
                  labels={'x': 'Product Categories', 'y': 'Total Spending'},
                  title=f'Total Spending on Products in {selected_country}')

# Pie chart: Acceptance of marketing campaigns
campaign_cols = [f'AcceptedCmp{i}' for i in range(1, 6)]
pie_chart = px.pie(names=campaign_cols, values=[filtered_marketing_data[col].sum() for col in campaign_cols], title=f'Acceptance of Marketing Campaigns in {selected_country}')

# Display charts
st.plotly_chart(bar_chart)
st.plotly_chart(pie_chart)

# Customer Satisfaction Dashboard components
st.header('Customer Satisfaction and Loyalty Dashboard')

# Select Time Period Range
selected_years = st.slider('Select Time Period', min_value=df['Dt_Customer'].dt.year.min(), max_value=df['Dt_Customer'].dt.year.max(), value=[df['Dt_Customer'].dt.year.min(), df['Dt_Customer'].dt.year.max()])

# Calculate overall satisfaction based on filtered data
filtered_df = df[(df['Dt_Customer'].dt.year >= selected_years[0]) & (df['Dt_Customer'].dt.year <= selected_years[1])]
overall_satisfaction = filtered_df['Response'].mean()

# Create updated satisfaction gauge figure
satisfaction_gauge_figure = go.Figure(go.Indicator(
    mode="gauge+number",
    value=overall_satisfaction,
    title={'text': 'Satisfaction'},
    gauge={'axis': {'range': [None, 1]}, 'bar': {'color': "darkblue"}},
))

# Dropdown for Education Level
selected_education = st.selectbox('Education Level', df['Education'].unique(), index=0)

# Dropdown for Marital Status
selected_marital_status = st.selectbox('Marital Status', df['Marital_Status'].unique(), index=0)

# Filter the data based on user input for Customer Satisfaction
filtered_education_data = df[
    (df['Education'] == selected_education) &
    (df['Marital_Status'] == selected_marital_status)
]

# Stacked Bar Chart: Distribution of spending over the years
stacked_bar_chart = px.bar(
    x=filtered_education_data['Year_Birth'],
    y=filtered_education_data['Income'],
    labels={'x': 'Year of Birth', 'y': 'Income'},
    title=f'Income Distribution for {selected_education}'
)

# Scatter Plot: Income Trend Over Time
scatter_plot = px.scatter(
    x=filtered_education_data['Year_Birth'],
    y=filtered_education_data['Income'],
    labels={'x': 'Year of Birth', 'y': 'Income'},
    title=f'Income Trend Over Time for {selected_education}',
)


# Display charts
st.plotly_chart(satisfaction_gauge_figure)
st.plotly_chart(stacked_bar_chart)
st.plotly_chart(scatter_plot)

# Run the app
