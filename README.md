# cpa-automate
Generate paperwork for CPA freelance photo jobs

## Setup

1. Install Requirements

`pip install -r requirements.txt`

2. Create your config file config.py

Config file consists of the following constants:

- `EVENT_RATE`
The rate for event jobs, $100/hr (2018).

- `PORTRAIT RATE`
The rate for portrait jobs, $120/hr (2018).

- `CREDENTIALS_PATH`
The path to the created JSON file downloaded from the generated Service Account Key.

- `SPREADSHEET_URL`
Browser URL to the spreadsheet.

IMPORTANT: Share the spreadsheet with the client_email generated in the Service Account Key JSON file (this will be different from the email that you associate the API keys with)
