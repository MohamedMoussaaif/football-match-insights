
import json
from pathlib import Path
from urllib.request import urlopen

BASE_URL = (
    "https://raw.githubusercontent.com/"
    "statsbomb/open-data/master/data"
)

MATCH_ID = 18244

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def download_json(url: str, output_path: Path) -> dict | list:
    """Download one JSON file and save a local copy."""
    print(f"Downloading: {url}")

    with urlopen(url, timeout=30) as response:
        data = json.load(response)

    output_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Saved: {output_path}")
    return data


# Download the small match metadata file.
matches_url = f"{BASE_URL}/matches/16/2.json"
matches = download_json(
    matches_url,
    RAW_DIR / "ucl_2016_2017_matches.json",
)

# Find the final by its stage and match ID.
finals = [
    match for match in matches
    if match["match_id"] == MATCH_ID
    and match["competition_stage"]["name"] == "Final"
]

if not finals:
    raise ValueError("The requested final was not found.")

match = finals[0]

print(
    f"\nSelected: {match['home_team']['home_team_name']} "
    f"{match['home_score']} - {match['away_score']} "
    f"{match['away_team']['away_team_name']}"
)

# Download only this match's events and lineups.
download_json(
    f"{BASE_URL}/events/{MATCH_ID}.json",
    RAW_DIR / f"{MATCH_ID}_events.json",
)

download_json(
    f"{BASE_URL}/lineups/{MATCH_ID}.json",
    RAW_DIR / f"{MATCH_ID}_lineups.json",
)

# Save a compact record of the selected match.
(RAW_DIR / f"{MATCH_ID}_match_info.json").write_text(
    json.dumps(match, indent=2, ensure_ascii=False),
    encoding="utf-8",
)

print("\nMatch data downloaded successfully!")
