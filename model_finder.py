import csv
import requests

csv_only = False


def model_finder(search_term, **kwargs):

    kwargs["csv_only"] = False

    url = "https://storage.googleapis.com/play_public/supported_devices.csv"

    response = requests.get(url)

    reader = csv.reader(response.text.strip().split('\n'))

    header = next(reader)

    #search_term = input("Enter a device name to search for: ")

    code_names = set()

    for row in reader:
        if search_term.lower() in row[1].lower() or search_term.lower() in row[2].lower() or search_term.lower() in row[3].lower():
            if row[2] not in code_names:
                code_names.add(row[2])
                print(row)
                # print(row[2])
    if not kwargs["csv_only"]:
        for code_name in code_names:
            search_eos = requests.get(f"https://doc.e.foundation/devices/{code_name}")
            if search_eos.status_code == 200:
                print(f"https://doc.e.foundation/devices/{code_name}")

            search_cos = requests.get(f"https://calyxos.org/install/devices/{code_name}/")
            if search_cos.status_code == 200:
                print(f"https://calyxos.org/install/devices/{code_name}/")

            if search_cos.status_code == 200 and code_name != "FP4":
                print(f"https://grapheneos.org/releases#{code_name}-stable")

        if code_names:
            print(f"https://forum.xda-developers.com/search/?type=post&q={code_names.pop()}")


def main(device_name, **kwargs):
    model_finder(device_name, **kwargs)


if __name__ == "__main__":
    main()