import streamlit as st
import pandas as pd

#st.title("My First Streamlit App")
#st.write("Hello, Streamlit!")


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

with tab3:
    st.dataframe(df)

    
    #include a multiselectbox to select the country names
    selected_countries = st.multiselect(
        "Select countries:",
        options=df["country"].unique()
    )

    #include a slider to select the year range
    year_range = st.slider(
        "Select year range:",
        min_value=1990,
        max_value=2020,
        value=(1990, 2020)
    )

    #make the filtered dataset downloadable
    # Filter the dataset
    filtered_data = df.copy()

    if selected_countries:
        filtered_data = filtered_data[filtered_data["country"].isin(selected_countries)]

    filtered_data = filtered_data[
        (filtered_data["year"] >= year_range[0]) &
        (filtered_data["year"] <= year_range[1])
    ]

    # Show the filtered dataframe
    st.dataframe(filtered_data)    

    # Make CSV from filtered data
    csv_data = filtered_data.to_csv(index=False)

    # Download button
    st.download_button(
        "Download filtered dataset",
        data=csv_data,
        file_name="filtered_data.csv",
        mime="text/csv"
    )


#task 3: deployment: deploy the app on streamlit cloud (see readme: create own github repo with practical.py file and requirements.txt, connect the github to streamlit cloud)