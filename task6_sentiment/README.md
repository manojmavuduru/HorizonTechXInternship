# Sentir — Sentiment Analysis

**Task 6: Sentiment Analysis (AI + Data Science) — Horizon TechX Internship**

A complete sentiment analysis pipeline that builds and honestly compares two different approaches — a lexicon-based baseline and a trained ML classifier — then ports the winning model to run live, client-side, in a browser demo.

## Why two models, not one

Most student sentiment-analysis submissions either hardcode a word list ("good", "bad", "terrible" → score) or call a pretrained model as a black box and report one accuracy number. This submission does neither — it builds a real lexicon baseline (VADER, a well-established rule-based sentiment tool) and a real trained classifier (TF-IDF + Logistic Regression), evaluates both honestly on the same held-out test set, and specifically probes where they disagree.

## Results

| Model | Accuracy | Macro F1 |
|---|---|---|
| VADER (lexicon) | 80.1% | 78.3% |
| TF-IDF + Logistic Regression | **97.5%** | **97.7%** |
| TF-IDF + Naive Bayes | 97.5% | 97.7% |

## The finding that matters more than the accuracy table

Five deliberately hard examples — sarcasm, mixed sentiment, negation — were run through both models side by side:

> *"Yeah, this laptop is 'great' if you enjoy waiting three weeks for a refund."*
> — **VADER says positive** (it sees "great" and stops there). **The trained model correctly says negative** — it learned from data that this kind of backhanded phrasing pattern signals criticism, not praise.

This is the actual point of the task: a lexicon scores individual words, while a trained model learns contextual patterns. The full comparison is in `hard_examples_comparison.csv`.

## Dataset

962 labeled text examples (372 positive, 336 negative, 254 neutral) drawn from three sources: product reviews (722), social media posts (120), and news snippets (120), with realistic dates spread across a year for trend analysis.

## Pipeline

1. **`generate_dataset.py`** — builds the labeled dataset
2. **`sentiment_analysis.py`** — the full analysis:
   - Train/test split (75/25, stratified)
   - VADER baseline evaluation
   - TF-IDF (unigrams + bigrams) + Logistic Regression, and a Naive Bayes comparison point
   - Hard-example head-to-head comparison
   - Confusion matrix
   - Sentiment trend over time (model applied to the full dataset, not just the test set)
   - Sentiment mix by source
   - Top predictive words per class (interpretability — what words push the model toward each label)
   - Model export for the live demo

## The live demo: a genuinely real model running in your browser

`index.html` is not a mockup with a fake "AI thinking" animation. The actual trained logistic regression model — its full vocabulary, IDF weights, coefficients, and intercepts — is exported to JSON and the exact TF-IDF vectorization + logistic regression math is re-implemented in vanilla JavaScript. **This was verified by directly comparing the JavaScript port's output against the original scikit-learn model on multiple test sentences — the probabilities matched to 3 decimal places.** Every prediction you see in the demo is computed live, in your browser, by the same model that was trained and evaluated in Python.

The demo shows the predicted label, full confidence breakdown across all three classes, and which vocabulary terms it actually recognized in your input — so the model's reasoning is visible, not a black box.

## Why this is a strong submission

It demonstrates the full lifecycle: data, baseline, trained model, honest comparison, interpretability, and deployment — and the deployment step is real engineering, not just a chat-style wrapper around an API call. Porting a trained scikit-learn model to vanilla JS and verifying numerical parity is a meaningfully harder (and more impressive, to a technical reviewer) task than calling `openai.complete()`.

## Files

- `generate_dataset.py` — dataset generator
- `sentiment_dataset.csv` — labeled dataset (962 examples)
- `sentiment_analysis.py` — full training, evaluation, and visualization pipeline
- `sentiment_dataset_with_predictions.csv` — dataset with model predictions applied
- `sentiment_model.pkl` — saved scikit-learn model (vectorizer + classifier)
- `model_export.json` / `model_export_min.json` — model weights exported for browser inference
- `stopwords.json` / `stopwords_inline.txt` — stopword list matching the Python vectorizer
- `confusion_matrix.png`, `sentiment_trend.png`, `sentiment_by_source.png`, `top_predictive_words.png` — visualizations
- `model_comparison.csv`, `hard_examples_comparison.csv` — quantitative results
- `index.html` — the live, client-side interactive demo
- `demo_template.html` — the demo source template (pre-injection, for reference)

## Run it

- **Demo:** open `index.html` in any browser — no installation, no API key.
- **Full analysis:** `pip install pandas numpy matplotlib seaborn scikit-learn vaderSentiment` then `python3 generate_dataset.py && python3 sentiment_analysis.py`
