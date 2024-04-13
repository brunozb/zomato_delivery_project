import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🍽️"
)
   
image = Image.open ('image0.jfif')
st.sidebar.image ( image , width=120 )

st.sidebar.markdown('# Zomato Company #')
st.sidebar.markdown('## Best Restaurants in the World ##')
st.sidebar.markdown('''---''')

st.write( "# Zomato Company Growth Dashboard" )

st.markdown(
    """
    Growth Dashboard was built to follow Restaurants growth metrics, by Countries, Cities and different Cuisines
    ### How can I use this Growth Dashboard?
    - Main Vision:
        - General and geographic vision of the restaurants 
    - Country Vision:
        - Numbers of registered cities and restaurants and average prices and reviews by countries  
    - Cities Vision:
        -  Number of best rated restaurants with more types of cuisine by city 
    - Cuisines Vision:
        - best restaurants for different types of cuisine 
    ### Ask for Help
    - @bruno.boneto - brunozb10@gmail.com
    """ )