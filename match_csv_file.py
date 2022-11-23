import difflib

import pandas as pd

cards_df = pd.read_csv("all_cards.csv")
transformed_card_names = cards_df["Transformed Name"]

titles_df = pd.read_csv("unmatched_titles.csv")
titles_s = titles_df["titles"]
matched_titles = cards_df[transformed_card_names.isin(titles_s)]
unmatched_titles = titles_s[~titles_s.isin(transformed_card_names)]
estimated_titles = []
for unmatched in unmatched_titles:
    estimated_titles.append(
        difflib.get_close_matches(unmatched, transformed_card_names, n=1)[0]
    )

estimated_matches = cards_df[transformed_card_names.isin(estimated_titles)]
pd.concat([matched_titles, estimated_matches])["Name"].to_csv(
    "matched_titles.csv", index=False
)
