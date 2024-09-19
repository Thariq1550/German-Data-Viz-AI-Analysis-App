import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

from ollama import ask_ollama

# Load dataset
df = pd.read_excel('ew24_structure_data.xlsx', dtype={'District': str})

# Load the shapefile
shapefile_path = 'resources/VG2500_KRS.shp'  # Update with your path
germany_map = gpd.read_file(shapefile_path)

# Ensure both columns are of type string for merging
df['District'] = df['District'].astype(str)
germany_map['AGS'] = germany_map['AGS'].astype(str)  # Update 'AGS' with the actual column name

# Select only numeric columns from df for the merge
numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
df = df[['District','Name'] + numeric_columns]  # Keep only 'District' and numeric columns

# Merge the datasets on the district key
germany_map = germany_map.merge(df, left_on='AGS', right_on='District', how='left')

# Dropdown for selecting feature
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
    
max_value=df[selected_feature].max()
min_value=df[selected_feature].min()

max_district_id = df[df[selected_feature] == max_value]['District'].values[0]
min_district_id = df[df[selected_feature] == min_value]['District'].values[0]

max_district_name = get_district_name(max_district_id)
min_district_name = get_district_name(min_district_id)
    
def send_val_to_ollama():
    return max_value, min_value, max_district_name,min_district_name,selected_feature

def main_map():
    # Initialize session state for ollama request tracking
    if 'request_status' not in st.session_state:
        st.session_state.request_status = None

     # Dropdown for selecting feature with a placeholder
    options = ['Select a feature'] + numeric_columns
    selected_feature = st.selectbox("Select a feature", options)
    
    # Handle placeholder selection
    if selected_feature == 'Select a feature':
        st.write('Please select a feature to visualize.')
    else:
        # Clear previous request status if a new feature is selected
        if st.session_state.request_status == 'pending':
            st.session_state.request_status = 'canceled'
            st.experimental_rerun()

        # Render the map if a valid feature is selected
        plot_map(selected_feature, germany_map)

        # Show spinner while waiting for Ollama's response
        st.session_state.request_status = 'pending'
        with st.spinner('Ollama is analyzing the data...'):
            summary = ask_ollama(selected_feature, max_value, min_value, max_district_name, min_district_name)
        
        # Update request status
        st.session_state.request_status = 'completed'
        
        # Display the summary
        st.subheader("Ollama's Summary of the Map:")
        st.write(summary)







