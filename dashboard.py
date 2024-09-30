import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from ollama import ask_ollama

# Load the excel to a pandas dataframe variable
df = pd.read_excel('resources/ew24_structure_data.xlsx', dtype={'District': str})
 
# Load the shapefile 
shapefile_path = 'resources/VG2500_KRS.shp'  # Update with your path
germany_map = gpd.read_file(shapefile_path)

# Ensure both columns are of type string for merging
df['District'] = df['District'].astype(str)
germany_map['AGS'] = germany_map['AGS'].astype(str)  # Update 'AGS' with the actual column name

# Select only numeric columns from df for the merge
numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
df = df[['District','Name'] + numeric_columns]  # Keep only 'Name','District' and numeric columns

# Apply filter to remove records with district values having exactly 2 digits
df = df[~df['District'].str.match(r'^\d{2}$')]

# Merge the datasets on the district key
germany_map = germany_map.merge(df, left_on='AGS', right_on='District', how='left')

# Dropdown for selecting feature in UI
selected_feature = st.selectbox("Select a feature", numeric_columns)  # Only numeric columns

# Function to plot the map using Matplotlib
def plot_map(feature_column, germany_map):
    # Convert feature column to numeric, handling any errors
    germany_map[feature_column] = pd.to_numeric(germany_map[feature_column], errors='coerce')

    # Check if the feature has valid data
    if germany_map[feature_column].isnull().all():
        st.error("The selected feature contains no valid numeric values for visualization.")
        return

    # Plot the map using Matplotlib
    fig, ax = plt.subplots(figsize=(10, 15))
    germany_map.boundary.plot(ax=ax, color='black')  # Plot district boundaries
    germany_map.plot(column=feature_column, ax=ax, legend=True,
                     legend_kwds={'label': feature_column, 'orientation': "horizontal"},
                     cmap='OrRd', missing_kwds={"color": "lightgrey"})
    ax.set_title('Districts in Germany')
    ax.set_axis_off()

    # Display the plot in Streamlit
    st.pyplot(fig)

def get_district_name(district_id):
    # Filter the DataFrame for the row with the specified 'id'
    result = df[df['District'] == district_id]['Name']
    
    # Check if the result is not empty, then return the name, else return a message
    if not result.empty:
        return result.values[0]
    else:
        return "District not found"


def main_dashboard():
    flag_png = "resources/german_flag_icon.png"  
    col1, col2 = st.columns([1, 6])  # Two columns to display the flag png & Title in-line

    # Display flag in the first column
    with col1:
        st.image(flag_png, width=80)  # Adjust width as needed
    # Display title in the second column
    with col2:
        st.subheader("**GERMANY STRUCTURAL FEATURES DASHBOARD**")

    st.write("") #Empty line to create spacing between title and content

    # Create a placeholder for the selected feature text so that it stays pinned on top
    selected_feature_placeholder = st.empty()

    # Create two columns: one for map visualization, the other for Ollama analysis
    col1, col2 = st.columns(2)

    # Dropdown for selecting feature with a placeholder
    options = ['Select a feature'] + numeric_columns
    selected_feature = st.selectbox("Select a feature", options, disabled=False)

    # Handle placeholder selection
    if selected_feature == 'Select a feature':
        selected_feature_placeholder.subheader('Select a feature from the dropdown to visualize its distribution across districts.')
        #selected_feature_placeholder.markdown("<h5 style='text-align: center;'>Select a feature from the dropdown to visualize its distribution across districts.</h5>", unsafe_allow_html=True)

        return  # Exit if no feature is selected
    
    # Update the placeholder with the selected feature using Streamlit's default styling
    selected_feature_placeholder.subheader(f"**{selected_feature}**")

    # Calculate val_summary for the selected feature
    val_summary = df[selected_feature].describe()

    # Calculate the max, min, and district names based on the selected feature
    max_value = df[selected_feature].max()
    min_value = df[selected_feature].min()

    max_district_id = df[df[selected_feature] == max_value]['District'].values[0]
    min_district_id = df[df[selected_feature] == min_value]['District'].values[0]

    max_district_name = get_district_name(max_district_id)
    min_district_name = get_district_name(min_district_id)

    # Render the map if a valid feature is selected
    with col1:
        st.markdown('**_District Map Visualization_**')
        plot_map(selected_feature, germany_map)

    with col2:
        st.markdown('**_Data Analysis and Insights_**')
        with st.spinner('Ollama is analyzing the data... Please wait...'):
            summary = ask_ollama(selected_feature, max_value, min_value, max_district_name, min_district_name, val_summary)
            # Display the summary
            st.write(summary)
