"""
Spendon AI Engine — Configuration & Data Models
Core data structures used across all modules.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


# ── Product scope levels ──────────────────────────────────────────────

class ProductScope(Enum):
    SINGLE = "single"          # One SKU / product launch
    TOP_PRODUCTS = "top"       # 3-10 bestsellers
    FULL_CATALOG = "catalog"   # Entire product range


# ── Supported regional languages ──────────────────────────────────────

class Language(Enum):
    HINDI = "hi"
    TAMIL = "ta"
    TELUGU = "te"
    KANNADA = "kn"
    MALAYALAM = "ml"
    BENGALI = "bn"
    MARATHI = "mr"
    GUJARATI = "gu"
    PUNJABI = "pa"
    ODIA = "or"
    ASSAMESE = "as"
    URDU = "ur"

    @property
    def display_name(self):
        return {
            "hi": "Hindi", "ta": "Tamil", "te": "Telugu", "kn": "Kannada",
            "ml": "Malayalam", "bn": "Bengali", "mr": "Marathi", "gu": "Gujarati",
            "pa": "Punjabi", "or": "Odia", "as": "Assamese", "ur": "Urdu"
        }[self.value]

    @property
    def region(self):
        return {
            "hi": "North India, Central India",
            "ta": "Tamil Nadu, Puducherry",
            "te": "Andhra Pradesh, Telangana",
            "kn": "Karnataka",
            "ml": "Kerala",
            "bn": "West Bengal, Tripura",
            "mr": "Maharashtra",
            "gu": "Gujarat",
            "pa": "Punjab, Haryana",
            "or": "Odisha",
            "as": "Assam",
            "ur": "Uttar Pradesh, Jammu & Kashmir"
        }[self.value]


# ── Tier / plan levels ────────────────────────────────────────────────

class PlanTier(Enum):
    FREE = "free"
    GROWTH = "growth"
    PRO = "pro"
    ENTERPRISE = "enterprise"


# ── Input data structures ─────────────────────────────────────────────

@dataclass
class ProductInfo:
    """Single product or SKU data."""
    name: str
    category: str
    price: float
    currency: str = "INR"
    description: str = ""
    usps: list[str] = field(default_factory=list)
    target_audience: str = ""
    past_performance: dict = field(default_factory=dict)


@dataclass
class SalesData:
    """Processed sales data summary (from CSV or API)."""
    total_revenue: float
    period_months: int
    top_products: list[dict] = field(default_factory=list)
    regional_breakdown: dict = field(default_factory=dict)
    seasonal_patterns: dict = field(default_factory=dict)
    growth_trend: str = ""  # "growing", "stable", "declining"


@dataclass
class MetaAdsData:
    """Processed Meta Ads performance data."""
    total_spend: float
    period_days: int
    avg_cac: float
    avg_cpm: float
    avg_cpc: float
    avg_ctr: float
    avg_roas: float
    best_performing_campaigns: list[dict] = field(default_factory=list)
    audience_insights: dict = field(default_factory=dict)
    creative_performance: list[dict] = field(default_factory=list)
    regional_performance: dict = field(default_factory=dict)


@dataclass
class BrandDNA:
    """Web-scraped brand intelligence profile."""
    company_name: str
    website_url: str = ""
    slogans: list[str] = field(default_factory=list)
    taglines: list[str] = field(default_factory=list)
    brand_tone: str = ""       # "formal", "casual", "playful", "premium"
    core_values: list[str] = field(default_factory=list)
    product_descriptions: dict = field(default_factory=dict)
    social_bio: str = ""
    content_pillars: list[str] = field(default_factory=list)
    past_ad_themes: list[str] = field(default_factory=list)
    competitor_insights: list[dict] = field(default_factory=list)


@dataclass
class CampaignRequest:
    """Complete input for strategy generation."""
    # Company info
    company_name: str
    brand_dna: Optional[BrandDNA] = None

    # Product scope
    scope: ProductScope = ProductScope.SINGLE
    products: list[ProductInfo] = field(default_factory=list)

    # Budget & goals
    monthly_budget: float = 0
    target_cac: Optional[float] = None
    campaign_goal: str = ""
    campaign_duration_days: int = 30

    # Target markets
    target_languages: list[Language] = field(default_factory=list)

    # Data inputs
    sales_data: Optional[SalesData] = None
    meta_ads_data: Optional[MetaAdsData] = None

    # Plan
    tier: PlanTier = PlanTier.FREE


# ── Output data structures ────────────────────────────────────────────

@dataclass
class BudgetAllocation:
    """Budget split across channels, regions, and products."""
    total_budget: float
    channel_split: dict = field(default_factory=dict)    # {"reels": 40, "feed": 30, ...}
    regional_split: dict = field(default_factory=dict)    # {"Tamil Nadu": 35, ...}
    product_split: dict = field(default_factory=dict)     # {"Product A": 50, ...}
    daily_pacing: list[dict] = field(default_factory=list)
    scenarios: dict = field(default_factory=dict)         # conservative/moderate/aggressive


@dataclass
class CreativeBrief:
    """AI-generated creative brief for one language market."""
    language: Language
    headline_variants: list[str] = field(default_factory=list)
    body_copy_variants: list[str] = field(default_factory=list)
    cta_options: list[str] = field(default_factory=list)
    recommended_format: str = ""   # "reels", "carousel", "static", "story"
    hook_type: str = ""            # "emotional", "urgency", "social_proof", "value"
    visual_direction: str = ""
    cultural_notes: str = ""
    predicted_ctr: float = 0


@dataclass
class CreatorMatch:
    """AI-matched creator recommendation."""
    name: str
    platform: str
    language: Language
    niche: str
    followers: int
    engagement_rate: float
    match_score: float
    estimated_cost: float
    brief_suggestion: str = ""


@dataclass
class MarketingStrategy:
    """Complete AI-generated marketing strategy output."""
    # Meta
    strategy_id: str = ""
    company_name: str = ""
    scope: ProductScope = ProductScope.SINGLE
    confidence_score: float = 0

    # Strategy summary
    executive_summary: str = ""
    market_analysis: str = ""

    # Budget
    budget_allocation: Optional[BudgetAllocation] = None

    # Channel strategy
    channel_recommendations: list[dict] = field(default_factory=list)
    timing_recommendations: dict = field(default_factory=dict)

    # Creatives per language
    creative_briefs: list[CreativeBrief] = field(default_factory=list)

    # Creators
    creator_matches: list[CreatorMatch] = field(default_factory=list)

    # Predictions
    predicted_cac: float = 0
    predicted_roas: float = 0
    predicted_conversions: int = 0

    # For free tier: teaser insights
    teaser_insights: list[str] = field(default_factory=list)
    is_full_strategy: bool = True
