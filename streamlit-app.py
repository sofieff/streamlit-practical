import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


from plot import generate_scatter_plot
from model import train_life_expectancy_model


#write headline as header "Worldwide Analysis of Quality of Life and Economic Factors"
st.header("Worldwide Analysis of Quality of Life and Economic Factors")

#write subtitle "This app enables you to explore the relationships between poverty, 
#            life expectancy, and GDP across various countries and years. 
#            Use the panels to select options and interact with the data."
st.subheader("This app enables you to explore the relationships between poverty, "
             "life expectancy, and GDP across various countries and years. "
             "Use the panels to select options and interact with the data.")

#use the whole width of the page
st.write("")

#create 3 tabs called "Global Overview", "Country Deep Dive", "Data Explorer"
tab1, tab2, tab3 = st.tabs(["Global Overview", "Country Deep Dive", "Data Explorer"])


#use global_development_data.csv to be found here: https://raw.githubusercontent.com/JohannaViktor/streamlit_practical/refs/heads/main/global_development_data.csv
# which is a cleaned merge of those 3 datasets

#poverty_url = 'https://raw.githubusercontent.com/owid/poverty-data/main/datasets/pip_dataset.csv'
#life_exp_url = "https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Healthy%20Life%20Expectancy%20-%20IHME/Healthy%20Life%20Expectancy%20-%20IHME.csv"
#gdp_url = 'https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Maddison%20Project%20Database%202020%20(Bolt%20and%20van%20Zanden%20(2020))/Maddison%20Project%20Database%202020%20(Bolt%20and%20van%20Zanden%20(2020)).csv'

#show the dataset in the 3rd tab

@st.cache_data
def load_data():
    """Load data from the CSV file and cache it."""
    return pd.read_csv("./global_development_data.csv")

# Load the dataset with spinner
with st.spinner("Loading data..."):
    df = load_data()

# Dictionary with country coordinates for the map plot
# This is a sample set of countries from the dataset
country_coords = {
    "Afghanistan": [33.93911, 67.709953],
    "Albania": [41.153332, 20.168331],
    "Algeria": [28.033886, 1.659626],
    "Angola": [-11.202692, 17.873887],
    "Argentina": [-38.416097, -63.616672],
    "Australia": [-25.274398, 133.775136],
    "Austria": [47.516231, 14.550072],
    "Bangladesh": [23.684994, 90.356331],
    "Brazil": [-14.235004, -51.92528],
    "Canada": [56.130366, -106.346771],
    "China": [35.86166, 104.195397],
    "Colombia": [4.570868, -74.297333],
    "Congo": [-4.038333, 21.758664],
    "Croatia": [45.1, 15.2],
    "Cuba": [21.521757, -77.781167],
    "Cyprus": [35.126413, 33.429859],
    "Denmark": [56.26392, 9.501785],
    "Ecuador": [-1.831239, -78.183406],
    "Egypt": [26.820553, 30.802498],
    "Finland": [61.92411, 25.748151],
    "France": [46.227638, 2.213749],
    "Germany": [51.165691, 10.451526],
    "Greece": [39.074208, 21.824312],
    "India": [20.593684, 78.96288],
    "Indonesia": [-0.789275, 113.921327],
    "Iran": [32.427908, 53.688046],
    "Iraq": [33.223191, 43.679291],
    "Ireland": [53.41291, -8.24389],
    "Israel": [31.046051, 34.851612],
    "Italy": [41.87194, 12.56738],
    "Japan": [36.204824, 138.252924],
    "Kenya": [-0.023559, 37.906193],
    "Kuwait": [29.31166, 47.481766],
    "Mexico": [23.634501, -102.552784],
    "Netherlands": [52.132633, 5.291266],
    "New Zealand": [-40.900557, 174.885971],
    "Nigeria": [9.081999, 8.675277],
    "Pakistan": [30.375321, 69.345116],
    "Peru": [-9.189967, -75.015152],
    "Poland": [51.919438, 19.145136],
    "Portugal": [39.399872, -8.224454],
    "Russia": [61.52401, 105.318756],
    "Saudi Arabia": [23.885942, 45.079162],
    "Singapore": [1.352083, 103.819836],
    "South Africa": [-30.559482, 22.937506],
    "Spain": [40.463667, -3.74922],
    "Sudan": [12.862807, 30.217636],
    "Sweden": [60.128161, 18.643501],
    "Switzerland": [46.818188, 8.227512],
    "Syria": [34.802075, 38.99677],
    "Thailand": [15.870032, 100.992541],
    "Turkey": [38.963745, 35.243322],
    "Ukraine": [48.379433, 31.16558],
    "United Kingdom": [55.378051, -3.435973],
    "United States": [37.09024, -95.712891],
    "Vietnam": [14.058324, 108.277199],
}

# Convert the coordinates dictionary into a DataFrame
coords_df = pd.DataFrame([
    {"country": country, "lat": coords[0], "lon": coords[1]}
    for country, coords in country_coords.items()
])

# Merge the coordinates with the main DataFrame
df = pd.merge(df, coords_df, on="country", how="left")


