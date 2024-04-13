#---------------------------- Libraries ----------------------------------
import pandas as pd
import re
import plotly
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config(page_title='Countries',page_icon='📈',layout='wide')

#=========================================================================

#---------------------------- Functions ----------------------------------

#=========================================================================

#Create the bar graphic of the number of cities selected with the most different types of cuisine:
def qtd_cuisine():
    df1_aux=(df1.loc[:,['Country Name','City','Cuisines']]
               .groupby(['City','Country Name'])
               .nunique()
               .sort_values(by='City',ascending=False)
               .reset_index())
    df1_aux=df1_aux.iloc[:cities_select]
    fig=px.bar(df1_aux,x='City',y='Cuisines',text_auto=True,labels={'City':'Cities', 'Cuisines':'Quantity of Cuisines','Country':'Countries'},color='Country Name')
    fig.update_layout(title={'text':f'Top {cities_select} cities with restaurants with the most different types of cuisine','x':0.5,'xanchor':'center'})
    st.plotly_chart(fig,use_container_width=True)

#Creates a bar graph with the highest and lowest ratings of restaurants according to the selection of countries and quantities
def top_rating(note,bigger=True):
    if bigger:
        df1_aux=(df1.loc[df['Aggregate rating']>note,['City','Country Name','Aggregate rating']]
                    .groupby(['Country Name','City'])
                    .count()
                    .sort_values(by='Aggregate rating',ascending=False)
                    .reset_index())
        df1_aux=df1_aux.iloc[:cities_select]
        fig=px.bar(df1_aux,x='City',y='Aggregate rating',text_auto='Restaurant ID',labels={'City':'Cities', 'Aggregate rating':'Rating', 'Country':'Countries'},color='Country Name')
        fig.update_layout(title={'text':f'Top {cities_select} cities with restaurants with an average rating above {note}','x':0.5,'xanchor':'center'})
    else:
        df1_aux = (df1.loc[df['Aggregate rating']<note,['City','Country Name','Aggregate rating']]
                      .groupby(['Country Name','City'])
                      .count()
                      .sort_values(by='Aggregate rating',ascending=False)
                      .reset_index())
        df1_aux=df1_aux.iloc[:cities_select]
        fig=px.bar(df1_aux,x='City',y='Aggregate rating',text_auto='Restaurant ID',labels={'City':'Cities', 'Aggregate rating':'Rating', 'Country':'Countries'},color='Country Name')
        fig.update_layout(title={'text':f'Top {cities_select} cities with restaurants with an average rating below {note}','x':0.5,'xanchor':'center'})
    st.plotly_chart(fig,use_container_width=True)
    
#Create a bar graphic with the most quantity of restaurants by cities: 
def top_cities():
    df1_aux=(df1.loc[:, ['City','Restaurant ID','Country Name']]
                .groupby(['Country Name','City'])
                .count()
                .sort_values(by='Restaurant ID',ascending=False)
                .reset_index())
    df1_aux=df1_aux.iloc[:cities_select]
    fig=px.bar(df1_aux,x='City',y='Restaurant ID',text_auto='Restaurant ID',labels={'City':'Cities', 'Restaurant ID':'Quantity of Restaurants','Country Name':'Countries'},color='Country Name')
    fig.update_layout(title={'text':f'Top {cities_select} cities with the most restaurants','x':0.5,'xanchor':'center'})
    st.plotly_chart(fig,use_container_width=True)
    return fig

#=========================================================================

#--------------------- Preparing DataFrame -------------------------------

#=========================================================================

# Group of countries by codes:
countries = {1: 'India',
 189: 'South Africa',
 214: 'The United Arab Emirates',
 191: 'Sri Lanka Run',
 208: 'Türkiye',
 215: 'United Kingdom',
 166: 'Qatar',
 162: 'Philippines',
 30: 'Brazil',
 148: 'New Zealand / New Zealand',
 94: 'Indonesia',
 37: 'Canada',
 14: 'Australia',
 216: 'United States',
 184: 'Singapore'}

def country_name(country_id):
    return countries[country_id]

#Creating the types of price of food
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

#Creating names of the colors:
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",}

def color_name(color_code):
    return COLORS[color_code]

def rename_columns(df):
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

#Cleaning DF:
def clear_df(df_raw):
    # Removing duplicates keeping the firt appearence:
    df_raw = df_raw.drop_duplicates(subset='Restaurant ID', keep='first')

    #Order DF by Restaurant ID:
    df_raw = df_raw.sort_values(by='Restaurant ID', ascending=True)
    
    #Show all the columns of the DataFrame:
    pd.set_option('display.max_columns', None)
    
    #Create a column named "Country Name" with the names of the countries by "Country Code":
    df_raw['Country Name'] = df_raw['Country Code'].apply(country_name)
    
    #Clean Cuisine column
    df_raw["Cuisines"] = df_raw["Cuisines"].apply(lambda x: x.split(",")[0] if isinstance(x, str) else "")
    return df_raw

#=========================================================================

# -------------- Starting the logical structure of the code --------------

#=========================================================================

# -----------------
# Importing dataset:
# -----------------

df_raw = pd.read_csv('dataset/zomato_original.csv')

# -------------------
# Preparing DataFrame
# -------------------

df = clear_df(df_raw)
  
#======================================================================

# --------------------------- Side bar --------------------------------

#======================================================================


image_path = 'image3.jfif'
image = Image.open ( image_path )
st.sidebar.image( image , width=120 )

st.sidebar.markdown('# No Hunger #')
st.sidebar.markdown('## Best Delivery ##')
st.sidebar.markdown('''---''')

st.sidebar.markdown('## Select a deadline ##')

countries_option = st.sidebar.multiselect(
    'Choose the Countries you want to view the Restaurants',
    ['India',
 'South Africa',
 'The United Arab Emirates',
 'Sri Lanka Run',
 'Türkiye',
 'United Kingdom',
 'Qatar',
 'Philippines',
 'Brazil',
 'New Zealand / New Zealand',
 'Indonesia',
 'Canada',
 'Australia',
 'United States',
 'Singapore'],
     default=['India',
 'South Africa',
 'The United Arab Emirates',
 'Sri Lanka Run',
 'Türkiye',
 'United Kingdom',
 'Qatar',
 'Philippines',
 'Brazil',
 'New Zealand / New Zealand',
 'Indonesia',
 'Canada',
 'Australia',
 'United States',
 'Singapore'])

#Country filter
df1=df[df['Country Name'].isin(countries_option)]
# df1=df1[df['City'].isin(df.loc['City'].[cities_select]

#Function quantity Restaurants view:
cities_select=st.sidebar.select_slider('Select the number of cities you want to view', options=list(range(1, 21)),value=(10))

st.sidebar.markdown('''---''')
st.sidebar.markdown('### Powered by Bruno Boneto ###')

#======================================================================

# --------------------- Layout in Streamlit ---------------------------

#======================================================================

st.markdown('# 🏙️Cities Vision')

with st.container():
    top_cities()
    
with st.container():
    col1,col2=st.columns(2)
    with col1:
        top_rating(4,bigger=True)

    with col2:
        top_rating(2.5,bigger=False)

with st.container():
    qtd_cuisine()
    
    
