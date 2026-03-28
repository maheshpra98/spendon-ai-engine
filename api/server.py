"""
Spendon AI Engine — FastAPI Backend
REST API for the strategy generation engine.

Endpoints:
  POST /api/strategy/generate     — Generate a new marketing strategy
  POST /api/data/upload-csv       — Upload and process CSV data  
  POST /api/scraper/brand         — Scrape brand intelligence
  POST /api/strategy/generate-manual — Quick strategy from manual inputs
  GET  /api/health                — Health check
"""

import os
import json
import asyncio
from typing import Optional
from dataclasses import asdict

# FastAPI imports (install: pip install fastapi uvicorn python-multipart)
try:
    from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
except ImportError:
    print("Install dependencies: pip install fastapi uvicorn python-multipart")
    raise

from core.models import (
    CampaignRequest, ProductScope, PlanTier, Language,
    ProductInfo, BrandDNA, MarketingStrategy
)
from core.engine import StrategyEngine, AIClient
from data.processors import CSVProcessor, ManualInputProcessor
from scrapers.brand_scraper import BrandScraper


# ── App Setup ─────────────────────────────────────────────────────────

app = FastAPI(
    title="Spendon AI Engine",
    description="Regional Language Marketing Intelligence Platform — Meta-First Strategy Engine",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS", "https://spendon.ai,http://localhost").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI engine
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = os.environ.get("AI_MODEL", "claude-sonnet-4-20250514")
engine = StrategyEngine(api_key=API_KEY, model=MODEL) if API_KEY else None


# ── Request/Response Models (Pydantic) ────────────────────────────────

class ProductInput(BaseModel):
    name: str
    category: str = "General"
    price: float = 0
    description: str = ""
    usps: list[str] = []
    target_audience: str = ""


class ManualStrategyRequest(BaseModel):
    company_name: str
    monthly_budget: float
    target_cac: Optional[float] = None
    campaign_goal: str = ""
    scope: str = "single"  # single / top / catalog
    products: list[ProductInput] = []
    target_languages: list[str] = ["Hindi"]
    campaign_duration_days: int = 30
    tier: str = "free"  # free / growth / pro / enterprise

    # Optional: pre-scraped brand data
    website_url: str = ""
    brand_slogans: list[str] = []

    # Optional: pre-processed data
    sales_summary: Optional[dict] = None
    meta_ads_summary: Optional[dict] = None


class BrandScrapeRequest(BaseModel):
    company_name: str
    website_url: str = ""
    meta_page_name: str = ""
    competitor_urls: list[str] = []
    social_handles: dict = {}


class StrategyResponse(BaseModel):
    strategy_id: str
    company_name: str
    scope: str
    confidence_score: float
    executive_summary: str
    is_full_strategy: bool
    # Full strategy fields (empty for free tier)
    market_analysis: str = ""
    budget_allocation: Optional[dict] = None
    channel_recommendations: list = []
    timing_recommendations: dict = {}
    creative_briefs: list = []
    creator_matches: list = []
    predicted_cac: float = 0
    predicted_roas: float = 0
    predicted_conversions: int = 0
    # Free tier fields
    teaser_insights: list = []


# ── Helper: convert MarketingStrategy to response ─────────────────────

def strategy_to_response(strategy: MarketingStrategy) -> dict:
    """Convert internal MarketingStrategy to API response."""
    result = {
        "strategy_id": strategy.strategy_id,
        "company_name": strategy.company_name,
        "scope": strategy.scope.value,
        "confidence_score": strategy.confidence_score,
        "executive_summary": strategy.executive_summary,
        "is_full_strategy": strategy.is_full_strategy,
        "market_analysis": strategy.market_analysis,
        "predicted_cac": strategy.predicted_cac,
        "predicted_roas": strategy.predicted_roas,
        "predicted_conversions": strategy.predicted_conversions,
        "teaser_insights": strategy.teaser_insights,
    }

    if strategy.is_full_strategy:
        result["budget_allocation"] = asdict(strategy.budget_allocation) if strategy.budget_allocation else None
        result["channel_recommendations"] = strategy.channel_recommendations
        result["timing_recommendations"] = strategy.timing_recommendations
        result["creative_briefs"] = [
            {
                "language": cb.language.display_name,
                "headlines": cb.headline_variants,
                "body_copy": cb.body_copy_variants,
                "ctas": cb.cta_options,
                "format": cb.recommended_format,
                "hook": cb.hook_type,
                "visual": cb.visual_direction,
                "cultural_notes": cb.cultural_notes,
            }
            for cb in strategy.creative_briefs
        ]
        result["creator_matches"] = [
            {
                "profile": cm.name,
                "platform": cm.platform,
                "language": cm.language.display_name,
                "niche": cm.niche,
                "match_score": cm.match_score,
                "brief": cm.brief_suggestion,
            }
            for cm in strategy.creator_matches
        ]

    return result


# ── Endpoints ─────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "engine": "ready" if engine else "no_api_key",
        "model": MODEL,
        "version": "2.0.0"
    }


