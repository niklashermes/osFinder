import json

import requests


# Define the device name to search for
# device_name = "iphone 11"


def json_search(device_name, base_url):
    # Define the website to search on
    # website = "https://wiki.lineageos.org/search.json?q=" + device_name
    # website = "https://wiki.pixelexperience.org/search.json?q=" + device_name
    website = base_url + device_name
    # Send a GET request to the website
    response = requests.get(website)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the json data
        json_data = response.json()
        matched_devices = []
        # Iterate through the devices in the json data
        for device in json_data:
            # Check if the device name contains the search query
            if device_name.lower() in device["title"].lower():
                # Append the matched device to the list
                matched_devices.append(device)
        if matched_devices:
            # Print the title and url of all the matched devices
            for device in matched_devices:
                # print("Title: ", device["title"])
                print(f"{base_url[:-15]}" + device["url"])
        else:
            return "Device not found in json file on " + base_url.split(".")[1]


def main(device_name):
    # device_name = "mido"
    los_res = json_search(device_name, "https://wiki.lineageos.org/search.json?q=")
    pex_res = json_search(device_name, "https://wiki.pixelexperience.org/search.json?q=")
    return [los_res, pex_res]


if __name__ == "__main__":
    main()
