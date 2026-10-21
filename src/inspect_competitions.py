
import pandas as pd

url = (
    "https://raw.githubusercontent.com/"
    "statsbomb/open-data/master/data/competitions.json"
)

competitions = pd.read_json(url)

print("Available competitions and seasons:\n")
print(
    competitions[
        ["competition_id", "season_id", "competition_name", "season_name"]
    ].to_string(index=False)
)

print("\nEnglish competition candidates:\n")

english = competitions[
    competitions["country_name"].str.contains(
        "England", case=False, na=False
    )
    | competitions["competition_name"].str.contains(
        "Premier League|Championship",
        case=False,
        na=False,
        regex=True,
    )
]

print(
    english[
        ["competition_id", "season_id", "competition_name", "season_name"]
    ].to_string(index=False)
)
