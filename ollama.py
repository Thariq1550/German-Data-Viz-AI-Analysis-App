import json
import requests
import streamlit as st

# Ollama API configuration
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Ensure this URL is correct


# Function to analyze the map data using Ollama with improved error handling
def ask_ollama(selected_feature,max_value,min_value,max_district,min_district,val_summary):
    data = {
        "model": "llama3.1:latest",
        "prompt": f"The feature selected is {selected_feature}. The district with the maximum {selected_feature} is {max_district} with the value {max_value} , and the district with the minimum is {min_district} with the value {min_value}. The following is the summary statistics of the {selected_feature} , {val_summary}. Can you analyze these findings in the context of Germany's districts and give a short response in less than 5-10 lines?"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        # Send POST request to Ollama API
        response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(data))

        # Split the response into multiple JSON objects
        response_text = response.text.strip().split('\n')

        # Concatenate the "response" fields from each JSON object
        final_summary = ""
        for response_chunk in response_text:
            try:
                json_response = json.loads(response_chunk)
                final_summary += json_response.get('response', '')
            except json.JSONDecodeError:
                continue  # Handle any non-JSON parts

        # Return the concatenated summary
        return final_summary.strip()
    
    except requests.RequestException as e:
        # Handle connection errors or timeouts
        st.error(f"Request error: {str(e)}")
        return f"Request error: {str(e)}"