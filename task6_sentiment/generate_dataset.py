"""
Generates a realistic labeled dataset for sentiment analysis: a mix of
product reviews, social media style posts, and news-style headlines,
spanning positive, negative, and neutral sentiment, with some genuinely
hard/ambiguous examples included on purpose (sarcasm, mixed sentiment,
negation) so the model has to do real work rather than pattern-matching
on obvious keywords.
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

positive_templates = [
    "Absolutely love this {product}, exceeded all my expectations!",
    "Best {product} I've ever bought, worth every penny.",
    "This {product} works perfectly, couldn't be happier.",
    "Amazing quality for the price, highly recommend this {product}.",
    "Fast shipping and the {product} is exactly as described, great experience.",
    "I'm so impressed with this {product}, it's a game changer.",
    "Five stars, this {product} is fantastic and very well made.",
    "Customer service was wonderful and the {product} arrived early.",
    "My {product} works flawlessly, I use it every single day.",
    "Great value, the {product} performs better than I expected.",
    "This {product} made my life so much easier, thank you!",
    "Beautifully designed {product}, looks even better in person.",
    "Super happy with my purchase, the {product} is top notch.",
    "Will definitely buy this {product} again, no complaints at all.",
    "The {product} is durable, stylish, and works great.",
]

negative_templates = [
    "Terrible {product}, broke after just two days of use.",
    "Waste of money, this {product} doesn't work as advertised.",
    "Very disappointed with this {product}, poor quality overall.",
    "The {product} arrived damaged and customer service was unhelpful.",
    "Worst {product} I've ever purchased, complete garbage.",
    "Do not buy this {product}, it stopped working within a week.",
    "I regret buying this {product}, total waste of time and money.",
    "The {product} is overpriced and underperforms badly.",
    "Awful experience, the {product} was nothing like the pictures.",
    "This {product} is cheaply made and fell apart immediately.",
    "Extremely frustrated with this {product}, asking for a refund.",
    "The {product} stopped functioning after one use, very disappointing.",
    "Horrible build quality, this {product} feels like a scam.",
    "I would not recommend this {product} to anyone, total disaster.",
    "The {product} is slow, unreliable, and constantly malfunctions.",
]

neutral_templates = [
    "The {product} arrived on schedule, packaging was standard.",
    "This {product} does what it says, nothing more nothing less.",
    "I received the {product} yesterday and haven't tested it fully yet.",
    "The {product} is okay, similar to other ones I've owned.",
    "It's a {product}, works as expected for the price point.",
    "Average {product}, gets the job done but nothing special.",
    "The {product} has standard features, comparable to competitors.",
    "I bought this {product} to replace an older model, seems similar.",
    "The {product} matches the description provided on the listing.",
    "This {product} is functional, no major issues to report so far.",
    "Just an update: the {product} is still being used, no new feedback.",
    "The {product} ships in a basic box, no special packaging.",
]

hard_examples = [
    ("Yeah, this {product} is 'great' if you enjoy waiting three weeks for a refund.", "negative"),
    ("Not bad, but definitely not the best {product} I've used either.", "neutral"),
    ("I wanted to love this {product}, but the battery life ruined it for me.", "negative"),
    ("This {product} isn't terrible, it just isn't great.", "neutral"),
    ("Sure, it's cheap, but you absolutely get what you pay for with this {product}.", "negative"),
    ("The {product} looks amazing but the performance leaves a lot to be desired.", "negative"),
    ("Honestly didn't expect much, and somehow this {product} still disappointed me.", "negative"),
    ("It's not the worst {product} out there, but I wouldn't buy it again.", "negative"),
    ("This {product} isn't perfect, but it's good enough for casual use.", "neutral"),
    ("Wow, never thought a {product} could make me this happy, incredible find.", "positive"),
    ("The {product} has flaws, sure, but overall I'm genuinely satisfied with it.", "positive"),
    ("I can't say I hate this {product}, but I definitely don't love it either.", "neutral"),
]

products = ['laptop','phone case','blender','running shoes','desk chair','headphones',
            'backpack','coffee maker','tablet','monitor','keyboard','router','vacuum',
            'air fryer','smartwatch','speaker','webcam','mattress','jacket','water bottle']

news_positive = [
    "Company reports record quarterly profits, stock surges on strong earnings.",
    "New policy praised by experts for boosting economic growth significantly.",
    "Local team celebrates championship win after incredible season.",
    "Breakthrough treatment shows promising results in clinical trials.",
    "City unveils new park, residents excited about green space expansion.",
]
news_negative = [
    "Company faces backlash after massive data breach affects millions.",
    "Economists warn of recession risk as unemployment numbers rise sharply.",
    "Factory shutdown leaves hundreds of workers without jobs this week.",
    "Officials criticized for slow response during the ongoing crisis.",
    "Stock prices plummet after disappointing earnings report released.",
]
news_neutral = [
    "City council to vote on new zoning proposal next Tuesday afternoon.",
    "Quarterly report shows steady performance in line with expectations.",
    "New regulations to take effect starting next month, officials confirm.",
    "Annual conference scheduled to take place in the downtown venue.",
    "Department releases updated guidelines for upcoming fiscal year.",
]

social_positive = [
    "just tried the new coffee shop downtown and im obsessed!! best latte ever",
    "can't believe how good this movie was, definitely watching it again",
    "had the best weekend with my friends, feeling so grateful right now",
    "this playlist is literally perfect for studying, 10/10 recommend",
    "finally finished my project and it turned out amazing, so proud!!",
]
social_negative = [
    "stuck in traffic for two hours and now im late, worst monday ever",
    "why does my wifi keep dropping every five minutes this is so annoying",
    "just lost my favorite sweater at the gym, today is not my day",
    "can't believe they cancelled the show last minute, so disappointed",
    "ordered food an hour ago and it still hasn't arrived, ridiculous",
]
social_neutral = [
    "heading to the grocery store, need to pick up a few things",
    "watching the game tonight, not sure who's going to win honestly",
    "rescheduled my appointment to next week instead of this friday",
    "trying out a new recipe tonight, we'll see how it goes",
    "got my package today, haven't opened it yet",
]

rows = []
start_date = datetime(2025, 1, 1)

def add_rows(templates_or_texts, label, n, is_template, date_spread_days=365):
    for _ in range(n):
        if is_template:
            t = random.choice(templates_or_texts)
            text = t.format(product=random.choice(products))
        else:
            text = random.choice(templates_or_texts)
        days_offset = random.randint(0, date_spread_days)
        date = start_date + timedelta(days=days_offset)
        rows.append({'text': text, 'label': label, 'date': date.strftime('%Y-%m-%d'), 'source': 'review'})

add_rows(positive_templates, 'positive', 280, True)
add_rows(negative_templates, 'negative', 220, True)
add_rows(neutral_templates, 'neutral', 150, True)

for text, label in hard_examples:
    for _ in range(6):
        text_filled = text.format(product=random.choice(products))
        days_offset = random.randint(0, 365)
        date = start_date + timedelta(days=days_offset)
        rows.append({'text': text_filled, 'label': label, 'date': date.strftime('%Y-%m-%d'), 'source': 'review'})

for texts, label in [(news_positive,'positive'),(news_negative,'negative'),(news_neutral,'neutral')]:
    for t in texts:
        for _ in range(8):
            days_offset = random.randint(0, 365)
            date = start_date + timedelta(days=days_offset)
            rows.append({'text': t, 'label': label, 'date': date.strftime('%Y-%m-%d'), 'source': 'news'})

for texts, label in [(social_positive,'positive'),(social_negative,'negative'),(social_neutral,'neutral')]:
    for t in texts:
        for _ in range(8):
            days_offset = random.randint(0, 365)
            date = start_date + timedelta(days=days_offset)
            rows.append({'text': t, 'label': label, 'date': date.strftime('%Y-%m-%d'), 'source': 'social_media'})

df = pd.DataFrame(rows)
df = df.sample(frac=1, random_state=11).reset_index(drop=True)
df['id'] = range(1, len(df)+1)
df = df[['id', 'date', 'source', 'text', 'label']]

df.to_csv('sentiment_dataset.csv', index=False)
print(f"Generated {len(df)} labeled examples")
print(df['label'].value_counts())
print(df['source'].value_counts())
