import csv
import logging

import requests

# Gets all Yu Gi HO Cards and puts them in usable format


class CardRegisterAdder:
    def __init__(
        self,
        card_name=None,
        rarity="Common",
        print_tag=None,
        first_edition=None,
        damaged=None,
        notes="",
    ):
        self.card_name = card_name
        self.rarity = rarity
        self.print_tag = print_tag
        self.first_edition = first_edition
        self.damaged = damaged
        self.notes = notes
        self.match_type = None

        self._card_info = None
        self._card_prices = None
        self._possible_rarities = None
        self._possible_print_tags = None

    @property
    def card_info(self):
        if self._card_info is None:
            self._card_info = self.get_card_info()

        return self._card_info

    @property
    def card_prices(self):
        if self._card_prices is None:
            self._card_prices = self.get_card_prices()

        return self._card_prices

    @property
    def possible_rarities(self):
        if self._possible_rarities is None:
            self._possible_rarities = self.get_rarities()

        return self._possible_rarities

    @property
    def possible_print_tags(self):
        if self._possible_print_tags is None:
            self._possible_print_tags = self.get_print_tags()

        return self._possible_print_tags

    def get_card_info(self):
        card_name = self.card_name
        card_info = requests.get(
            f"http://yugiohprices.com/api/get_card_prices/{card_name}"
        )

        if card_info.json()["status"] == "success":
            return card_info.json()["data"]
        else:
            raise Exception("Card name not found")

    def get_rarities(self):
        return list({card["rarity"] for card in self.card_info})

    def get_print_tags(self):
        return list({card["print_tag"] for card in self.card_info})

    def card_match_r_pt(self):
        """Rarity and print tag search

        Returns:
            _type_: _description_
        """
        matches = list(
            filter(
                lambda card: card["price_data"]["status"] == "success"
                and card["rarity"] == self.rarity
                and card["print_tag"] == self.print_tag,
                self.card_info,
            )
        )
        if matches != []:
            self.match_type = "R/PT"

        return matches

    def card_match_r(self):
        """Rarity search

        Returns:
            _type_: _description_
        """
        matches = list(
            filter(
                lambda card: card["price_data"]["status"] == "success"
                and card["rarity"] == self.rarity,
                self.card_info,
            )
        )

        if matches != []:
            self.match_type = "R"

        return matches

    def card_match_pt(self):
        """Print tag search

        Returns:
            _type_: _description_
        """
        matches = list(
            filter(
                lambda card: card["price_data"]["status"] == "success"
                and card["print_tag"] == self.print_tag,
                self.card_info,
            )
        )

        if matches != []:
            self.match_type = "PT"

        return matches

    @staticmethod
    def card_price_range_calc(cards_data):
        """If multiple matches calculate range

        Args:
            cards_data (list): All price data of cards matched
        """
        price_data = [card["price_data"]["data"]["prices"] for card in cards_data]

        price_high = [card["high"] for card in price_data]
        highest_high = max(price_high)
        lowest_high = min(price_high)

        price_average = [card["average"] for card in price_data]
        highest_average = max(price_average)
        lowest_average = min(price_average)

        price_low = [card["low"] for card in price_data]
        highest_low = max(price_low)
        lowest_low = min(price_low)

        card_price_range = {
            "high": f"£{lowest_high}-£{highest_high}",
            "average": f"£{lowest_average}-£{highest_average}",
            "low": f"£{lowest_low}-£{highest_low}",
        }

        return card_price_range

    def get_card_prices(self):
        # ? This search may need to change depending on what
        # ? Is more important rarity or print tag
        card_data = self.card_match_r_pt()

        if card_data == []:
            card_data = self.card_match_r()

        if card_data == []:
            card_data = self.card_match_pt()

        if card_data == []:
            # Card has never been sold
            logging.warning("No price info found")
            self.highest_card_price = float("-")
            self.average_card_price = float("-")
            self.lowest_card_price = float("-")
            self.match_type = "None"
            return

        if len(card_data) == 1:
            # One match found
            card_prices = card_data[0]["price_data"]["data"]["prices"]
            self.highest_card_price = f"£{card_prices['high']}"
            self.average_card_price = f"£{card_prices['average']}"
            self.lowest_card_price = f"£{card_prices['low']}"
            return

        # Multiple matches found
        card_prices = self.card_price_range_calc(card_data)
        self.highest_card_price = card_prices["high"]
        self.average_card_price = card_prices["average"]
        self.lowest_card_price = card_prices["low"]
        return

    def write_card_to_csv(self):
        with open("card_data.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    self.card_name,
                    self.rarity,
                    self.print_tag,
                    self.first_edition,
                    self.damaged,
                    self.lowest_card_price,
                    self.average_card_price,
                    self.highest_card_price,
                    self.notes,
                ]
            )

    def __call__(self):
        self.filter_card_info()

        self.write_card_to_csv()


def run():
    card_name = "Bait Doll"
    inst = CardRegisterAdder(card_name)
    inst()


# run()
