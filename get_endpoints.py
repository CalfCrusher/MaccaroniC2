import requests

# Specify your ngrok API key
api_key = ""

# Set the API endpoint URL
api_url = "https://api.ngrok.com/endpoints"

# Set the headers with API key and Ngrok version
headers = {
    "Authorization": f"Bearer {api_key}",
    "Ngrok-Version": "2"
}

# Send the GET request
response = requests.get(api_url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    endpoints = data["endpoints"]
    
    # Print information about each endpoint
    for endpoint in endpoints:
        endpoint_id = endpoint["id"]
        created_at = endpoint["created_at"]
        updated_at = endpoint["updated_at"]
        public_url = endpoint["public_url"]
        proto = endpoint["proto"]
        hostport = endpoint["hostport"]
        endpoint_type = endpoint["type"]
        tunnel_id = endpoint["tunnel"]["id"]
        tunnel_uri = endpoint["tunnel"]["uri"]
        
        print(f"Endpoint ID: {endpoint_id}")
        print(f"Created At: {created_at}")
        print(f"Updated At: {updated_at}")
        print(f"Public URL: {public_url}")
        print(f"Protocol: {proto}")
        print(f"Hostport: {hostport}")
        print(f"Type: {endpoint_type}")
        print(f"Tunnel ID: {tunnel_id}")
        print(f"Tunnel URI: {tunnel_uri}")
        print()
else:
    print(f"Error: {response.status_code} - {response.text}")
