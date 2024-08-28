import requests
import sys
import os

url = "http://localhost:7071/api/apply_filter"
files = {'image': open(r"./test_cat.jpg", 'rb')}
data = {'filter': 'sepia'}

response = requests.post(url, files=files, data=data)
print(f"Response status code: {response.status_code}")

# Only write to file if status code is successful (200-299)
if 200 <= response.status_code < 300:
    output_file = "./filtered_cat.jpg"
    with open(output_file, 'wb') as file:
        file.write(response.content)
    print(f"Image saved successfully as '{output_file}'")
else:
    print(f"Error: Received status code {response.status_code}. Image not saved.")

