# College Student Dietary & Lifestyle Dashboard

This repository contains a Streamlit app (app.py) for exploratory analysis of a college student food choices dataset (food_coded.csv).

What I added to make this repo ready for deployment on Streamlit Community Cloud (and other hosting platforms):

- `requirements.txt` — lists Python dependencies required to run the app.
- `.streamlit/config.toml` — Streamlit server config for headless deployments.
- `Procfile` — optional, useful if deploying to platforms like Heroku.
- `README.md` — instructions for running locally and deploying to Streamlit.

Quick start (local)

1. Create a virtual environment and activate it:

   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate     # Windows

2. Install dependencies:

   python -m pip install -r requirements.txt

3. Run the app:

   streamlit run app.py

Deploy to Streamlit Community Cloud

1. Go to https://streamlit.io/cloud and sign in with GitHub.
2. Click "New app" -> select this repository and branch `main` and set the "Main file" to `app.py`.
3. Deploy. Streamlit will automatically install dependencies from `requirements.txt`.

Notes & troubleshooting

- The app uses the `wordcloud` package which sometimes requires system build tools to compile. If you see build errors when installing `wordcloud`, try adding the relevant OS packages (for Debian/Ubuntu: `apt-get update && apt-get install -y build-essential libfreetype6-dev`), or use a pre-built wheel.
- Plotly's trendline option uses `statsmodels`, so it is included in the requirements.
- If Streamlit fails to find `food_coded.csv`, make sure the dataset is in the repository root (it currently is).

If you want, I can also:
- Pin dependency versions in `requirements.txt`.
- Add a GitHub Actions workflow to run linting/tests before deploy.
- Create a sample `Procfile`/`Dockerfile` tailored for other hosts.
