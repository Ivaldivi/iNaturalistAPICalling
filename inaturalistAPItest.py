import requests
import json

# Define the API endpoint for observations
url = "https://api.inaturalist.org/v1/observations"

# Parameters: you can filter by taxon_id, location, date, etc.
params = {
    "q": "sciurus",
    "per_page": 25  # Get only 10 results per query
}

# Send the GET request to the iNaturalist API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse JSON response
    observations = data['results']
    
    ## Extract desired fields from each observation
    filtered_data = []
    for observation in observations:
        if "photos" in observation and len(observation["photos"]) > 0: 
                observation_photo_url = observation["photos"][0]["url"] 
        if "quality_grade" in observation and observation["quality_grade"]=="research": 
            # Select specific fields: species name, date, and coordinates (lat, long)
            filtered_observation = {
                "species": observation['taxon']['name'],  # Species name
                "common name": observation["taxon"]['preferred_common_name'],
                "observation photo url": observation_photo_url,
                "date": observation['observed_on'],  # Date of observation
                "latitude": observation['location'].split(',')[0] if observation['location'] else None,  # Latitude
                "longitude": observation['location'].split(',')[1] if observation['location'] else None,  # Longitude
                "quality_grade": observation["quality_grade"]
            }
            filtered_data.append(filtered_observation)
    
    ## Pretty print the filtered data
    print(json.dumps(filtered_data, indent=2))
else:
    print("Error:", response.status_code)

