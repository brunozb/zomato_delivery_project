#---------------------------- Libraries ----------------------------------
import pandas as pd
import re
import plotly
import plotly.express as px
import folium
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


st.set_page_config( page_title='Cuisines',page_icon='📈', layout='wide' )

#=========================================================================

#---------------------------- Functions ----------------------------------

#=========================================================================

#Function to create bar graphics with the best or the worst restaurants (Aggregate rating) of the DataBase, by Cuisines:
def top_cuisines(clase_):
    df1_max_rat=(df1.loc[:,['Restaurant Name','Cuisines','Aggregate rating']]
                    .groupby('Cuisines')
                    .mean()
                    .sort_values(by='Aggregate rating',ascending=clase_)
                    .reset_index())
    df1_max_rat=df1_max_rat.iloc[:restaurants_select]
    fig=px.bar(df1_max_rat,x='Cuisines',y='Aggregate rating',text_auto=True)
    fig.update_layout(title={'text':f'Top {restaurants_select} Best Cuisines','x':0.5,'xanchor':'center'})
    st.plotly_chart(fig,use_container_width=True)

#Create a DataFrame with the best restaurants according to the slide selection of the side bar:
def top_restaurants(df1):
    df1_aux=(df1.loc[df1['Aggregate rating']==(df1['Aggregate rating']
                .max()),['Restaurant Name','Country Name','City','Cuisines','Average Cost for two','Aggregate rating','Votes']]
                .sort_values(by='Votes',ascending=False)
                .reset_index())
    df1_aux=df1_aux.iloc[:restaurants_select]
    df1_aux=df1_aux.set_index('Restaurant Name')
    df1_aux=df1_aux.drop('index',axis=1)
    result=st.write(df1_aux)
    return result

#Create cards with the best restaurants of selected cuisines
def best_cuisines_type(df):
    best_restaurants_by_cuisine=df[df['Cuisines'].isin(cuisines_select)]
    best_restaurants_by_cuisine=(best_restaurants_by_cuisine.loc[:,['Country Name', 'Restaurant Name', 'Aggregate rating', 'Votes', 'Cuisines','City','Currency','Average Cost for two']]
                                                            .groupby('Cuisines')
                                                            .apply(lambda x: x.nlargest(1, ['Aggregate rating', 'Votes']))
                                                            .sort_values(by='Aggregate rating', ascending=False)
                                                            .reset_index(drop=True))

    # Create five columns to display the cards side by side
    columns = st.columns(5)

    # Loop over each row of the DataFrame
    for idx, row in best_restaurants_by_cuisine.iterrows():
        # Create strings for the label, value and additional_info
        label = f"{row['Cuisines']}: {row['Restaurant Name']}"
        value = f"{row['Aggregate rating']}/5.0"
        additional_info = f"**Country:** {row['Country Name']}  \n**City:** {row['City']}  \n**Price for two people:** {row['Currency']}{row['Average Cost for two']}"
        
        # Display the card in the corresponding column
        with columns[idx % 5]:
            st.metric(label=label, value=value, help=additional_info)
            
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


image_path = 'image4.jfif'
image = Image.open ( image_path )
st.sidebar.image( image , width=120 )

st.sidebar.markdown('# No Hunger #')
st.sidebar.markdown('## Best Delivery ##')
st.sidebar.markdown('''---''')

st.sidebar.markdown('# Select the deadlines #')

#Function multiselect by Countries:
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

#Function quantity Restaurants view:
restaurants_select=st.sidebar.select_slider('Select the number of Restaurants you want to view', options=list(range(1, 21)),value=(10))
               
#Function Cuisines view:
cuisines_select=st.sidebar.multiselect('Select the Cuisines you want to view',['North Indian', 'South Indian', 'Mithai', 'Italian', 'Cafe',
       'Continental', 'Malaysian', 'European', 'Gujarati', 'Biryani',
       'Pizza', 'Burger', 'Healthy Food', 'Mughlai', 'Fast Food',
       'Street Food', 'Chinese', 'Finger Food', 'Bakery', 'American',
       'Asian', 'Thai', 'Japanese', 'Parsi', 'BBQ', 'Seafood', 'Arabian',
       'Tibetan', 'Chettinad', 'Mexican', 'African', 'Indian',
       'Contemporary', 'Greek', 'Steak', 'Portuguese', 'Turkish', 'Grill',
       'Ice Cream', 'French', 'Hyderabadi', 'Kebab', 'Kerala',
       'Rajasthani', 'Desserts', 'Mediterranean', 'Andhra', 'Goan',
       'Belgian', 'Lebanese', 'British', 'Brazilian', 'Juices',
       'Sandwich', 'Momos', 'Mongolian', 'Maharashtrian', 'Malwani',
       'Assamese', 'Rolls', 'Naga', 'North Eastern', 'Salad', 'Beverages',
       'Tea', 'Lucknowi', 'Afghan', 'Mangalorean', 'Charcoal Chicken',
       'Modern Indian', 'Pakistani', 'Mandi', 'Sushi', 'Tex-Mex',
       'Filipino', 'German', 'Sri Lankan', 'Middle Eastern', 'Vietnamese',
       'World Cuisine', 'Döner', 'Restaurant Cafe', 'Patisserie',
       'Old Turkish Bars', 'Izgara', 'Home-made', 'Coffee', 'Kokoreç',
       'Bar Food', 'Giblets', 'Kumpir', 'Fresh Fish', 'Ottoman',
       'Turkish Pizza', 'Spanish', 'Ramen', 'Latin American', 'Peruvian',
       'Taiwanese', 'Khaleeji', 'Korean', 'International', 'Singaporean',
       'South African', 'Caribbean', 'Cuban', 'Argentine',
       'Gourmet Fast Food', 'Vegetarian', 'Author', 'Balti', 'Nepalese',
       'Moroccan', 'Cafe Food', 'Kiwi', 'Creole', 'Pan Asian', 'Sunda',
       'Western', 'Scottish', 'Cantonese', 'Durban', 'Deli',
       'Fish and Chips', '', 'Bengali', 'Iranian', 'Irish', 'Drinks Only',
       'Australian', 'Coffee and Tea', 'Modern Australian', 'Korean BBQ',
       'Yum Cha', 'Hawaiian', 'Breakfast', 'Diner', 'Canadian',
       'Eastern European', 'Others', 'Southern', 'Tapas',
       'Pacific Northwest', 'Russian', 'Donuts', 'Pub Food', 'Cajun',
       'New American', 'New Mexican', 'Ukrainian', 'Burmese',
       'California', 'Dim Sum', 'Crepes', 'Taco', 'Fusion',
       'Southwestern', 'Polish', 'Awadhi', 'Dimsum', 'Asian Fusion',
       'Indonesian', 'Mineira', 'Egyptian', 'Armenian', 'Roast Chicken'],default=['Italian','Chinese','Mexican','Indian','Brazilian'])
                   
#Country filter
df1=df[df['Country Name'].isin(countries_option)]

st.sidebar.markdown('''---''')
st.sidebar.markdown('### Powered by Bruno Boneto ###')

#======================================================================

# --------------------- Layout in Streamlit ---------------------------

#======================================================================


with st.container():
    st.markdown('# 🍽️Cuisines Vision')
    st.markdown('## Best Restaurant of the main Cuisines')
    best_cuisines_type(df1)
    st.markdown('___')
    
with st.container():
    st.markdown(f'## Top {restaurants_select} Restaurants')
    top_restaurants(df1)
    st.markdown('___')
    
with st.container():
    col1,col2=st.columns(2)
    with col1:
        top_cuisines(False)
       
    with col2:
        top_cuisines(True)
        