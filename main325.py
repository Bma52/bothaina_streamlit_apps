from wsgiref.simple_server import demo_app
import pandas as pd 
import streamlit as st
import numpy as np 

import pycountry
import plotly.express as px
import chart_studio.plotly as pcs
import plotly.offline as py
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode()



st.title("Causes of WorldWide Deaths")
st.markdown("It is important to understand what is meant by the cause of death and the risk factor associated with a premature death. <p>In the epidemiological framework of the Global Burden of Disease study each death has one specific cause. In their own words: ‘each death is attributed to a single underlying cause — the cause that initiated the series of events leading to death</p>", unsafe_allow_html=True)
st.write("Below, in our section on Measurement, you find a more detailed explanation.")

st.markdown("<font size= 5px color='green'> PLEASE NOTE that the dataset is a public one found on Kaggle and it misses date which is an important metric for the below study, as usually we should limit our study to a specific period for a well structured analysis.</font>", unsafe_allow_html=True )
df = pd.read_csv("/Users/bothainaa/Desktop/Death Cause Reason by Country.csv")

df = df.rename(columns={" Alzheimer's disease": 'Alzeheimer disease', "Parkinson's disease": 'Parkinson disease'})



df = pd.melt(df, id_vars='Country Name', value_vars=['Covid-19 Deaths', 'Cardiovascular diseases',
       'Respiratory diseases ', 'Kidney diseases', 'Neonatal disorders ',
       'Meningitis ', 'Malaria ', 'Interpersonal violence', 'HIV/AIDS',
       'Tuberculosis', 'Maternal disorders', 'Lower respiratory infections',
       'Alcohol use disorders', 'Diarrheal diseases', 'Poisoning',
       'Nutritional deficiencies', 'Alzeheimer disease',
       'Parkinson disease', ' Acute hepatitis', 'Digestive diseases',
       ' Cirrhosis and other chronic liver diseases',
       'Protein-energy malnutrition', 'Neoplasms', 'Fire, heat', 'Drowning',
       'Drug use disorders', 'Road injuries',
       'Environmental heat and cold exposure', 'Self-harm',
       ' Conflict and terrorism', 'Diabetes '])


df = df.rename(columns={"variable": 'Disease', "value": 'Deaths'})
df.drop(df.index[df['Country Name'] == 'Israel'], inplace = True)

all_countries = list(df['Country Name'].unique())
all_diseases = list(df['Disease'].unique())

all_countries.append("Select All")
all_diseases.append("Select All")


#country_filter = st.sidebar.selectbox('Filter By Country:', df['Country Name'].unique())
country_filter = st.sidebar.multiselect('Filter By Country:', all_countries, default= all_countries)
disease_filter = st.sidebar.multiselect('Filter By Disease:', all_diseases, default= all_diseases)



df = df[(df["Country Name"].isin(country_filter)) & (df["Disease"].isin(disease_filter))]




#Top 10 countries in terms of deaths 
df_deaths = df.groupby('Country Name').sum('Deaths')

modified = df_deaths.reset_index()

top_10_countries = modified.sort_values('Deaths', ascending = False).head(10)
print(top_10_countries)


#Top 10 Leading deaths in the world 
df_diseases = df.groupby('Disease').sum('Deaths')

modified_disease = df_diseases.reset_index()

top_10_diseases = modified_disease.sort_values('Deaths', ascending = False).head(10)
print(top_10_diseases)

st.write("After Data manipulation and adaptaion to our needs in visualization, data revealed that China is the top country in terms of deaths as deaths reached 10.44M. India came rank 2 in terms of deaths and recorded 8.95M")
data = [go.Bar(x=top_10_countries['Country Name'],
            y=top_10_countries.Deaths, marker=dict(color='#A2D5F2'))]

layout = dict(title = 'Top 10 countires in Terms of Deaths',
              xaxis = dict(title = 'Country'),
              yaxis = dict(title = 'Deaths'),
              )

fig = dict(data=data, layout=layout)
st.plotly_chart(fig)




data2 = [go.Bar(x=top_10_diseases['Disease'],
            y=top_10_diseases.Deaths, marker=dict(color='#ffcdd2'))]

layout2 = dict(title = 'Top 10 Diseases causing Deaths in the World',
              xaxis = dict(title = 'Disease'),
              yaxis = dict(title = 'Deaths'),
              )

fig2 = dict(data=data2, layout=layout2)
st.plotly_chart(fig2)

def findCountry_alpha2 (country_name):
    try:
        return pycountry.countries.get(name=country_name).alpha_2
    except:
        return ("not founded")
    
def findCountry_alpha3 (country_name):
    try:
        return pycountry.countries.get(name=country_name).alpha_3
    except:
        return ("not founded")
    
modified['Country_alpha_2'] = modified.apply(lambda row: findCountry_alpha2(row['Country Name']) , axis = 1)   
modified['Country_alpha_3'] = modified.apply(lambda row: findCountry_alpha3(row['Country Name']) , axis = 1)

fig = px.scatter(df, y="Country Name", x="Deaths", color="Disease", symbol="Disease")
fig.update_traces(marker_size=10)
st.plotly_chart(fig)


fig = px.choropleth(modified, locations="Country_alpha_3",
                    color="Deaths", # lifeExp is a column of gapminder
                    hover_name="Country Name", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig)

df_grouped = df.groupby(["Country Name", "Disease"]).sum("Deaths")







