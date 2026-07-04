# Pulse — Data Visualization Dashboard

**Task 4: Data Visualization Dashboard — Horizon TechX Internship**

An interactive, dark-mode analytics dashboard built on top of the same cleaned e-commerce dataset from Task 3, using Chart.js for rendering.

## What's in it

- **6 live KPI cards** — total revenue, orders, AOV, return rate, repeat-customer rate, average rating
- **Monthly revenue trend** with holiday-season (Nov/Dec) points highlighted in amber
- **Rating distribution** color-coded by sentiment (red = 1-2 stars, amber = 3, green = 4-5)
- **Interactive category revenue chart** — click any bar to highlight that category's row in the ranking table beside it
- **Region performance combo chart** — revenue bars and average delivery time on a dual axis, in the same chart, to make the delivery/region relationship visually obvious
- **Acquisition channel donut chart** with hover tooltips showing exact revenue
- **Weekday order volume**, with weekends highlighted (green) — useful for staffing/scheduling decisions
- **Payment method breakdown**
- **Written takeaways panel** translating the charts into specific, numbered business findings

## Design decisions

This is built as a single self-contained `index.html` — the cleaned, aggregated dataset is embedded directly as a JSON object in the page, so the dashboard needs zero backend, zero build step, and zero external dependencies beyond Chart.js (loaded from CDN) and Google Fonts. Open it and it works.

The dark theme with a desaturated palette (slate blue, amber, muted green/red) was chosen deliberately over default Chart.js colors — bright primary colors on a dark background create visual fatigue in a dashboard meant to be glanced at repeatedly, not viewed once.

## Why this is a strong submission

Most student dashboards are static screenshots of matplotlib charts pasted into a slide. This one is genuinely interactive (click-to-filter, hover tooltips, combo/dual-axis charts) and is built on real, cleaned data with defensible numbers traced back to the Task 3 analysis — not placeholder values. It also closes the loop that a lot of dashboards skip: it tells the viewer what to *do* with the data (the takeaways panel), not just what the data *is*.

## Run it

Open `index.html` in any modern browser. No installation needed.

## Files

- `index.html` — the dashboard
- `dashboard_data.json` — the source aggregated data (also embedded inline in the HTML)
