# 🔍 PhD Jobs Search Filter
This simple Python script extracts and filters the RSS feed from [Academic Jobs Online](https://academicjobsonline.org).  
It focuses on PhD positions related to **dark matter**, **cosmology**, and **astroparticle physics**.

The keywords can be customized directly in the script for searching jobs in other areas:

```python
keywords = ["dark matter", "cosmology", "astroparticle"]
```

##  Functionality

- Automatically dowlnloads the RSS feed from Academic Jobs Online website
- Filters PhDs containing the keywords
- Generates and automatically opens an HTML (output.html)


## Example of keywords used
- `dark matter`
- `cosmology`
- `astroparticle`

You can modify them in the script as needed.

## Requirements

- Python 3.12
- Packages: `requests`, `beautifulsoup4`

## Installation

Install the required packages via pip
`pip install requests beautifulsoup4`


## Launch
Run the script from the terminal:
`pyhton jobs_position_filter.py`

It will open a browser tab with the filtered job listed in `output.html`.

## Author
Made by Alessandra Amosso for simplify the search of PhDs :)