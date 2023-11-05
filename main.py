import csv
import json
import re

import inquirer
import requests

import jsonSearch
import model_finder
import websiteSearch
import sys


# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def question_with_choices(message, choices):
    """Prompt the user to select something from the choices.

    :keyword
    message -- string shown to the user
    choices -- the list of strings to choose from
    :returns string with the choice
    """
    choices.append("Exit")
    questions = [inquirer.List("question",
                               message,
                               choices,
                               ),
                 ]
    answers = inquirer.prompt(questions)
    if answers["question"] == "Exit":
        exit(0)
    else:
        try:
            return answers["question"]
        except TypeError:
            exit(0)


def question_with_text(message):
    """Prompt the user to input any kind of text but only text.

    :keyword
    message -- string shown to the user
    :returns the typed in text by the user
    """
    questions = [inquirer.Text("text",
                               message,
                               )]
    answers = inquirer.prompt(questions)
    try:
        return answers["text"]
    except TypeError:
        exit(0)


def los_search(device_name):
    search_los = requests.get("https://wiki.lineageos.org/search.json")
    los = json.loads(search_los.content.decode())
    for item in los:
        for key, value in item.items():
            if key == "url" and device_name in value:
                return True


def pixel_search(device_name):
    search_los = requests.get("https://wiki.pixelexperience.org/search.json")
    pex = json.loads(search_los.content.decode())
    for item in pex:
        for key, value in item.items():
            if key == "url" and device_name in value:
                return True


def elixir_search(device_name):
    list_request = requests.get(
        "https://raw.githubusercontent.com/ProjectElixir-Devices/official_devices/A13/README.md")
    readme = list_request.text.split("\n")
    start = False
    for item in readme:
        if item == "<!--START_SECTION:devices-->":
            start = True
        if re.search(device_name, item, re.IGNORECASE) and start:
            return item[item.find("(") + 1:item.find(")")]
        if item == "<!--END_SECTION:devices-->":
            break


def search(query, dict_list):
    """Search in a list of dictionaries for a query string.

    :keyword
    query     -- The string to search for
    dict_list -- A list of dictionaries
    :returns a list of matching dictionaries."""
    res = []
    for item in dict_list:
        if query in item["title"]:
            res.append(item)
    return res


def main(device_name):
    """Convert device_name to its code_name by searching in googles Play Services requirement sheet.
    """
    links = {"LineageOS           ": "n/a",
             "/e/OS               ": "n/a",
             "GrapheneOS          ": "n/a",
             "CalyxOS             ": "n/a",
             "Project Elixir OS   ": "n/a",
             "Pixel Experience OS ": "n/a",
             "LineageOS + MicroG  ": "n/a"}

    results = []
    dev_csv = csv.reader(open('google_devices.csv', "r"), delimiter=",")
    for row in dev_csv:
        brand = device_name.split(" ")[0]
        model = device_name.replace(brand, "").strip()
        if re.search(brand, row[0], re.IGNORECASE):
            if re.search(model, row[1], re.IGNORECASE):
                results.append(row)
        elif re.search(device_name, row[1], re.IGNORECASE):
            results.append(row)
        elif re.search(device_name, row[2], re.IGNORECASE):
            results.append(row)

    if len(results) > 1:
        result = question_with_choices("choose", results)
        code_name = result[2]
    elif len(results) == 0:
        code_name = device_name
    else:
        code_name = results[0][2]

    if los_search(code_name):
        links["LineageOS           "] = "https://wiki.lineageos.org/devices/" + code_name

    if pixel_search(code_name):
        links["Pixel Experience OS "] = "https://wiki.pixelexperience.org/devices/" + code_name

    if elixir_search(device_name) is not None:
        links["Project Elixir OS   "] = "https://projectelixiros.com/device/" + elixir_search(device_name)

    search_eos = requests.get(f"https://doc.e.foundation/devices/{code_name}")
    if search_eos.status_code == 200:
        links["/e/OS               "] = f"https://doc.e.foundation/devices/{code_name}"

    search_cos = requests.get(f"https://calyxos.org/install/devices/{code_name}/")
    if search_cos.status_code == 200:
        links["CalyxOS             "] = f"https://calyxos.org/install/devices/{code_name}/"

    if search_cos.status_code == 200 and code_name != "FP4":
        links["GrapheneOS          "] = f"https://grapheneos.org/releases#{code_name}-stable"

    search_losmg = requests.get(f"https://download.lineage.microg.org/{code_name}/")
    if search_losmg.status_code == 200:
        links["LineageOS + MicroG  "] = f"https://download.lineage.microg.org/{code_name}/"

    print("Found the following OSes:")
    for key, value in links.items():
        print(key + ": " + value)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == "-h":
            print("usage: osFinder -g  -- only searches within the google csv.")
        while sys.argv[1] == "-g":
            try:
                device_name = input("Enter Device name: ")
            except KeyboardInterrupt:
                exit(0)
            model_finder.main(device_name, csv_only=True)

    while True:
        try:
            device_name = input("Enter Device name: ")
        except KeyboardInterrupt:
            exit(0)
        web_results = websiteSearch.main(device_name)
        json_results = jsonSearch.main(device_name)
        results = web_results + json_results
        do_google_csv = True
        for result in results:
            if result:
                print(result)
            else:
                do_google_csv = False
        if do_google_csv:
            print("maybe try the Name from the google csv:")
            model_finder.main(device_name)
