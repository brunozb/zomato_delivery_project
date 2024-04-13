#---------------------------- Libraries ----------------------------------
import pandas as pd
import plotly
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config( page_title='Main Page',page_icon='📈', layout='wide' )

#=========================================================================

#---------------------------- Functions ----------------------------------

#=========================================================================

#Create the button to download DataBase
def button_download():
    download = df.to_excel('zomato.xlsx')
    return download

#Create the map with the points of the restaurants of the DataBase with theirs cards:
def restaurants_map(df1):
  cols = ['Restaurant Name','Average Cost for two','Cuisines','Aggregate rating','City','Latitude', 'Longitude', 'Rating color']
  map = folium.Map()
  marker_cluster = MarkerCluster().add_to(map)
  for index,line in df1.iterrows():

    name = line["Restaurant Name"]
    price_for_two = line["Average Cost for two"]
    cuisine = line["Cuisines"]
    currency = line["Currency"]
    rating = line["Aggregate rating"]
    color = f'{line["Rating color"]}'

    html = "<p><strong>{}</strong></p>"
    html += "<p>Price: {},00 ({}) para dois"
    html += "<br />Type: {}"
    html += "<br />Aggragate Rating: {}/5.0"
    html = html.format(name, price_for_two, currency, cuisine, rating)

    popup = folium.Popup(
              folium.Html(html, script=True),
              max_width=500,
    )

    folium.Marker([line['Latitude'],
                  line['Longitude']],
                  popup=popup,
                  icon=folium.Icon(color=line['Rating color'],
                  icon='home')).add_to(marker_cluster)

  folium_static(map, width=1024, height=600)

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
    
    #Create a column named "Country Name" with the names of the countries by "Country Code" (there´s not in the original database):
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


image_path = 'image1.jfif'
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

st.header('$Zomato$', divider='rainbow')
st.header('No :rainbow[Hunger]!')
st.write('### The best spot to find your newer favorite :red[Restaurant]!') 

with st.container():
        
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.metric('Registered Restaurants',len(df['Restaurant ID'].unique()))
    with col2:
        st.metric('Registered Countries',len(df['Country Code'].unique()))
    with col3:
        st.metric('Registered Cities',len(df['City'].unique()))            
    with col4:
        st.metric('Reviews Made on the Platform',df['Votes'].sum())            
    with col5:
        st.metric('Types of Cuisines offered',len(df['Cuisines'].unique()))

    with st.container():

        st.markdown('##### Distance distribution by cities')
        restaurants_map(df1)






                
