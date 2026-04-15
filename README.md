# Data_viz

A One Piece data visualization and analysis project using scraped JSON data from oparchive.com.

## Overview

This project analyzes One Piece characters, Devil Fruits, and islands data to generate visual insights through Python.

The main script, `vizonpe.py`, loads three JSON datasets and produces six PNG charts including:

- Character status distribution
- Top 20 bounties
- Devil Fruit type breakdown and average bounty
- Power type vs bounty comparison
- Most represented races
- Island count by region

## Files

- `vizonpe.py` — main analysis and chart generation script
- `characters.json` — scraped character dataset
- `devil_fruits.json` — scraped Devil Fruit dataset
- `islands.json` — scraped island dataset
- `requirement.txt` — package requirements

## Installation

1. Install Python 3.8+.
2. Install required packages:

```bash
pip install pandas numpy matplotlib
```

> If `requirement.txt` is available, you can also use:
>
> ```bash
> pip install -r requirement.txt
> ```

## Usage

Run the script from the project folder:

```bash
python vizonpe.py
```

The script will print dataset summaries and generate image files such as:

- `graph1_statuts.png`
- `graph2_top20_primes.png`
- `graph3_fruits_demon.png`
- `graph4_pouvoirs_primes.png`
- `graph5_races.png`
- `graph6_iles_regions.png`

## Data Source

Source data was obtained from:

- https://oparchive.com/pages/characters.html

## Notes

- Keep the JSON files in the same folder as `vizonpe.py`.
- The analysis includes French labels, titles, and comments in the script.
- The generated charts are saved to the local folder.
