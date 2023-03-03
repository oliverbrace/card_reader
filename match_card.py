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
                self.found_card_name, transformed_card_names, n=1, cutoff=0.8
            )

        if len(matched_transformed_card_name) != 0:
            card_name = cards_df[
                transformed_card_names == matched_transformed_card_name[0]
            ]["Name"].iloc[0]

            self.matched_card_name = card_name
            logging.info(f"Card match: {card_name}")
        else:
            # logging.warning("Failed to find card. Try again.")
            pass


def match_card(unmatched_title):
    mc = MatchCard(unmatched_title)
    mc()
    return mc.matched_card_name
