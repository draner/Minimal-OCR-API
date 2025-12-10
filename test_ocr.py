import base64
import json
import time

import requests

# Path to the image
image_path = "0118101435.png"

# Read and encode image to Base64
with open(image_path, "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

# Prepare request
url = "http://localhost:8000/ocr"
payload = {"image_data": image_base64}

# Send request
try:
    start_time = time.time()
    response = requests.post(url, json=payload)
    response.raise_for_status()

    # Display results
    result = response.json()
    end_time = time.time()
    print(f"✅ OCR completed in {end_time - start_time:.2f} seconds")
    print(json.dumps(result, indent=2, ensure_ascii=False))

except requests.exceptions.ConnectionError:
    print(
        "❌ Error: Cannot connect to API. Make sure it's running on http://localhost:8000"
    )
except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP Error: {e.response.status_code}")
    print(f"Response: {e.response.text}")
except Exception as e:
    print(f"❌ Error: {e}")
