import difflib
import logging

import pandas as pd


class MatchCard:
    """Use text from card to find most likely corresponding card"""

    def __init__(self, found_card_name):
        self.found_card_name = found_card_name
        self.matched_card_name = None

    def __call__(self):
        cards_df = pd.read_csv("all_cards.csv")
        transformed_card_names = cards_df["Transformed Name"]

        if self.found_card_name in transformed_card_names:
            self.matched_card_name = self.found_card_name
        else:
            matched_transformed_card_name = difflib.get_close_matches(
                self.found_card_name, transformed_card_names, n=1
            )[0]

            self.matched_card_name = cards_df[
                transformed_card_names == matched_transformed_card_name
            ]["Name"].iloc[0]


def match_card(unmatched_title):
    mc = MatchCard(unmatched_title)
    mc()
    return mc.matched_card_name


def all():
    unmatched_titles = pd.read_csv("unmatched_titles.csv")["titles"]
    for unmatched_title in unmatched_titles:
        logging.warning(match_card(unmatched_title))


# all()