@app.post("/api/strategy/generate")
async def generate_strategy(req: ManualStrategyRequest):
    """
    Generate a marketing strategy from manual inputs.
    This is the primary endpoint for the MVP.
    """
    if not engine:
        raise HTTPException(500, "AI engine not configured. Set ANTHROPIC_API_KEY.")

    # Build CampaignRequest from form data
    campaign = ManualInputProcessor.build_request(
        company_name=req.company_name,
        monthly_budget=req.monthly_budget,
        target_cac=req.target_cac,
        campaign_goal=req.campaign_goal,
        scope=req.scope,
        products=[p.dict() for p in req.products],
        target_languages=req.target_languages,
        campaign_duration_days=req.campaign_duration_days,
        tier=req.tier,
    )

    # Attach brand DNA if slogans provided
    if req.brand_slogans or req.website_url:
        campaign.brand_dna = BrandDNA(
            company_name=req.company_name,
            website_url=req.website_url,
            slogans=req.brand_slogans,
        )

    # Generate strategy
    try:
        strategy = await engine.generate(campaign)
        return strategy_to_response(strategy)
    except Exception as e:
        raise HTTPException(500, f"Strategy generation failed: {str(e)}")


@app.post("/api/data/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload and process a CSV file (sales or campaign data).
    Returns structured data summary.
    """
    if not file.filename.endswith((".csv", ".tsv")):
        raise HTTPException(400, "Only CSV/TSV files supported")

    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    # Detect type and process
    reader = csv.DictReader(io.StringIO(text))
    headers = reader.fieldnames or []
    data_type = CSVProcessor.detect_type(headers)

    if data_type == "sales":
        result = CSVProcessor.process_sales_csv(text)
        return {
            "type": "sales",
            "summary": {
                "total_revenue": result.total_revenue,
                "period_months": result.period_months,
                "top_products": result.top_products[:5],
                "regional_breakdown": result.regional_breakdown,
                "growth_trend": result.growth_trend,
            }
        }
    else:
        result = CSVProcessor.process_campaign_csv(text)
        return {
            "type": "campaign",
            "summary": {
                "total_spend": result.total_spend,
                "period_days": result.period_days,
                "avg_cac": round(result.avg_cac, 2),
                "avg_cpm": round(result.avg_cpm, 2),
                "avg_cpc": round(result.avg_cpc, 2),
                "avg_ctr": round(result.avg_ctr, 2),
                "avg_roas": round(result.avg_roas, 2),
                "best_campaigns": result.best_performing_campaigns[:5],
            }
        }


@app.post("/api/scraper/brand")
async def scrape_brand(req: BrandScrapeRequest):
    """
    Scrape brand intelligence from public web sources.
    Returns a structured brand DNA profile.
    """
    if not engine:
        raise HTTPException(500, "AI engine not configured. Set ANTHROPIC_API_KEY.")

    scraper = BrandScraper(ai_client=engine.ai)
    try:
        brand_dna = await scraper.build_brand_profile(
            company_name=req.company_name,
            website_url=req.website_url,
            meta_page_name=req.meta_page_name,
            competitor_urls=req.competitor_urls,
            social_handles=req.social_handles
        )
        return asdict(brand_dna)
    except Exception as e:
        raise HTTPException(500, f"Brand scraping failed: {str(e)}")


@app.post("/api/strategy/generate-with-data")
async def generate_with_all_data(
    req: ManualStrategyRequest,
    sales_csv: Optional[UploadFile] = File(None),
    campaign_csv: Optional[UploadFile] = File(None),
):
    """
    Generate strategy with optional CSV file uploads.
    Combines manual inputs + uploaded data + optional scraping.
    """
    if not engine:
        raise HTTPException(500, "AI engine not configured. Set ANTHROPIC_API_KEY.")

    # Build base request
    campaign = ManualInputProcessor.build_request(
        company_name=req.company_name,
        monthly_budget=req.monthly_budget,
        target_cac=req.target_cac,
        campaign_goal=req.campaign_goal,
        scope=req.scope,
        products=[p.dict() for p in req.products],
        target_languages=req.target_languages,
        campaign_duration_days=req.campaign_duration_days,
        tier=req.tier,
    )

    # Process uploaded CSVs
    if sales_csv:
        content = (await sales_csv.read()).decode("utf-8", errors="ignore")
        campaign.sales_data = CSVProcessor.process_sales_csv(content)

    if campaign_csv:
        content = (await campaign_csv.read()).decode("utf-8", errors="ignore")
        campaign.meta_ads_data = CSVProcessor.process_campaign_csv(content)

    # Scrape brand DNA if URL provided
    if req.website_url:
        scraper = BrandScraper(ai_client=engine.ai)
        campaign.brand_dna = await scraper.build_brand_profile(
            company_name=req.company_name,
            website_url=req.website_url,
        )

    # Generate strategy
    try:
        strategy = await engine.generate(campaign)
        return strategy_to_response(strategy)
    except Exception as e:
        raise HTTPException(500, f"Strategy generation failed: {str(e)}")


# ── Run ───────────────────────────────────────────────────────────────

import csv
import io

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
