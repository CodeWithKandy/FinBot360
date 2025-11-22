# Deployment Guide

## 1. Push to GitHub
Since you have a `.gitignore` file ready, you can push your code to GitHub.

1.  Initialize Git (if not done):
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```
2.  Create a new repository on GitHub.
3.  Link and push:
    ```bash
    git remote add origin <YOUR_REPO_URL>
    git branch -M main
    git push -u origin main
    ```

## 2. Deploy to Streamlit Cloud
1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Log in with GitHub.
3.  Click **"New app"**.
4.  Select your repository, branch (`main`), and main file path: `ui/dashboard.py` (or `main.py` if you adjust the entry point, but pointing directly to `ui/dashboard.py` is often easier for Streamlit Cloud).
5.  Click **"Deploy!"**.

## Dependencies
Ensure `requirements.txt` is up to date. It should include:
```
streamlit
yfinance
plotly
pandas
pandas_ta
feedparser
```