with tab3:
    st.dataframe(df)

    
    #include a multiselectbox to select the country names
    selected_countries_tab3 = st.multiselect(
        "Select countries:",
        options=df["country"].unique()
    )

    #include a slider to select the year range
    year_range_tab3 = st.slider(
        "Select year range:",
        min_value=1990,
        max_value=2020,
        value=(1990, 2020),
        key="year_tab3"
    )

    #make the filtered dataset downloadable
    # Filter the dataset
    filtered_data_tab3 = df.copy()

    if selected_countries_tab3:
        filtered_data_tab3 = filtered_data_tab3[filtered_data_tab3["country"].isin(selected_countries_tab3)]

    filtered_data_tab3 = filtered_data_tab3[
        (filtered_data_tab3["year"] >= year_range_tab3[0]) &
        (filtered_data_tab3["year"] <= year_range_tab3[1])
    ]

    # Show the filtered dataframe
    st.dataframe(filtered_data_tab3)    

    # Make CSV from filtered data
    csv_data = filtered_data_tab3.to_csv(index=False)

    # Download button
    st.download_button(
        "Download filtered dataset",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv"
    )


#task 3: deployment: deploy the app on streamlit cloud (see readme: create own github repo with practical.py file and requirements.txt, connect the github to streamlit cloud)

#task 4 in tab 1
with tab1:

    #create a slider to select a certain year, filter the dataset accordingly
    year_range_tab1 = st.slider(
            "Select year range:",
            min_value=1990,
            max_value=2020,
            value=(1990, 2020),
            key="year_tab1"
        )
    
    filtered_data_tab1 = df.copy()

    filtered_data_tab1 = filtered_data_tab1[
        (filtered_data_tab1["year"] >= year_range_tab1[0]) &
        (filtered_data_tab1["year"] <= year_range_tab1[1])
    ]

    #create 4 key metrics in 4 columns each with a description: 
    #col1: mean of life expectancy; 
    #col2: median of GDP per capita; 
    #col3: mean of headcount_ratio_upper_mid_income_povline; 
    #col4: Number of countries
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Mean Life Expectancy", value=filtered_data_tab1["Life Expectancy (IHME)"].mean(), )
    col2.metric(label="Median GDP per Capita", value=filtered_data_tab1["GDP per capita"].median())
    col3.metric(label="Mean Poverty Rate", value=filtered_data_tab1["headcount_ratio_upper_mid_income_povline"].mean())
    col4.metric(label="Number of Countries", value=filtered_data_tab1["country"].nunique())


    #task 5 in tab 1: 
    #create a scatterplot of the dataframe filtered according to the slider: x=GDP per capita, y = Life Expectancy (IHME) with hover, log, size, color, title, labels
    #you might store the code in an extra plots.py file

    st.subheader("GDP per Capita vs Life Expectancy (IHME)")
    # Call the function from the plot.py file
    st.plotly_chart(generate_scatter_plot(filtered_data_tab1))

    #task 6 in tab 1: create a simple model (conda install scikit-learn -y; Randomforest Regressor): 
    #features only 3 columns: ['GDP per capita', 'headcount_ratio_upper_mid_income_povline', 'year']; target: 'Life Expectancy (IHME)'
    #you might store the code in an extra model.py file

    #make input fields for inference of the features (according to existing values in the dataset) and use the model to predict the life expectancy for the input values
    #additional: show the feature importance as a bar plot

    st.subheader("Predict Life Expectancy")
    # Train the model and get the feature importances
    model, feature_importances_df = train_life_expectancy_model(df)
    
    # Create input widgets for the features
    with st.container():
        st.markdown("Use the sliders below to predict the life expectancy for a hypothetical scenario.")
        
        col1_model, col2_model, col3_model = st.columns(3)
        with col1_model:
            gdp_value = st.slider(
                "GDP per capita (in thousands)",
                min_value=0.0,
                max_value=200.0,
                value=50.0,
                step=1.0,
                key="gdp_model"
            )
        with col2_model:
            poverty_rate = st.slider(
                "Poverty Rate (headcount ratio)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=1.0,
                key="poverty_model"
            )
        with col3_model:
            year_value = st.slider(
                "Year",
                min_value=1990,
                max_value=2020,
                value=2020,
                step=1,
                key="year_model"
            )
    
    # Create a DataFrame from the user's inputs
    data = pd.DataFrame([[gdp_value, poverty_rate, year_value]], 
                              columns=['GDP per capita', 'headcount_ratio_upper_mid_income_povline', 'year'])
    
    # Make a prediction
    prediction = model.predict(data)[0]
    
    # Display the prediction in a formatted metric
    st.metric(label="Predicted Life Expectancy", value=f"{prediction:.2f} years")

    st.markdown("---")
    st.subheader("Feature Importance")
    st.markdown("This bar chart shows which features the model considered most important for making its predictions.")
    
    # Use st.bar_chart to display the feature importances
    st.bar_chart(feature_importances_df, x='feature', y='importance')


    #task 7 in tab 1: 
    #create a map plot like the demo in hello streamlit with 3D bars. 
    #use chatgpt or similar to create lat and lon values for each country (e.g. capital as reference)
    st.subheader("Life Expectancy and GDP on a Global Map")
    st.markdown("This map shows the relationship between Life Expectancy and GDP per capita, represented by the height and color of the bars for a given year.")

    # Filter the data for a single year for the map plot
    map_year = st.slider(
        "Select a year for the map:",
        min_value=int(df["year"].min()),
        max_value=int(df["year"].max()),
        value=2015,
        step=1,
        key="map_year"
    )
    
    map_data = df.copy()
    map_data = map_data[map_data["year"] == map_year].dropna(subset=["lat", "lon"])
    
    fig = px.scatter_mapbox(
        map_data,
        lat="lat",
        lon="lon",
        hover_name="country",
        hover_data={"Life Expectancy (IHME)": ":.2f", "GDP per capita": ":,.0f"},
        color="GDP per capita",
        size="Life Expectancy (IHME)",
        color_continuous_scale=px.colors.sequential.Viridis,
        zoom=1,
        height=500,
        title=f"Global Overview for {map_year}"
    )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)
