#%%
import streamlit as st
import ee
import json
import pandas as pd
import geopandas as gpd
from shapely import wkt
import geemap.foliumap as geemap
import leafmap.foliumap as leafmap
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import os
import leafmap.kepler
#------------------------------------------------------------------
#Maps
Geemap_Map = geemap.Map(basemaps='CartoDB.DarkMatter')
Kepler_Map= leafmap.kepler.Map()
#------------------------------------------------------------------
# Loading Data
Pirforos = Image.open("Data\Picture1.png")
Mean_Income_2011 = gpd.read_file("Data\Mean_Income_us_tracts_2011.geojson")
Mean_Income_2019 = gpd.read_file("Data\Mean_Income_us_tracts_2019.geojson")
Land_Use_Percentage = pd.read_csv("Data\Cross Classification.csv")
Urban_Green_2011 = gpd.read_file("Data\FIXUrban_Green_2011.geojson")
Urban_Green_2019 = gpd.read_file("Data\FIXUrban_Green_2019.geojson")
Historic_Districts_2011 = gpd.read_file("Data\Historic Districts_2011.geojson")
Historic_Districts_2019 = gpd.read_file("Data\Historic Districts_2019.geojson")
Historic_Districts_2011 = gpd.GeoDataFrame(Historic_Districts_2011)
Historic_Districts_2019 = gpd.GeoDataFrame(Historic_Districts_2019)



#------------------------------------------------------------------
os.environ['LOCALTILESERVER_CLIENT_PREFIX'] = 'proxy/{port}'

#-------------------------------------------------------------------
# Function for NAIP Imagery
@st.cache
def image_for_classification(start_date,finish_date):
# - Polar Coordinates
    start = ee.Date(start_date)
    finish = ee.Date(finish_date)

    # A feature collection of point geometries for mountain peaks.

    filterBounds = ee.Geometry.BBox(-74.2559,40.4961,-73.7000,40.9155)

    #print('Images intersecting feature collection', filteredCollection.filterBounds(fc));

    filteredCollection = ee.ImageCollection('USDA/NAIP/DOQQ')\
      .filterBounds(filterBounds)\
      .filterDate(start, finish)\
      .sort('CLOUD_COVER', True)

    
    image = filteredCollection
    return image

def geemap_appearrance():
    vis = {
        'bands': ['R','G','B'],
        'min': 0,
        'max': 255,
        'gamma':1
    }
    
    start_date_1 = '2019-08-09'
    finish_date_1 = '2020-09-07'
    start_date_2 = '2011-01-01'
    finish_date_2 = '2013-12-31'

    Geemap_Map.addLayer(image_for_classification(start_date = start_date_1,finish_date = finish_date_1),vis,f'ROI {start_date_1}-{finish_date_1}')
    Geemap_Map.addLayer(image_for_classification(start_date = start_date_2,finish_date = finish_date_2),vis,f'ROI {start_date_2}-{finish_date_2}')
    Geemap_Map.zoom_to_bounds(bounds=[-74.2559,40.4961,-73.7000,40.9155])
    Geemap_Map.to_streamlit()
    st.write(f"1st: Image -> Start date: {start_date_1} and Finsh Date: {finish_date_1}")
    st.write(f"2nd: Image -> Start date: {start_date_2} and Finsh Date: {finish_date_2}")
    return


#------------------------------------------------------------------
# Main Function

