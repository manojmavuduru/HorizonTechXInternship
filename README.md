# Horizon TechX Internship — Project Portfolio

Five projects completed across web development, NLP, data science, and machine learning during the Horizon TechX internship. Each one is a fully working build — not a mockup — with its own README covering the technical approach and design decisions.

**Author:** [Manoj Mavuduru](https://github.com/manojmavuduru)

## Projects

| # | Project | Domain | What it is | Live demo | Code |
|---|---|---|---|---|---|
| 1 | **Lingua** | AI + NLP | Real-time browser translator, 25 languages, speech synthesis, no backend | [Demo](https://manojmavuduru.github.io/horizontechx_tasks/task1_translation/) | [`task1_translation`](./task1_translation) |
| 2 | **Atlas** | NLP | FAQ chatbot using TF-IDF + cosine similarity, not keyword matching | [Demo](https://manojmavuduru.github.io/horizontechx_tasks/task2_chatbot/) | [`task2_chatbot`](./task2_chatbot) |
| 3 | **Atlas Insights** | Data Analysis / EDA | Full EDA pipeline on a 5,000-row e-commerce dataset with intentional data-quality issues | [Notebook](./task3_eda/EDA_Notebook.ipynb) | [`task3_eda`](./task3_eda) |
| 4 | **Pulse** | Data Visualization | Interactive analytics dashboard, Chart.js, built on the Task 3 dataset | [Demo](https://manojmavuduru.github.io/horizontechx_tasks/task4_dashboard/) | [`task4_dashboard`](./task4_dashboard) |
| 5 | **Sentir** | Sentiment Analysis / ML | Lexicon vs. trained classifier (97.5% accuracy), model ported live to JavaScript | [Demo](https://manojmavuduru.github.io/horizontechx_tasks/task6_sentiment/) | [`task6_sentiment`](./task6_sentiment) |

*(Demo links go live once GitHub Pages is enabled on this repo — see [Deployment](#deployment) below.)*

## What ties these together

Each project was built to avoid the shortcut a typical student submission takes:

- **Lingua** makes a real translation API call with race-condition handling, instead of a hardcoded phrase dictionary.
- **Atlas** does actual TF-IDF vectorization and cosine similarity matching, instead of `if message.includes(...)`.
- **Atlas Insights** was run against a dataset seeded with real data-quality problems (duplicates, bad values, inconsistent text, missing fields), so the cleaning step required actual judgment calls, documented and justified.
- **Pulse** is genuinely interactive (click-to-filter, dual-axis charts) and built on the same cleaned dataset from the EDA task, with numbers that trace back to real analysis — not placeholder values.
- **Sentir** trains and honestly compares two different models (a rule-based baseline and a trained classifier), then re-implements the winning model's math in vanilla JavaScript and verifies the ported version matches the original scikit-learn output to 3 decimal places.

Every web project (1, 2, 4, 5) is a single self-contained `index.html` — no build step, no backend, no API keys required to run. That was a deliberate constraint: anyone can open the file or the live link and see it work immediately.

## Tech stack

- **Frontend:** Vanilla JavaScript, HTML, CSS (no frameworks — by choice, to keep every demo a zero-install, zero-build artifact)
- **Data / ML:** Python, pandas, numpy, scikit-learn, matplotlib, seaborn, VADER
- **Visualization:** Chart.js
- **Analysis:** Jupyter Notebook

## Deployment

Every web task runs standalone by opening its `index.html` — no server needed. To make the demo links above live:

1. Go to the repo's **Settings → Pages**
2. Under **Build and deployment**, set **Source: Deploy from a branch**
3. Branch: **main**, folder: **/ (root)** → Save

GitHub Pages will then serve each task at `https://manojmavuduru.github.io/HorizonTechXInternship/<task-folder>/`, matching the links in the table above.

## Repo structure

```
HorizonTechXInternship/
├── task1_translation/   # Lingua — translation tool
├── task2_chatbot/       # Atlas — FAQ chatbot
├── task3_eda/           # Atlas Insights — EDA notebook + report
├── task4_dashboard/     # Pulse — analytics dashboard
├── task6_sentiment/     # Sentir — sentiment analysis
└── README.md
```
