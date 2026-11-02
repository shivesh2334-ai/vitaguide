# VitaGuide

Personalized supplement and dietary decision support, with a Vercel-compatible web interface and the original Streamlit application.

## Features preserved

- All 17 original profile fields, including demographics, diet, religious preferences, region, laboratory categories, medications and lifestyle factors.
- Original `SupplementKnowledgeBase` and `SupplementRecommender` classes, preserved verbatim in `api/engine.py`.
- Risk stratification, prioritized supplement doses/rationales/duration, food sources, dietary advice, warnings, monitoring, cultural and regional guidance.
- Educational resources and the complete original nutrient, condition, dietary and regional knowledge datasets.
- JSON report export; the web version also supports printing and medicine search.
- Original Streamlit UI remains runnable and includes the new medicine directory.

The web input adapter normalizes sex, pregnancy, cultural and condition labels for the existing engine. It forwards deficiency/risk indicators to prevent the low-risk branch from hiding an abnormal profile, and maps low vitamin D labels to the existing engine's expected value. The engine's clinical rules themselves have not been rewritten. Not all collected fields drive a specific recommendation: this is rule-based software, not a comprehensive clinical or interaction engine, and no external AI service is called.

## Indian medicines and supplements

`public/indian-medicines.json` contains five sourced India-market examples in each of 23 categories (115 category listings). Products can appear in several nutrient categories because they contain multiple ingredients. Each record includes formulation notes, type, a source link and review date. Combination products are not substitutes for single-nutrient deficiency treatment; confirm exact pack and dose.

The retinal category contains five related eye-health supplements, **not five verified AREDS2-equivalent formulations**. Indian formulations in the cited comparative study differed from trial composition. Clinician review is required, especially for pregnancy, renal disease, electrolyte replacement and high-dose vitamin products. Hospital-only potassium presentations are explicitly identified.

Listings were reviewed on 2 November 2026. Availability and composition may change. No price or stock guarantee is made.

## Vercel deployment

Import `shivesh2334-ai/vitaguide` from GitHub into the intended Vercel team:

- Framework preset: Other
- Root directory: repository root
- Output directory: `public`
- Build command: empty
- Install command: empty
- Production branch: `main`

`vercel.json` configures static assets and Vercel automatically serves `api/analyze.py` as a Python function. No API keys or database are required. The function uses only Python's standard library. The existing root `requirements.txt` is retained for Streamlit use.

The API accepts POST JSON at `/api/analyze` and returns a normalized profile and recommendations. GET on the same path is a health check. Profiles are processed in memory for the request; the app has no database, patient persistence, analytics or profile logging. JSON download is generated in the browser.

**Deployment status:** initial project creation was rejected by Vercel because the selected team reached the 200-project Hobby limit. No deployment or live URL is claimed. Free a project slot or upgrade the team before importing this repository. No existing project was modified or deleted.

## Original Streamlit application

```bash
pip install -r requirements.txt
streamlit run vitaguide_app.py
```

## Verification

```bash
python tests/test_engine.py
python -m py_compile api/analyze.py api/engine.py vitaguide_app.py
node --check public/app.js
```

The engine check confirms AST equality with the original Streamlit classes, representative profile scenarios, 100 deterministic varied profiles, all 17 inputs, and all 115 sourced medicine listings. This verifies software behavior, not clinical validity of every original recommendation. A live production check remains pending deployment.

## Clinical references retained from the original application

USPSTF vitamin/mineral supplementation recommendation (2022), NIH Office of Dietary Supplements, COSMOS, Physicians' Health Study II and SELECT. The original educational content and dose thresholds are preserved; they should be reviewed against current guidance before clinical use.
