"""
Task 6: Sentiment Analysis (AI + Data Science)
Horizon TechX Internship

Two approaches are built and compared, not just one, to demonstrate real
understanding of the trade-offs between them:

  1. LEXICON-BASED BASELINE (VADER) -- a rule-based sentiment scorer that
     requires no training data, handles negation and intensifiers via
     hand-built linguistic rules, and is the standard "good baseline" in
     production NLP before reaching for a trained model.

  2. TRAINED ML CLASSIFIER (TF-IDF + Logistic Regression) -- a supervised
     model trained on labeled examples, which should outperform the
     lexicon baseline specifically on the dataset's harder examples
     (sarcasm, mixed sentiment, negation-heavy phrasing) since it learns
     patterns from data rather than applying fixed rules.

Both are evaluated honestly with a held-out test set, a confusion matrix,
and per-class precision/recall -- not just a single accuracy number.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

plt.rcParams['figure.dpi'] = 130
sns.set_style("whitegrid", {'grid.linestyle': ':', 'grid.color': '#dddddd'})
INK, AMBER, GREEN, RED = '#2E4057', '#D9A24B', '#5B8C6E', '#A3475C'

df = pd.read_csv('sentiment_dataset.csv', parse_dates=['date'])
print(f"Dataset: {len(df)} examples")
print(df['label'].value_counts())

# ============================================================
# 1. TRAIN/TEST SPLIT
# ============================================================
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['label'], test_size=0.25, random_state=42, stratify=df['label']
)
print(f"\nTrain: {len(X_train)}, Test: {len(X_test)}")

# ============================================================
# 2. LEXICON BASELINE -- VADER
# ============================================================
analyzer = SentimentIntensityAnalyzer()

def vader_predict(text):
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        return 'positive'
    elif compound <= -0.05:
        return 'negative'
    else:
        return 'neutral'

vader_preds_test = X_test.apply(vader_predict)
vader_acc = accuracy_score(y_test, vader_preds_test)
vader_f1 = f1_score(y_test, vader_preds_test, average='macro')
print(f"\n--- VADER (lexicon baseline) ---")
print(f"Accuracy: {vader_acc:.3f}")
print(f"Macro F1: {vader_f1:.3f}")
print(classification_report(y_test, vader_preds_test))

# ============================================================
# 3. TRAINED ML CLASSIFIER -- TF-IDF + Logistic Regression
# ============================================================
vectorizer = TfidfVectorizer(
    max_features=3000,
    ngram_range=(1, 2),
    stop_words='english',
    min_df=2
)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

clf = LogisticRegression(max_iter=1000, C=3.0, class_weight='balanced')
clf.fit(X_train_vec, y_train)

ml_preds_test = clf.predict(X_test_vec)
ml_acc = accuracy_score(y_test, ml_preds_test)
ml_f1 = f1_score(y_test, ml_preds_test, average='macro')
print(f"\n--- TF-IDF + Logistic Regression ---")
print(f"Accuracy: {ml_acc:.3f}")
print(f"Macro F1: {ml_f1:.3f}")
print(classification_report(y_test, ml_preds_test))

# also fit a Naive Bayes for a second ML comparison point
nb_clf = MultinomialNB()
nb_clf.fit(X_train_vec, y_train)
nb_preds_test = nb_clf.predict(X_test_vec)
nb_acc = accuracy_score(y_test, nb_preds_test)
nb_f1 = f1_score(y_test, nb_preds_test, average='macro')
print(f"\n--- TF-IDF + Naive Bayes ---")
print(f"Accuracy: {nb_acc:.3f}")
print(f"Macro F1: {nb_f1:.3f}")

# ============================================================
# 4. HARD EXAMPLES -- where lexicon-based scoring should struggle
# ============================================================
hard_test_cases = [
    "Yeah, this laptop is 'great' if you enjoy waiting three weeks for a refund.",
    "Not bad, but definitely not the best phone I've used either.",
    "I wanted to love this blender, but the noise ruined it for me.",
    "This vacuum isn't terrible, it just isn't great.",
    "Sure, it's cheap, but you absolutely get what you pay for with this jacket.",
]
print("\n--- Hard example comparison (sarcasm / mixed sentiment / negation) ---")
hard_results = []
for text in hard_test_cases:
    vader_pred = vader_predict(text)
    ml_pred = clf.predict(vectorizer.transform([text]))[0]
    hard_results.append({'text': text, 'vader': vader_pred, 'ml_model': ml_pred})
    print(f"VADER: {vader_pred:10s} | ML: {ml_pred:10s} | {text[:70]}")

pd.DataFrame(hard_results).to_csv('hard_examples_comparison.csv', index=False)

# ============================================================
# 5. SAVE MODEL COMPARISON SUMMARY
# ============================================================
comparison = pd.DataFrame({
    'model': ['VADER (lexicon)', 'TF-IDF + Logistic Regression', 'TF-IDF + Naive Bayes'],
    'accuracy': [vader_acc, ml_acc, nb_acc],
    'macro_f1': [vader_f1, ml_f1, nb_f1]
})
comparison.to_csv('model_comparison.csv', index=False)
print(f"\n{comparison}")

# ============================================================
# 6. CONFUSION MATRIX (best model)
# ============================================================
labels_order = ['negative', 'neutral', 'positive']
cm = confusion_matrix(y_test, ml_preds_test, labels=labels_order)

fig, ax = plt.subplots(figsize=(6, 5.2))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels_order, yticklabels=labels_order,
            square=True, linewidths=0.5, cbar_kws={'shrink':0.8}, ax=ax)
ax.set_xlabel('Predicted label')
ax.set_ylabel('True label')
ax.set_title('Confusion matrix — TF-IDF + Logistic Regression', fontweight='bold', fontsize=12.5)
plt.tight_layout()
plt.savefig('confusion_matrix.png', bbox_inches='tight')
plt.close()

# ============================================================
# 7. SENTIMENT TREND OVER TIME (apply trained model to full dataset)
# ============================================================
df['predicted_sentiment'] = clf.predict(vectorizer.transform(df['text']))
df['month'] = df['date'].dt.to_period('M').astype(str)

monthly_sentiment = df.groupby(['month', 'predicted_sentiment']).size().unstack(fill_value=0)
monthly_sentiment = monthly_sentiment.reindex(columns=['negative','neutral','positive'], fill_value=0)
monthly_pct = monthly_sentiment.div(monthly_sentiment.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(12, 5.5))
ax.stackplot(monthly_pct.index, monthly_pct['negative'], monthly_pct['neutral'], monthly_pct['positive'],
             colors=[RED, '#C7CCDC', GREEN], labels=['Negative','Neutral','Positive'], alpha=0.85)
ax.set_title('Sentiment mix over time (model-predicted)', fontweight='bold', fontsize=13.5)
ax.set_ylabel('Share of mentions (%)')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)
ax.spines[['top','right']].set_visible(False)
plt.xticks(rotation=45, ha='right')
ax.set_ylim(0, 100)
plt.tight_layout()
plt.savefig('sentiment_trend.png', bbox_inches='tight')
plt.close()

# ============================================================
# 8. SENTIMENT BY SOURCE
# ============================================================
source_sentiment = df.groupby(['source', 'predicted_sentiment']).size().unstack(fill_value=0)
source_sentiment = source_sentiment.reindex(columns=['negative','neutral','positive'], fill_value=0)
source_pct = source_sentiment.div(source_sentiment.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(9, 5))
source_pct.plot(kind='barh', stacked=True, color=[RED, '#C7CCDC', GREEN], ax=ax, width=0.6)
ax.set_title('Sentiment mix by source', fontweight='bold', fontsize=13)
ax.set_xlabel('Share (%)')
ax.set_ylabel('')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, frameon=False)
ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig('sentiment_by_source.png', bbox_inches='tight')
plt.close()

# ============================================================
# 9. TOP PREDICTIVE WORDS PER CLASS (model interpretability)
# ============================================================
feature_names = np.array(vectorizer.get_feature_names_out())
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for idx, label in enumerate(clf.classes_):
    coefs = clf.coef_[idx]
    top_idx = np.argsort(coefs)[-10:]
    top_words = feature_names[top_idx]
    top_scores = coefs[top_idx]
    color = RED if label == 'negative' else (GREEN if label == 'positive' else '#8FA6CB')
    axes[idx].barh(top_words, top_scores, color=color)
    axes[idx].set_title(f"Top terms — {label}", fontweight='bold', fontsize=12)
    axes[idx].spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig('top_predictive_words.png', bbox_inches='tight')
plt.close()

# Save model artifacts for the demo app to use
import pickle
with open('sentiment_model.pkl', 'wb') as f:
    pickle.dump({'vectorizer': vectorizer, 'classifier': clf}, f)

df.to_csv('sentiment_dataset_with_predictions.csv', index=False)

print("\nAll analysis complete. Visualizations and model saved.")
