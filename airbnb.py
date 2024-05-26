# Importing Libraries
import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

#page configuration
st.set_page_config(page_title= "Airbnb Analysis || Sagar",
                   page_icon= "A",
                   layout= "wide",initial_sidebar_state= "expanded")

#option menu
with st.sidebar:
   selected = option_menu("Menu", ["Home","Overview","Explore"], 
                           icons=["house","graph-up-arrow","bar-chart-line"],
                           menu_icon= "menu-button-wide",
                           default_index=0
                          )
   
#mongo db connection:
client = pymongo.MongoClient("mongodb+srv://sagar72427:sagar72427@cluster0.pmsz4he.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_airbnb
coll1 = db.listingsAndReviews

#reading the dataframe:
df  =pd.read_csv("Airbnb_data.csv")


if selected == "Home":
    # Title Image
    st.image("C:/Users/sagar/Desktop/Projects/airbnb images/Airbnb_Logo_Bélo.svg.png")
    col1,col2 = st.columns(2,gap= 'medium')
    col1.markdown("## :blue[Domain] : Travel Industry, Property Management and Tourism")
    col1.markdown("## :blue[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
    col1.markdown("## :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
    col2.markdown("#   ")
    col2.markdown("#   ")
    col2.image("C:\\Users\\sagar\\Desktop\\Projects\\airbnb images\\airbnb.jpg",
               use_column_width= "always")
    

# OVERVIEW PAGE
if selected == "Overview":
    tab1,tab2 = st.tabs(["$\huge 📝 RAW DATA $", "$\huge🚀 INSIGHTS $"])
    
    # RAW DATA TAB
    with tab1:
        # RAW DATA
        col1,col2 = st.columns(2)
        if col1.button("Click to view Raw data"):
            col1.write(coll1.find_one())
        # DATAFRAME FORMAT
        if col2.button("Click to view Dataframe"):
            col1.write(coll1.find_one())
            col2.write(df)

    
        # INSIGHTS TAB
    with tab2:
        # GETTING USER INPUTS
        country = st.sidebar.multiselect('Select a Country',sorted(df.country.unique()),sorted(df.country.unique()))
        prop = st.sidebar.multiselect('Select Property_type',sorted(df.property_type.unique()),sorted(df.property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type',sorted(df.room_type.unique()),sorted(df.room_type.unique()))
        price = st.slider('Select Price',df.price.min(),df.price.max(),(df.price.min(),df.price.max()))
        
        # CONVERTING THE USER INPUT INTO QUERY
        query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'
    
        # CREATING COLUMNS
        col1,col2 = st.columns(2,gap='medium')
        
        with col1:
            
            # TOP 10 PROPERTY TYPES BAR CHART
            df1 = df.query(query).groupby(["property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
            fig = px.bar(df1,
                         title='Top 10 Property Types',
                         x='Listings',
                         y='property_type',
                         orientation='h',
                         color='property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True) 


            # TOP 10 HOSTS BAR CHART
            df2 = df.query(query).groupby(["host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
            fig = px.bar(df2,
                         title='Top 10 Hosts with Highest number of Listings',
                         x='Listings',
                         y='host_name',
                         orientation='h',
                         color='host_name',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig,use_container_width=True)

        with col2:
            
            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
            df1 = df.query(query).groupby(["room_type"]).size().reset_index(name="counts")
            fig = px.pie(df1,
                         title='Total Listings in each Room_types',
                         names='room_type',
                         values='counts',
                         color_discrete_sequence=px.colors.sequential.Rainbow
                        )
            fig.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig,use_container_width=True)

            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
            country_df = df.query(query).groupby(['country'],as_index=False)['name'].count().rename(columns={'name' : 'Total_Listings'})
            fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='country',
                                locationmode='country names',
                                color='Total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                               )
            st.plotly_chart(fig,use_container_width=True)





# EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")
    
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(df.country.unique()),sorted(df.country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df.property_type.unique()),sorted(df.property_type.unique()))
    room = st.sidebar.multiselect('Select room_type',sorted(df.room_type.unique()),sorted(df.room_type.unique()))
    price = st.slider('Select Price',df.price.min(),df.price.max(),(df.price.min(),df.price.max()))
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'
    
    # HEADING 1
    st.markdown("## Price Analysis")
    
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='medium')
    
    with col1:
        
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('room_type',as_index=False)['price'].mean().sort_values(by='price')
        fig = px.bar(data_frame=pr_df,
                     x='room_type',
                     y='price',
                     color='price',
                     title='Avg Price in each Room type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
        # HEADING 2
        st.markdown("## Availability Analysis")
        
        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df.query(query),
                     x='room_type',
                     y='availability_365',
                     color='room_type',
                     title='Availability by Room_type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    with col2:
        
        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('country',as_index=False)['price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='country',
                                       color= 'price', 
                                       hover_data=['price'],
                                       locationmode='country names',
                                       size='price',
                                       title= 'Avg Price in each Country',
                                       color_continuous_scale='agsunset'
                            )
        col2.plotly_chart(fig,use_container_width=True)
        
        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")
        
        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('country',as_index=False)['availability_365'].mean()
        country_df.availability_365 = country_df.availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='country',
                                       color= 'availability_365', 
                                       hover_data=['availability_365'],
                                       locationmode='country names',
                                       size='availability_365',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)