# Spendon AI Engine v2.0

**Regional Language Marketing Intelligence Platform — Meta-First Strategy Engine**

An AI model that transforms a company's sales data, Meta ad performance, and web-scraped brand intelligence into high-conversion marketing strategies in 12+ Indian regional languages.

---

## Architecture

```
spendon-ai/
├── main.py                  # Entry point (CLI + server)
├── requirements.txt         # Dependencies
│
├── core/
│   ├── models.py            # Data models (ProductScope, Language, CampaignRequest, etc.)
│   └── engine.py            # Strategy engine — orchestrates the 6-step prompt chain
│
├── prompts/
│   └── chains.py            # Prompt chain system (brand → market → budget → creative → creators → synthesis)
│
├── data/
│   └── processors.py        # CSV/Excel processors, manual input handler
│
├── scrapers/
│   └── brand_scraper.py     # Web scraper for brand DNA (website, Meta Ad Library, social, competitors)
│
└── api/
    └── server.py            # FastAPI REST API
```

## How the AI Model Works

The engine runs a **6-step prompt chain** — each step builds on the previous:

```
Step 1: Brand Analysis
  └→ Analyzes scraped brand DNA, slogans, tone, positioning
  
Step 2: Market Intelligence  
  └→ Analyzes sales data + Meta performance per regional language market
  
Step 3: Budget Optimization
  └→ Allocates budget across channels, regions, products (scope-aware)
  
Step 4: Creative Strategy (parallel, per language)
  └→ Generates native regional ad copy — NOT translated English
  
Step 5: Creator Matching
  └→ Recommends ideal regional creator profiles per language market
  
Step 6: Synthesis
  └→ Assembles everything into a coherent strategy with predictions
```

### Key Design Decisions

1. **Prompt chains, not a single prompt**: Each step is specialized. Brand analysis feeds market intelligence, which feeds budget optimization, etc. This produces dramatically better output than dumping everything into one prompt.

2. **Scope-aware pipeline**: The prompts fundamentally change based on whether the user selected single product, top products, or full catalog scope. It's not a filter — it changes the analysis methodology.

3. **Transcreation, not translation**: The creative strategy prompts explicitly instruct the AI to create native regional content, not translate English. A Tamil ad should feel like it was conceived by a Tamil marketer.

4. **Freemium intelligence**: Free tier runs steps 1-3 + a teaser synthesis. Paid tiers run all 6 steps. The free output is designed to prove value and create demand for the full strategy.

5. **Parallel language generation**: Step 4 runs concurrently for all target languages, cutting generation time significantly.

---

## Setup

```bash
# 1. Clone and enter directory
cd spendon-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# 4. Test the model
python main.py test

# 5. Start the API server
python main.py serve
# → API docs at http://localhost:8000/docs
```

---

## API Endpoints

### `POST /api/strategy/generate`
Generate a marketing strategy from manual inputs.

```json
{
  "company_name": "FreshBasket",
  "monthly_budget": 300000,
  "target_cac": 200,
  "campaign_goal": "Launch cold-pressed juice in South India",
  "scope": "single",
  "products": [
    {
      "name": "Cold-Pressed Juice Combo",
      "category": "Health & Wellness",
      "price": 599,
      "usps": ["100% natural", "No preservatives"]
    }
  ],
  "target_languages": ["Tamil", "Kannada"],
  "tier": "growth",
  "website_url": "https://freshbasket.in",
  "brand_slogans": ["Farm Fresh, Always Fresh"]
}
```

### `POST /api/data/upload-csv`
Upload sales or campaign CSV. Auto-detects type.

### `POST /api/scraper/brand`
Scrape brand intelligence from web sources.

```json
{
  "company_name": "FreshBasket",
  "website_url": "https://freshbasket.in",
  "meta_page_name": "FreshBasket",
  "competitor_urls": ["https://competitor1.com"]
}
```

### `POST /api/strategy/generate-with-data`
Full pipeline: manual inputs + CSV uploads + brand scraping in one call.

---

## Data Inputs Supported

| Input | How | What It Provides |
|-------|-----|------------------|
| **Manual form** | JSON body | Budget, goals, products, languages |
| **CSV upload** | File upload | Sales data OR campaign performance |
| **Meta API** | OAuth (production) | Ad spend, CAC, ROAS, audiences |
| **Web scraping** | URL input | Brand DNA, slogans, competitor intel |

---

## Product Scope System

| Scope | Use Case | What Changes |
|-------|----------|-------------|
| **Single** | Product launch, seasonal push | Deep focus on one SKU. Product-specific CAC, audiences, creatives. |
| **Top Products** | Multi-product optimization | Cross-product budget split, cannibalization analysis, bundle strategies. |
| **Full Catalog** | Brand-level strategy | Category grouping, portfolio rebalancing, seasonal rotation. |

---

## Supported Languages

Hindi, Tamil, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati, Punjabi, Odia, Assamese, Urdu

Each language gets its own creative brief with native copy, cultural context, and regional creator recommendations.

---

## Monetization Tiers

| Tier | Price | Scope | What They Get |
|------|-------|-------|---------------|
| Free | ₹0 | Single (limited) | Teaser insights, high-level tips |
| Growth | ₹25K-50K/mo | Single + Top | Full strategy, 3 languages, creative briefs |
| Pro | ₹75K-1.5L/mo | All scopes | 8 languages, creator matching, competitive intel |
| Enterprise | Custom | All + custom | Done-for-you, custom training, dedicated AM |

---

## Production Deployment Notes

1. **Web Scraping**: Replace simplified HTTP fetching with Playwright for JS-heavy sites. Use Meta Ad Library API with proper access tokens.

2. **Database**: Add PostgreSQL for strategy storage, Redis for caching prompt results, Pinecone for creator embeddings.

3. **Meta OAuth**: Implement Facebook Login for Business to pull Ads Manager data directly.

4. **Background Jobs**: Use Celery + Redis for async strategy generation (takes 30-60 seconds for full pipeline).

5. **Rate Limiting**: Claude API has rate limits. Implement queuing for concurrent users.

6. **Model Selection**: Use `claude-sonnet-4-20250514` for speed/cost balance. Upgrade to Opus for enterprise-tier quality.
