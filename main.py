import json
from utils.puller import Puller


if __name__ == "__main__":
    with open("sites.json") as json_file:
        data = json.load(json_file)

        d = {}

        for site_obj in data["sites"]:
            d[site_obj["name"]] = Puller(site_obj["params"])
        print("Loaded", len(d.keys()), "sites.")

        q = input("Input Search Query: ")

        for site in d:
            print(d[site].search_query(q))