def main():
    # Create a sidebar with a selection widget
    st.set_page_config(layout="wide")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Dive into :", ["Introduction","NAIP Imagery Dataset","Page1: Luxury Effect vs Urban Green Spaces", "Page2: Land Use Effect vs Urban Green Spaces","Page 3: Legacy Effect vs Urban Green Spaces"])

    # Use an if statement to display different content on different pages:

    if page == "Introduction":
        backgroundColor="#FFFFFH"
        col1,col2 = st.columns([1,9])
        with col2:
            st.title("National Tecnhical University of Athens\t - School of Rural, Surveying and Geoinformatics Engineer")
        
        with col1:
            st.image(Pirforos,width=90, use_column_width=200)
        st.header("Title: How Urban Green Spaces can be affected by Socioeconomic Factors and Land Uses ")
        st.markdown("### Subject : Remote Sensing Application")
        

        st.markdown("""##### **:green[A brief introduction about my Project]** \n
        The aim of this project is to detect how Green Urban Spaces can be affected by Land use and Socioeconomic Factors.
        The project is made of three Pages. The 1st examines how Luxury Effect can affect Urban Green Spaces (UGS) and the 2nd and 3rd Pages examine how Land Use Effect and Legacy Effect can be affect UGS, respectivly.  
        The Socioeconomic Factors which will be examined are : \n
        - Mean Income (Luxury Effect) \n 
        - Historic Districts (Legacy Effect) \n
        and also - Land Use (Lan Use Effect).
        
        More Info about data sources:\n
        For Mean Income: United States Census Bureau -> https://data.census.gov/map?t=Income+(Households,+Families,+Individuals)&g=0500000US36005,36061&tid=ACSST1Y2021.S1901&cid=S1901_C01_001E&layer=VT_2021_050_00_PY_D1&palette=Reds&breaks=Quantile(1)&mode=thematic&loc=40.7512,-73.9558,z12.6789 \n
        For Historic Districts: NYC Open Data -> https://data.cityofnewyork.us/Housing-Development/Historic-Districts/xbvj-gfnw \n
        For Land Use: A classification has been made using Google Earth Engine and the ImaageCollection: NAIP Imagery
        """)

        st.markdown("""###### My name: Demetriades Pavlos \n ###### Semester: 9th \n ###### Year: 2022 - 2023 """)
    


    elif page=="NAIP Imagery Dataset":
        st.header("NAIP Imagery Dataset")
        
        st.warning("Be carefull about the NAIP Imagery Dataset.\n The things that you have to pay attention, are the resolution of this Dataset.\
            The radiometric and spatial resolution are not perfect for the Change Detection. This is due to the 2011 dataset, which has not been preprocessed.\
            Also both of th 'Images' are not true orthorectified. That means that deflection due to relief appears.")
        st.success("But for the purposes of this project, the 2011 dataset has been theorized to be suitable for change detection.")
        geemap_appearrance()
    # Page 1 follows --------------------------------------------------------------------------------------

    elif page == "Page1: Luxury Effect vs Urban Green Spaces":
        st.header("1. Luxury Effect vs Urban Green Spaces")
        st.markdown("The variable which represents the Luxury Effect, is Mean Income.\
        In this Page will be examined how UGS can be affected by Mean Income.")

        st.subheader("1.1 A plot with Mean Income and Green [%]")
        col_mean_1,col_mean_2 = st.columns(2)
        with col_mean_1:
            fig_mean_1 = px.scatter(data_frame = Mean_Income_2011,  x = "Mean Income 2011 ($)", y = "Green [%]", hover_name="GEOID",title="Plot of Mean Income and Green [%] 2011 ")
            st.plotly_chart(fig_mean_1)
        with col_mean_2:
            fig_mean_2 = px.scatter(data_frame = Mean_Income_2019,  x = "Mean Income 2019 ($)", y = "Green [%]", hover_name="GEOID", title="Plot of Mean Income and Green [%] 2019")
            st.plotly_chart(fig_mean_2)
        Expander_1_1 = st.expander(label="My observatios and Yours ? (write them in the box bellow)")
        with Expander_1_1:
            Text_1_1 = st.text_area(label="My observations ... yours ? :", 
            value=""" 
            As it seems, there is a positive correlation between Mean Income and Urban Green Spaces (Green[%]).\
            Although, this positive correlation occurs, something weird is happening with the highest values of Mean Income\
            The highest values of Mean Income correspond with the lowest values of the Green [%]. Respectively this is happening with the\
            highest values of the Green [%] and the lowest values of the Mean Income.\
            This shows up the necessity of map creation, to see what really is happening.\n
            What's your observations? :
            """,height=200)

        st.write(Text_1_1)
        config = {
        'version': 'v1',
        'config': {
        'mapState': {
            'latitude': 40.71427,
            'longitude': -74.00597,
            'zoom': 9
            }}
        }
        with open(file="Kepler_Map_Configuration.json") as Kepler_Datas_Configuration:
            Kepler_Datas_Configuration=json.load(Kepler_Datas_Configuration)

        #Adding Datasets to Kepler Maps
        st.subheader("1.2 The map with Mean Income tracts and 'Green tracts' ")
        Kepler_Map.add_gdf(gdf=gpd.GeoDataFrame(Mean_Income_2011),layer_name="Mean Income 2011",config=Kepler_Datas_Configuration)
        Kepler_Map.add_gdf(gdf=gpd.GeoDataFrame(Mean_Income_2019),layer_name="Mean Income 2019",config =Kepler_Datas_Configuration )
        Kepler_Map.add_gdf(gdf=gpd.GeoDataFrame(Urban_Green_2011),layer_name="Urban_Grenn_Use_2011",config=Kepler_Datas_Configuration)
        Kepler_Map.add_gdf(gdf=gpd.GeoDataFrame(Urban_Green_2019),layer_name="Urban_Grenn_Use_2019",config=Kepler_Datas_Configuration)
        
        # Show me the Kepler Mp
        
        Kepler_Map.to_streamlit()
        st.write("What are the final conclusions ? ")
        st.markdown("Coclusions:")
        st.markdown("* :blue[1st: There is a positive correlation between UGS and Mean Income.]")
        st.markdown("* :blue[2nd: There is a 'mandatory' need for more realistic indices than the plot (Mean Income and UGS) for more realisic results.]")
        st.markdown("* :blue[3rd: This examples shows up the neccesity of a map creation.]")
        st.markdown("* :blue[4th: This example reveals the complexity of the spatial characteristics, the real world.]")

    # Page 2 follows --------------------------------------------------------------------------------------
    
    elif page == "Page2: Land Use Effect vs Urban Green Spaces":
        st.header("2. Land Use Effect vs Urban Green Spaces")
        st.markdown("The variable which represents the Land Uses Effect is Land uses.\
        In this Page will be examined how UGS can be affected by Land Uses")

        st.subheader("2.1 Change detection between 2011 & 2019")
        st.warning("For the change detection, a classification has been made for the two images of the NAIP Imagery program. One for 2019 and one for 2011.\
                     So, the results which will follow refers to these classifications. Unfortunately the two classification images can't show up in this app,\
                     due to the weakness of the browser to afford so huge files like Geotiffs. Hence, some examples of the change detection image\
                     are showed up for demonstration.")
        
        tab_2_1,tab_2_2,tab_2_3 = st.tabs(["From Trees to Buildings","From Buildings to Trees","From Buildings to Grass"])
        with tab_2_1:
            Trees_to_Buildings = Image.open("Data\Trees_to_Buildings.JPG")
            st.markdown(":green[Yellow circles show the correct change detections] and :red[Red Circles the false change detections]")
            st.image(Trees_to_Buildings)
            st.markdown("Observations: The main change detection in this picture, is the appearance of the big building in 2019")
        
        with tab_2_2:
            Buildings_to_Trees = Image.open("Data\Buildings_to_trees.JPG")
            st.image(Buildings_to_Trees)
            st.markdown("Observations: In this case, the most change detections which appear with blue, are false. This may is due to the Image 2011 which has not been preprocessed\
                        In respect to this, this case shows the necessity of the preprocess method to be made for an image especially for an image that will be used for a change detection. Also, another\
                        thing that pops up, is the necessity of the two images to have same resolutions.")

        with tab_2_3:
            Buildings_to_Grass = Image.open("Data\Buildings_to_Grass.JPG")
            st.image(Buildings_to_Grass)
            st.markdown("Observations: In this case this chnage detection shows the change between Buildings and Grass.")
        
        st.subheader("2.2 Quantification of Land Uses of the two epochs")
        st.markdown(":red[For the classification a Support Vector Machine (SVM) classifier has been used, using Google Earth Engine.]")
        st.dataframe(data=Land_Use_Percentage)
        #st.text("\n What's do you observe ?")
        Expander_2_1 = st.expander("My Observation and yours ? (Write them in the box bellow)")
        with Expander_2_1:
            Text_2_2_1 = st.text_area(label="My observations ... yours ? : ",\
            value=" The percentage of the change that UGS had, it was approximately +4%. The positive symbol means the positive percentage change in the overall percentage of all tracts\
                The biggest change is located on the Artifacts, with a percentage of 7.4%. This may be due to the large percentage change in the shadow category (~7.3% Epoch 2019). ")
        st.write(Text_2_2_1)
        dimensions = ['Green [%]',"Artifacts [%]"]
        st.markdown("##### 2.2.1 Plots: Artifacts vs Urban Green Spaces and Make your own Charts (Make your charts)")
        fig_1 = px.scatter(data_frame = pd.DataFrame(Urban_Green_2011),  x = "Artifacts [%]", y = "Green [%]",hover_name=Urban_Green_2011.index, title = "Artifacts vs Urban Green 2011")
        fig_2 = px.scatter(data_frame = pd.DataFrame(Urban_Green_2019),  x = "Artifacts [%]", y = "Green [%]",hover_name=Urban_Green_2019.index, title = "Artifacts vs Urban Green 2019")
        df_fig_1_1 = pd.DataFrame(Urban_Green_2011)
        df_fig_1_2 = pd.DataFrame(Urban_Green_2019)
             
        tab_1_1,tab_1_2 = st.tabs(tabs=["Artifacts vs UGS", "Make your own charts"])

        with tab_1_1:
            col_1,col_2 = st.columns(2)

            with col_1:
                #st.text("Epoch 2011")
                st.plotly_chart(fig_1, theme = "streamlit",use_container_width=True)
            
            with col_2:
                #st.text("Epoxh 2019")
                st.plotly_chart(fig_2, theme = "streamlit",use_container_width=True)
        st.write("Observations about the above plots. There is an obvious negative correlation between Artifacts and UGS.")
        with tab_1_2:
            
            #fig_2 = px.scatter(data_frame = pd.DataFrame(Urban_Green_2019),  x = "Artifacts [%]", y = "Green [%]",hover_name=Urban_Green_2019.index, title = "Artifacts vs Urban Green 2019")
            col_1,col_2 = st.columns(2)


            with col_1:
                #st.text("Epoch 2011")
                Select_box_x = st.selectbox(label = "Choose x column ",options=list(Urban_Green_2011.columns),index=13)
                Select_box_y = st.selectbox(label = "Choose y column ",options=list(Urban_Green_2011.columns),index=15)
                fig_1 = px.scatter(data_frame = df_fig_1_1,  x = Select_box_x, y = Select_box_y, hover_name=Urban_Green_2011.index, title = f"{Select_box_x} vs {Select_box_y} 2011")
                st.plotly_chart(fig_1, theme = "streamlit",use_container_width=True)
            
            with col_2:
                #st.text("Epoxh 2019")
                Select_box_x = st.selectbox(label = "Choose x column ",options=list(Urban_Green_2019.columns),index=12)
                Select_box_y = st.selectbox(label = "Choose y column ",options=list(Urban_Green_2019.columns),index=16)
                fig_2 = px.scatter(data_frame = df_fig_1_2,  x = Select_box_x, y = Select_box_y, hover_name=Urban_Green_2019.index, title = f"{Select_box_x} vs {Select_box_y} 2019")
                st.plotly_chart(fig_2, theme = "streamlit",use_container_width=True)
        
        st.markdown("##### 2.2.2 Quatification of **change detection of land uses** for the epochs 2019 & 2011")
        st.dataframe(data=pd.DataFrame(pd.read_csv('Data\Cross_Classification_Change_Detection.csv')),height=500)
        st.text("CrossClassCode column's number are corresponding to the numbers of the Change Detection Image.\nBut as it mentioned before the change detection image cannot shows up in this application")
        st.write("What are the final Coclusions?")
        st.markdown("**Coclusions:**")
        st.markdown("* :blue[1st: For a change detection, it is mandatory, the two image will have the same resolutions and be preprocessed]")
        st.markdown("* :blue[2nd: UGS are depended in a huge grade from Land Uses, specifically there is a negative dependance with the Artifacts (Buildings and Roads)\
                    and there is a positive dependance with bare land.]")


    # Page 3 follows --------------------------------------------------------------------------------------

    elif page == "Page 3: Legacy Effect vs Urban Green Spaces":
        st.header("3. Legacy Effect vs Urban Green Spaces")
        st.markdown("The variable which represents the Legacy Effect is Historic Districts.\
        In this Page will be examined how UGS can be affected by Historic Districts")
        st.subheader("3.1 Map of Historic Districts with Percentage of the Urban Green Spaces")
        style = {
            "stroke": False,
            "color": "#ff0000",
            "weight": 1,
            "opacity": 1,
            "fill": True,
            "fillColor": "#ffffff",
            "fillOpacity": 1.0,
            "dashArray": "9",
            "clickable": True
        }
        Hover_List = ["Green [%]","Grass [%]","ID","Vegetation [%]","category","desdate","area_name"]
        Geemap_Map.add_data(data=gpd.GeoDataFrame(Historic_Districts_2011),column = "Green [%]",cmap="Greens",k=7, layer_name=" Historic Districts 2011")
        Geemap_Map.add_data(data=gpd.GeoDataFrame(Historic_Districts_2019),column = "Green [%]",cmap="Greens",k=7, layer_name=" Historic Districts 2019")
        Geemap_Map.add_basemap(basemap="CartoDB.DarkMatter")
        #Map.set_center(lat=40.71427,lon=-74.00597)
        Geemap_Map.to_streamlit()
        
        
        Expander_3_1 = st.expander(label="My Observations and Yours (Write them down, inside the box) ?")
        with Expander_3_1:
                Text_3_1 = st.text_area(label="Observations",
                value= """ My obsevartions: Someone can notice that most Historic Districts have more than 20% of the UGS.\
                This is a great index which shows that someone can find a wide area of UGS in such places. Another thing that pops up, is the\
                positive spatial relation between UGS and Historic Districts.\
                Yours? :""", height=200)
        st.write(Text_3_1)

        # Creation of the plot with Historic Districts and the Percentage of the Urban Green Spaces in them
        st.subheader("3.2 A plot with Green Percentages of the two Epochs into Historic Districts ")
        st.markdown("x axis: IDs")
        st.markdown("y axis: Perentage of Green [%]")
        fig_3_1 = go.Figure()
        fig_3_1.add_trace(go.Scatter(
            x=Historic_Districts_2011["ID"],
            y=Historic_Districts_2011["Green [%]"],
            mode='markers',
            marker=dict(
                size=5,
                color='mediumpurple',
                #symbol='triangle-up'
            ),
            name=' 2011 Green Distribution'            
        ))

        fig_3_1.add_trace(go.Scatter(
            x=Historic_Districts_2019["ID"],
            y=Historic_Districts_2019["Green [%]"],
            mode='markers',
            marker=dict(
                size=5,
                color='mediumblue'
                #symbol='triangle-up'
            ),
            name=' 2019 Green Distribution'
        ))
        #fig_3_1.add_bar(xaxis="grgr")
        st.plotly_chart(fig_3_1,use_container_width=True)

        Expander_3_2 = st.expander(label="My Observations and yours? (Write them in the box bellow)")
        with Expander_3_2:
            Text_3_2 = st.text_area(label="Observations",
            value= """ This chart is plotting the Percentage of the Urban Green Spaces and the Historic Districts.\
            On the X axis, are the IDs and on the Y axis the percentage, in the two epochs respectively.\
            When the two dots (blue and purple) intersect each other, it means that the percentage of the UGS on a specific Historic District, didn't change.\
            Therefore, if the blue dot is higher than purple dot, that means the UGS in a Historic Districts saw a rise on the urban green.\
            What's your observations? (Write them down):""", height=200)
        
        st.write(Text_3_2)
        st.write("What are the final Conclusions?")
        st.markdown("**Conclusions**")
        st.markdown("* :blue[1st: There is a positive strength correlation of the UGS and Historic Districts]")
        st.markdown("* :blue[2nd: Over the years UGS are getting bigger into Historic Districts]")

    return

# code that should only be executed when this module is run directly

if __name__ == '__main__':
    main()
    
# %%
