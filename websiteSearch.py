import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


def web_markdown_search(device_name):
    # Define the website to search on
    website = "https://raw.githubusercontent.com/ProjectElixir-Devices/official_devices/A13/README.md"

    # Make a GET request to the URL
    response = requests.get(website)

    # Get the text of the markdown file
    markdown_text = response.text

    # Use regular expressions to search for the model name
    matches = re.finditer(device_name, markdown_text, re.IGNORECASE)

    lines_found = set()

    if matches:
        for match in matches:
            lines = markdown_text.split("\n")
            for line in lines:
                if match.group() in line:
                    if line not in lines_found:
                        lines_found.add(line)
                        # print(line)
                        line_match = re.search(r"\(([^)]+)\)", line)
                        if line_match:
                            print("https://projectelixiros.com/device/" + line_match.group(1))
    else:
        return "Device not found in projectelixiros markdown file."
    if not lines_found:
        return "Device not found in projectelixiros markdown file."


def web_search_eos(device_name):
    # specify the website URL
    url = "https://doc.e.foundation/devices"

    # retrieve the HTML of the website
    response = requests.get(url)
    # html = response.text

    # parse the HTML using BeautifulSoup
    # soup = BeautifulSoup(html, 'html.parser')

    # locate the table containing the device names
    # table = soup.find('table')

    # load the website's HTML into a DataFrame
    df = pd.read_html(url)[0]

    # create a new column "Brand_Name" with the combination of Brand and Name
    df["Brand_Name"] = df["Brand"] + ' ' + df["Name"]

    # filter the DataFrame to show only rows containing the device name in the Brand_Name column
    df_filtered = df[df["Brand_Name"].str.contains(device_name, case=False)]

    if "Empty DataFrame" not in df_filtered.to_string():
        for line in df_filtered["Name"]:
            match = re.search(r'"([^"]+)"', line)
            if match:
                code_name = match.group(1)
            print("https://doc.e.foundation/devices/" + code_name)

            search_cos = requests.get(f"https://calyxos.org/install/devices/{code_name}/")
            if search_cos.status_code == 200:
                print(f"https://calyxos.org/install/devices/{code_name}/")

            if search_cos.status_code == 200 and code_name != "FP4":
                print(f"https://grapheneos.org/releases#{code_name}-stable")
    else:
        return "Device not found in /e/OS Devices."


def web_search_ubuntu(device_name):
    # specify the website URL
    url = "https://devices.ubuntu-touch.io"

    # retrieve the HTML of the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the list on the page
        items = soup.find("ul")

        # Loop through the items in the list
        for item in items.find_all("li"):
            # Check if the item contains the keyword
            if re.search(device_name, item.text, re.IGNORECASE):
                data_id = item.get("data-id")
                print("https://devices.ubuntu-touch.io/device/" + data_id.split("@")[0])

    else:
        return "Device not found in Ubuntu Touch Devices."


def main(device_name):
    md_res = web_markdown_search(device_name)
    web_res_eos = web_search_eos(device_name)
    web_res_ubuntu = web_search_ubuntu(device_name)
    return [md_res, web_res_eos, web_res_ubuntu]


if __name__ == "__main__":
    main()
