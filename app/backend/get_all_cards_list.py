import csv
import json
import logging
import re

import requests

# Gets all Yu Gi HO Cards and puts them in usable format
x = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
card_infos = json.loads(x.text)["data"]

# open the file in the write mode
with open("all_cards.csv", "w", newline="", encoding="utf-8") as f:
    # create the csv writer
    writer = csv.writer(f)
    writer.writerow(
        [
            "Transformed Name",
            "Name",
        ]
    )
    for index, card_info in enumerate(card_infos):

        # write a row to the csv file
        try:
            writer.writerow(
                [
                    re.sub("[^0-9A-Z-]+", "", card_info["name"].upper()),
                    card_info["name"],
                ]
            )
        except Exception as e:
            logging.warning([card_info["name"]])
            print(card_info["name"])
            logging.warning(e)
