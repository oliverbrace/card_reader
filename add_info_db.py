import csv
import logging

import requests

# Gets all Yu Gi HO Cards and puts them in usable format


class CardRegisterAdder:
    def __init__(self, card_name):
        self.card_name = card_name
        self.card_info = None
        self.highest_card_price = None
        self.lowest_card_price = None
        self.average_card_price = None
        self.first_edition = None
        self.damaged = None

    @staticmethod
    def damaged_q():
        while True:
            response = input("Is card damaged (Y/N)").upper()

            # Check is number
            if response == "Y":
                return True
            elif response == "N":
                return False
            else:
                print("Please put either Y or N")

    @staticmethod
    def first_edition_q():
        while True:
            response = input("Is card first edition (Y/N)").upper()

            # Check is number
            if response == "Y":
                return True
            elif response == "N":
                return False
            else:
                print("Please put either Y or N")

    @staticmethod
    def pick_rarity(item_list):
        rarity_dict = {0: "Not in list"}
        user_query = "Pick the item you want: \n0. Not in list\n"
        for i, card_name in enumerate(item_list):
            rarity_dict[i + 1] = card_name
            user_query += f"{i + 1}. {card_name}\n"

        while True:
            response = input(user_query)

            # Check is number
            if response.isdigit():
                response = int(response)
            else:
                print("Please enter a valid number.")
                continue

            # Check if valid number
            if response >= 0 and response <= len(item_list):
                rarity = rarity_dict[response]
                break
            else:
                print("Please enter a valid number.")

        return rarity

    def get_card_info(self):
        card_name = self.card_name
        card_info = requests.get(
            f"http://yugiohprices.com/api/get_card_prices/{card_name}"
        )

        if card_info.json()["status"] == "success":
            self.card_info = card_info.json()
        else:
            raise Exception("Card name not found")

    def filter_card_info(self):
        card_data = self.card_info["data"]
        # Ask rarity
        rarity_list = {card["rarity"] for card in card_data}

        if len(rarity_list) == 1:
            self.rarity = rarity_list[0]
        else:
            self.rarity = self.pick_rarity(rarity_list)

        # Get rarity
        card_data = list(
            filter(
                lambda card: card["price_data"]["status"] == "success"
                and card["rarity"] == self.rarity,
                card_data,
            )
        )

        if len(card_data) == 0:
            # Card has never been sold. Can use most expensive
            logging.warning("No price info found")
            self.highest_card_price = float("nan")
            self.lowest_card_price = float("nan")
            self.average_card_price = float("nan")

        price_data = [card["price_data"]["data"]["prices"] for card in card_data]
        high_values = [card["high"] for card in price_data]
        self.highest_card_price = max(high_values)

        average_values = [card["average"] for card in price_data]
        self.average_card_price = max(average_values)

        low_values = [card["low"] for card in price_data]
        self.lowest_card_price = max(low_values)

    def write_card_to_csv(self):
        with open("card_data.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    self.card_name,
                    self.rarity,
                    self.first_edition,
                    self.damaged,
                    self.average_card_price,
                    self.highest_card_price,
                    self.lowest_card_price,
                ]
            )

    def __call__(self):
        if self.card_name is None:
            raise Exception("No card name provided")

        self.get_card_info()
        self.filter_card_info()

        self.first_edition = self.first_edition_q()
        self.damaged = self.damaged_q()
        self.write_card_to_csv()


def run():
    card_name = "Bait Doll"
    inst = CardRegisterAdder(card_name)
    inst()


# run()
