import requests

url = "http://digitalconstructionhub.ovh/api/tenant/devices"

headers = {
    "Content-Type": "application/json",
    "X-Authorization": "Bearer FclHfeTR9kReE6ZwPPYA"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    devices = response.json()
    for device in devices["data"]:
        print(f"Device Name: {device['name']}, Device ID: {device['id']['id']}")
else:
    print(f"Failed to get devices: {response.content}")