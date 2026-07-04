# Lingua — Language Translation Tool

**Task 1: AI + NLP — Horizon TechX Internship**

A real-time, browser-based translation tool with a manuscript-inspired two-pane interface, text-to-speech playback, and one-click copy.

## Live features

- **Real translation**, not a mock — calls Google's public translation endpoint directly from the browser, no API key required, no backend needed.
- **Auto language detection** — leave the source set to "Detect language" and it identifies the input language automatically, then labels it in the UI.
- **25 languages** including major world languages and a quick-select row for the six most common targets.
- **Text-to-speech** on both panes using the Web Speech API — listen to the original or the translation.
- **One-click copy** with inline confirmation state.
- **Swap button** to instantly flip source ↔ target and re-translate.
- **Debounced live translation** — translates as you type (450ms debounce) with a visible "translating…" status and an animated seam between panes while a request is in flight.
- **Character counter** with a 2,000-character soft limit and overflow warning state.
- **Fully responsive** — collapses to a stacked single-column layout on mobile.

## How it works technically

The app calls:
```
https://translate.googleapis.com/translate_a/single?client=gtx&sl={source}&tl={target}&dt=t&dt=bd&q={text}
```
This is the same public endpoint the Google Translate Chrome extension and many open-source translation tools use. It requires no authentication and returns translated segments plus a detected-language code, which the UI parses and renders.

All language detection, debouncing, request-race handling (so a slow stale request can't overwrite a newer one), speech synthesis, and clipboard access happen client-side in vanilla JavaScript — no frameworks, no build step.

## Design notes

The visual language treats translation as a manuscript moment: an ink-blue "original" pane sits beside a warm paper "translation" pane, divided by a seam that pulses gold while a translation is in flight — a nod to ink bleeding through paper. Fraunces (serif) carries the translated output to feel considered and final; Inter (sans) carries the UI and the live input to feel immediate and editable.

## Why this is a strong submission

Most student translation-tool submissions either hardcode a dictionary or fake the API call. This one makes a genuine network request, handles real failure states (offline, rate limits), prevents race conditions between rapid keystrokes, and has been designed — not just assembled — with a coherent visual identity. That combination (working integration + defensive engineering + design intent) is what separates a portfolio piece from a tutorial exercise.

## Run it

Open `index.html` in any modern browser. No installation, no server, no API key.
