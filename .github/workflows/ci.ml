name: Run Shipping Bot

on:
  workflow_dispatch:   # lets you trigger manually from GitHub
  push:                # runs on every push to main
    branches:
      - main

jobs:
  run-bot:
    runs-on: ubuntu-latest   # GitHub-hosted Linux runner

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          python -m playwright install

      - name: Run bot
        run: python main.py --headless --dry-run
