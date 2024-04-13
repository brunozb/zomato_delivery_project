#---------------------------- Libraries ----------------------------------
import pandas as pd
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

#Create graphic - bars with Country Name:
    
def graphic_avg(col2,title_):
    df1_aux=round(df1.loc[:,['Country Name',col2]].groupby('Country Name').mean().sort_values(by=col2,ascending=False).reset_index(),2)
    fig=px.bar(df1_aux,x='Country Name',y=col2,text_auto=True,title=title_)
    fig.update_layout(title={'text': title_,'x': 0.5,'xanchor': 'center'})
    st.plotly_chart(fig)
    return fig

def graphic_country(col2,title_):
    df1_aux=df1.loc[:,['Country Name',col2]].groupby('Country Name').count().sort_values(by=col2,ascending=False).reset_index()
    fig=px.bar(df1_aux,x='Country Name',y=col2,title=title_)
    fig.update_layout(title={'text': title_,'x': 0.5,'xanchor': 'center'})
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

image_path = 'image2.jfif'
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
 'Türkiye',
 'United Kingdom',
 'Brazil',
 'Indonesia',
 'Canada',
 'United States'])

st.sidebar.markdown('## Press to download DataBase ##')

if st.sidebar.button('Download',key='Download',use_container_width=False):
    button_download()
    st.write('Download completed!')

#Country filter
df1=df[df['Country Name'].isin(countries_option)]

st.sidebar.markdown('''---''')
st.sidebar.markdown('### Powered by Bruno Boneto ###')

#======================================================================

# --------------------- Layout in Streamlit ---------------------------

#======================================================================

st.markdown('# 🌎Countries Vision')
with st.container():
    graphic_country('Restaurant ID','Restaurants per Country')
    
with st.container():
    graphic_country('City','Cities per Country')
    
with st.container():
    col1,col2=st.columns(2)
    with col1:
        graphic_avg('Aggregate rating','Average Rating per Country')
    with col2:
        graphic_avg('Average Cost for two','Avg. price for two per country')
       
