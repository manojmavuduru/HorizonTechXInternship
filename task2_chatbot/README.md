# Atlas — AI Chatbot for FAQs

**Task 2: NLP — Horizon TechX Internship**

A genuine NLP-driven FAQ assistant: TF-IDF vectorization plus cosine similarity for intent matching, not a keyword if/else chain.

## What makes this "real" NLP

A lot of student FAQ-bot submissions hardcode `if (message.includes("shipping"))`. This implementation actually builds a small information-retrieval pipeline:

1. **Tokenization** — lowercases input, strips punctuation, removes stopwords (the, is, how, what, etc.)
2. **Corpus construction** — 20 intents, each with 3-4 paraphrased example questions (so the model learns the *intent*, not one exact phrasing)
3. **TF-IDF vectorization** — computes term frequency-inverse document frequency across the whole question corpus, so common words ("how", "do") are downweighted and distinctive words ("warranty", "exchange") are upweighted
4. **Cosine similarity** — the user's message is vectorized the same way and compared against every example question in the corpus; the highest-scoring intent wins
5. **Confidence floor** — matches below 32% similarity are rejected rather than guessed at, and the bot offers related topics instead of a wrong answer

This means the bot correctly matches paraphrases it's never seen verbatim — e.g. "when's my stuff getting here" will still match the shipping-time intent even though that exact phrase isn't in the training questions, because the shared distinctive terms after stopword removal score highly.

## Knowledge base

20 intents across 7 categories: shipping, returns/refunds, account, payment, pricing/promotions, product, orders, and support — modeled on a realistic e-commerce FAQ.

## UI features

- Chat interface with typing indicator and randomized response latency (feels alive, not instant)
- Each bot answer shows which intent matched and the confidence score, so the matching is transparent rather than a black box
- "Popular topics" sidebar with one-click sample questions
- Low-confidence fallback suggests related topics by tag overlap instead of failing silently
- Fully client-side — no API calls, no backend, runs from a single HTML file

## Why this is a strong submission

It demonstrates an actual understanding of how retrieval-based NLP systems work (vectorization, weighting, similarity scoring, confidence thresholds) rather than disguising string matching as AI. The confidence display and graceful fallback also show production-mindedness: real systems must handle "I don't know" gracefully, not just the happy path.

## Run it

Open `index.html` in any modern browser. No installation, no API key, no server.
