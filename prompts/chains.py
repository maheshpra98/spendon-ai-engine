"""
Spendon AI Engine — Prompt Chain System
Multi-step prompt architecture for strategy generation.

Each "chain" is a sequence of specialized prompts that build on each other:
  1. Brand Analysis → understands the company
  2. Market Intelligence → analyzes data + regional context  
  3. Budget Optimization → allocates spend
  4. Creative Strategy → generates regional content briefs
  5. Creator Matching → recommends influencers
  6. Synthesis → assembles the final strategy

The chain adapts based on:
  - Product scope (single / top / catalog)
  - Available data (Meta API vs CSV vs manual)
  - Plan tier (free gets teasers, paid gets full strategy)
"""

from core.models import (
    CampaignRequest, ProductScope, PlanTier, Language,
    BrandDNA, SalesData, MetaAdsData
)


# ── SYSTEM PROMPT (shared across all chains) ──────────────────────────

SYSTEM_PROMPT = """You are SpendOn AI, an expert marketing strategist specializing in 
Indian regional language markets and Meta (Facebook + Instagram) advertising.

You have deep expertise in:
- Indian consumer behavior across language markets (Hindi, Tamil, Telugu, Kannada, etc.)
- Meta Ads optimization: audience targeting, creative strategy, budget allocation, CAC modeling
- Regional cultural nuances: festivals, dialects, buying patterns, content preferences
- D2C and SMB brand marketing in India
- Influencer/creator marketing in regional language markets

Your output must be:
- Data-driven: ground recommendations in the provided performance data
- Culturally authentic: not translated English, but natively conceived regional content
- Actionable: specific enough that a marketing team can execute immediately
- Honest: flag uncertainties, don't over-promise on predictions

Always respond in structured JSON format as specified in each prompt."""


# ── CHAIN 1: BRAND ANALYSIS ──────────────────────────────────────────

def build_brand_analysis_prompt(request: CampaignRequest) -> str:
    """Analyze brand DNA, positioning, and voice."""

    brand_context = ""
    if request.brand_dna:
        b = request.brand_dna
        brand_context = f"""
SCRAPED BRAND INTELLIGENCE:
- Company: {b.company_name}
- Website: {b.website_url}
- Slogans: {', '.join(b.slogans) if b.slogans else 'Not found'}
- Taglines: {', '.join(b.taglines) if b.taglines else 'Not found'}
- Brand tone: {b.brand_tone or 'Unknown'}
- Core values: {', '.join(b.core_values) if b.core_values else 'Not specified'}
- Social bio: {b.social_bio or 'Not available'}
- Content pillars: {', '.join(b.content_pillars) if b.content_pillars else 'Not identified'}
- Past ad themes: {', '.join(b.past_ad_themes) if b.past_ad_themes else 'No data'}
- Product descriptions: {str(b.product_descriptions) if b.product_descriptions else 'None'}
"""
    products_context = ""
    for p in request.products:
        products_context += f"""
  - {p.name} ({p.category}): ₹{p.price}
    USPs: {', '.join(p.usps) if p.usps else 'Not specified'}
    Description: {p.description or 'None'}
    Target audience: {p.target_audience or 'Not specified'}
"""

    return f"""Analyze this brand and create a comprehensive brand profile that will guide 
all subsequent marketing strategy decisions.

COMPANY: {request.company_name}
PRODUCT SCOPE: {request.scope.value}
CAMPAIGN GOAL: {request.campaign_goal}
{brand_context}

PRODUCTS:
{products_context if products_context else 'No specific products provided'}

TARGET MARKETS: {', '.join(l.display_name + ' (' + l.region + ')' for l in request.target_languages)}

Respond in JSON:
{{
  "brand_profile": {{
    "positioning": "one-line brand positioning statement",
    "voice_attributes": ["attribute1", "attribute2", "attribute3"],
    "brand_personality": "2-3 sentence description",
    "key_differentiators": ["diff1", "diff2"],
    "emotional_territory": "the emotional space this brand owns"
  }},
  "product_analysis": [
    {{
      "product_name": "...",
      "core_value_prop": "...",
      "regional_appeal": {{"language_code": "why this product fits this market"}},
      "competitive_position": "..."
    }}
  ],
  "brand_consistency_guidelines": {{
    "must_include": ["elements that must appear in all content"],
    "must_avoid": ["things that would be off-brand"],
    "tone_spectrum": "formal-to-casual position"
  }}
}}"""


# ── CHAIN 2: MARKET INTELLIGENCE ─────────────────────────────────────

def build_market_intelligence_prompt(
    request: CampaignRequest,
    brand_analysis: dict
) -> str:
    """Analyze market data, regional context, and competitive landscape."""

    sales_context = ""
    if request.sales_data:
        s = request.sales_data
        sales_context = f"""
SALES DATA ({s.period_months} months):
- Total revenue: ₹{s.total_revenue:,.0f}
- Growth trend: {s.growth_trend}
- Top products: {str(s.top_products[:5])}
- Regional breakdown: {str(s.regional_breakdown)}
- Seasonal patterns: {str(s.seasonal_patterns)}
"""

    meta_context = ""
    if request.meta_ads_data:
        m = request.meta_ads_data
        meta_context = f"""
META ADS PERFORMANCE ({m.period_days} days):
- Total spend: ₹{m.total_spend:,.0f}
- Average CAC: ₹{m.avg_cac:.0f}
- Average CPM: ₹{m.avg_cpm:.0f}
- Average CPC: ₹{m.avg_cpc:.1f}
- Average CTR: {m.avg_ctr:.2f}%
- Average ROAS: {m.avg_roas:.1f}x
- Best campaigns: {str(m.best_performing_campaigns[:3])}
- Audience insights: {str(m.audience_insights)}
- Creative performance: {str(m.creative_performance[:5])}
- Regional performance: {str(m.regional_performance)}
"""

    competitor_context = ""
    if request.brand_dna and request.brand_dna.competitor_insights:
        competitor_context = f"""
COMPETITOR INTELLIGENCE:
{str(request.brand_dna.competitor_insights)}
"""

    scope_instruction = {
        ProductScope.SINGLE: "Focus analysis on the single product's market position in each target region.",
        ProductScope.TOP_PRODUCTS: "Analyze each product's regional fit. Identify cannibalization risks and cross-sell opportunities.",
        ProductScope.FULL_CATALOG: "Analyze at category level. Identify which categories to push in which regions. Consider portfolio balance."
    }[request.scope]

    return f"""Based on the brand analysis and available data, generate market intelligence 
for each target regional language market.

BRAND ANALYSIS (from previous step):
{str(brand_analysis)}

{sales_context}
{meta_context}
{competitor_context}

PRODUCT SCOPE: {request.scope.value}
SCOPE INSTRUCTION: {scope_instruction}
TARGET LANGUAGES: {', '.join(l.display_name for l in request.target_languages)}
MONTHLY BUDGET: ₹{request.monthly_budget:,.0f}

For each target language market, analyze:
1. Market size and opportunity
2. Cultural context (festivals, buying behavior, content preferences)
3. Current performance (if Meta data available)
4. Competitive gaps and opportunities
5. Product-market fit score (1-100)

Respond in JSON:
{{
  "regional_analysis": [
    {{
      "language": "language_code",
      "language_name": "...",
      "market_opportunity": "high/medium/low",
      "opportunity_reasoning": "...",
      "cultural_context": {{
        "upcoming_festivals": ["festival1 (date)", "festival2 (date)"],
        "buying_behavior": "...",
        "content_preferences": "video/static/carousel preference and why",
        "peak_engagement_times": "...",
        "dialect_notes": "..."
      }},
      "product_fit_score": 85,
      "product_fit_reasoning": "...",
      "current_performance": "summary of how brand is doing here (if data available)",
      "competitive_gaps": ["gap1", "gap2"],
      "recommended_priority": "primary/secondary/tertiary"
    }}
  ],
  "cross_market_insights": {{
    "strongest_market": "...",
    "highest_growth_potential": "...",
    "budget_priority_order": ["lang1", "lang2", "lang3"],
    "seasonal_timing_notes": "..."
  }}
}}"""


# ── CHAIN 3: BUDGET OPTIMIZATION ─────────────────────────────────────

def build_budget_optimization_prompt(
    request: CampaignRequest,
    brand_analysis: dict,
    market_intelligence: dict
) -> str:
    """Optimize budget allocation across channels, regions, and products."""

    scope_rules = {
        ProductScope.SINGLE: """
SINGLE PRODUCT RULES:
- All budget goes to one product
- Split across regional markets based on fit scores
- Recommend channel mix per region
- Include 3 budget scenarios (conservative/moderate/aggressive)""",

        ProductScope.TOP_PRODUCTS: """
TOP PRODUCTS RULES:
- Split budget across products based on regional fit and CAC
- Flag cannibalization risks (products competing for same audience)
- Recommend per-product channel allocation
- Include cross-sell budget allocation
- Include 3 budget scenarios""",

        ProductScope.FULL_CATALOG: """
FULL CATALOG RULES:
- Group products into categories first
- Allocate brand awareness vs product conversion budget (typically 20/80 for D2C)
- Seasonal rotation: which categories get priority this month
- Per-category regional allocation
- Include 3 budget scenarios"""
    }[request.scope]

    return f"""Generate an optimized Meta ad budget allocation plan.

BUDGET: ₹{request.monthly_budget:,.0f}/month for {request.campaign_duration_days} days
TARGET CAC: {f'₹{request.target_cac:.0f}' if request.target_cac else 'Not specified (optimize for lowest)'}
CAMPAIGN GOAL: {request.campaign_goal}

BRAND ANALYSIS: {str(brand_analysis)}
MARKET INTELLIGENCE: {str(market_intelligence)}

HISTORICAL META PERFORMANCE:
{f'Average CAC: ₹{request.meta_ads_data.avg_cac:.0f}, ROAS: {request.meta_ads_data.avg_roas:.1f}x' if request.meta_ads_data else 'No historical data available — use industry benchmarks for Indian D2C brands'}

{scope_rules}

PRODUCTS: {[p.name for p in request.products]}

Respond in JSON:
{{
  "budget_allocation": {{
    "channel_split": {{
      "meta_reels": {{"percentage": 40, "reasoning": "..."}},
      "meta_feed": {{"percentage": 25, "reasoning": "..."}},
      "meta_stories": {{"percentage": 15, "reasoning": "..."}},
      "meta_messenger": {{"percentage": 10, "reasoning": "..."}},
      "creator_collab": {{"percentage": 10, "reasoning": "..."}}
    }},
    "regional_split": {{
      "language_code": {{"percentage": 40, "budget_inr": 200000, "reasoning": "..."}}
    }},
    "product_split": {{
      "product_name": {{"percentage": 50, "reasoning": "..."}}
    }}
  }},
  "spend_pacing": {{
    "daily_budget": 0,
    "weekly_pattern": "description of spend distribution across the week",
    "creative_refresh_cycle": "every N days",
    "fatigue_signals": ["signal1", "signal2"]
  }},
  "scenarios": {{
    "conservative": {{
      "budget": 0,
      "predicted_cac": 0,
      "predicted_roas": 0,
      "predicted_conversions": 0,
      "risk_level": "low"
    }},
    "moderate": {{
      "budget": 0,
      "predicted_cac": 0,
      "predicted_roas": 0,
      "predicted_conversions": 0,
      "risk_level": "medium"
    }},
    "aggressive": {{
      "budget": 0,
      "predicted_cac": 0,
      "predicted_roas": 0,
      "predicted_conversions": 0,
      "risk_level": "high"
    }}
  }},
  "optimization_notes": "key recommendations for maximizing ROI"
}}"""


# ── CHAIN 4: CREATIVE STRATEGY (per language) ────────────────────────

def build_creative_strategy_prompt(
    request: CampaignRequest,
    brand_analysis: dict,
    market_intelligence: dict,
    budget_allocation: dict,
    target_language: Language
) -> str:
    """Generate creative briefs for a specific language market."""

    regional_data = {}
    if isinstance(market_intelligence, dict):
        for r in market_intelligence.get("regional_analysis", []):
            if r.get("language") == target_language.value:
                regional_data = r
                break

    return f"""Generate Meta ad creative briefs in {target_language.display_name} for 
the {target_language.region} market.

CRITICAL: You are NOT translating English copy. You are CREATING original 
{target_language.display_name} marketing content that feels native to {target_language.region}.
Think like a {target_language.display_name}-speaking marketer who has never seen the English version.

BRAND: {request.company_name}
BRAND VOICE: {str(brand_analysis.get('brand_profile', {}).get('voice_attributes', []))}
BRAND SLOGANS: {', '.join(request.brand_dna.slogans) if request.brand_dna and request.brand_dna.slogans else 'None provided'}

PRODUCTS: {[p.name + ' — ' + p.description for p in request.products]}
USPs: {[p.usps for p in request.products]}

REGIONAL CONTEXT:
{str(regional_data.get('cultural_context', 'No specific regional data'))}

BUDGET FOR THIS MARKET: Check budget allocation for {target_language.value}
CAMPAIGN GOAL: {request.campaign_goal}

Generate 3 creative concepts, each with multiple copy variants.
For each concept, the {target_language.display_name} copy must:
- Use natural {target_language.display_name} phrasing, not translated English
- Reference regional cultural touchpoints where relevant
- Match the brand's tone but adapted for this market
- Include appropriate script ({target_language.display_name} script, not romanized)

Respond in JSON:
{{
  "language": "{target_language.value}",
  "language_name": "{target_language.display_name}",
  "creative_concepts": [
    {{
      "concept_name": "short concept title",
      "hook_type": "emotional/urgency/social_proof/value/curiosity",
      "recommended_format": "reels/carousel/static/story",
      "headline_variants": [
        "{target_language.display_name} headline 1",
        "{target_language.display_name} headline 2",
        "{target_language.display_name} headline 3"
      ],
      "body_copy_variants": [
        "{target_language.display_name} body copy 1",
        "{target_language.display_name} body copy 2"
      ],
      "cta_options": [
        "{target_language.display_name} CTA 1",
        "{target_language.display_name} CTA 2"
      ],
      "visual_direction": "description of visual style, colors, imagery",
      "cultural_reference": "what cultural touchpoint this leverages",
      "predicted_ctr_range": "X-Y%",
      "a_b_test_suggestion": "what to test between variants"
    }}
  ],
  "cultural_sensitivity_flags": ["anything to watch out for in this market"],
  "dialect_recommendation": "formal vs colloquial recommendation and why",
  "best_posting_times": "optimal times for {target_language.region}"
}}"""


# ── CHAIN 5: CREATOR MATCHING ─────────────────────────────────────────

def build_creator_matching_prompt(
    request: CampaignRequest,
    brand_analysis: dict,
    market_intelligence: dict,
    creative_briefs: list[dict]
) -> str:
    """Recommend regional creators for the campaign."""

    languages_str = ", ".join(l.display_name for l in request.target_languages)
    products_str = ", ".join(p.name + " (" + p.category + ")" for p in request.products)
    niches_needed = set()
    for p in request.products:
        niches_needed.add(p.category)

    return f"""Recommend ideal regional creator profiles for this campaign.

BRAND: {request.company_name}
BRAND PERSONALITY: {str(brand_analysis.get('brand_profile', {}).get('brand_personality', ''))}
TARGET LANGUAGES: {languages_str}
PRODUCTS: {products_str}
PRODUCT NICHES: {', '.join(niches_needed)}
MONTHLY BUDGET FOR CREATORS: ~10% of ₹{request.monthly_budget:,.0f} = ₹{request.monthly_budget * 0.1:,.0f}

CREATIVE BRIEFS SUMMARY:
{str([b.get('language_name', '') + ': ' + str([c.get('concept_name', '') for c in b.get('creative_concepts', [])]) for b in creative_briefs])}

MATCHING CRITERIA (weighted):
- Language-market fit: 30% (creator's primary language matches target market)
- Niche relevance: 25% (content topics align with product category)
- Engagement quality: 20% (engagement rate, comment quality, not just followers)
- Brand safety: 15% (content tone aligns with brand, no controversy)
- Cost efficiency: 10% (estimated CPE within budget)

For each target language, recommend 2-3 ideal creator profiles.
Note: these are PROFILE RECOMMENDATIONS — specify the ideal creator 
attributes for the brand to search for.

Respond in JSON:
{{
  "creator_recommendations": [
    {{
      "language": "language_code",
      "language_name": "...",
      "creator_profiles": [
        {{
          "profile_type": "micro/mid/macro",
          "ideal_follower_range": "50K-200K",
          "niche": "specific content niche",
          "platform": "Instagram/YouTube/ShareChat/Moj",
          "content_style": "description of ideal content style",
          "engagement_benchmark": "minimum engagement rate",
          "estimated_cost_per_reel": "₹X-Y",
          "match_score": 92,
          "why_this_profile": "reasoning for this match",
          "brief_direction": "what the creator content should focus on",
          "content_format": "15s reel / 30s reel / carousel collab / story takeover",
          "brand_safety_requirements": ["requirement1"]
        }}
      ]
    }}
  ],
  "creator_strategy_notes": {{
    "portfolio_approach": "how creators across languages work together",
    "content_calendar_suggestion": "when to schedule creator posts",
    "measurement_kpis": ["kpi1", "kpi2"],
    "budget_distribution": "how to split creator budget across languages"
  }}
}}"""


# ── CHAIN 6: SYNTHESIS (final strategy assembly) ─────────────────────

def build_synthesis_prompt(
    request: CampaignRequest,
    brand_analysis: dict,
    market_intelligence: dict,
    budget_allocation: dict,
    creative_briefs: list[dict],
    creator_recommendations: dict,
    is_free_tier: bool = False
) -> str:
    """Assemble all chain outputs into a coherent strategy."""

    if is_free_tier:
        return f"""Synthesize the analysis into a FREE TIER strategy report.

FREE TIER RULES:
- Show enough intelligence to prove the model understands their business
- Include 3-5 teaser insights that hint at the full strategy
- DO NOT include: specific budget numbers, creative copy, creator recommendations, 
  or detailed channel splits
- End with a compelling upsell: show projected ROI if they upgrade

BRAND: {request.company_name}
MARKET INTELLIGENCE SUMMARY: {str(market_intelligence.get('cross_market_insights', {}))}
BUDGET: ₹{request.monthly_budget:,.0f}/month
PREDICTED METRICS (from budget optimization): {str(budget_allocation.get('scenarios', {}).get('moderate', {}))}

Respond in JSON:
{{
  "executive_summary": "2-3 paragraphs showing deep understanding of their business",
  "teaser_insights": [
    "Insight 1: specific data-driven observation (e.g., 'Your Tamil Nadu audience shows 3.2x higher purchase intent during Pongal')",
    "Insight 2: ...",
    "Insight 3: ..."
  ],
  "high_level_recommendations": [
    "General recommendation without specific numbers",
    "..."
  ],
  "upgrade_pitch": {{
    "what_full_strategy_includes": ["item1", "item2"],
    "projected_roi_improvement": "X-Y% improvement in ROAS",
    "projected_cac_reduction": "X% lower CAC"
  }},
  "confidence_score": 75
}}"""

    return f"""Synthesize all analysis into a comprehensive marketing strategy document.

INPUTS:
- Brand Analysis: {str(brand_analysis)}
- Market Intelligence: {str(market_intelligence)}
- Budget Allocation: {str(budget_allocation)}
- Creative Briefs: {len(creative_briefs)} languages covered
- Creator Recommendations: {str(creator_recommendations.get('creator_strategy_notes', {}))}

CAMPAIGN: {request.company_name}
SCOPE: {request.scope.value}
BUDGET: ₹{request.monthly_budget:,.0f}/month
DURATION: {request.campaign_duration_days} days
GOAL: {request.campaign_goal}

Respond in JSON:
{{
  "executive_summary": "3-4 paragraph strategy overview written for a founder/CMO",
  "market_analysis": "summary of regional market opportunities",
  "confidence_score": 85,
  "key_recommendations": [
    {{
      "priority": "1/2/3",
      "recommendation": "specific actionable recommendation",
      "expected_impact": "what this will achieve",
      "timeline": "when to execute"
    }}
  ],
  "predicted_outcomes": {{
    "predicted_cac": 0,
    "predicted_roas": 0,
    "predicted_conversions": 0,
    "predicted_reach": 0,
    "confidence_interval": "±X%"
  }},
  "risk_factors": [
    {{
      "risk": "description",
      "mitigation": "how to handle it",
      "likelihood": "low/medium/high"
    }}
  ],
  "30_60_90_plan": {{
    "first_30_days": "what to execute immediately",
    "days_31_60": "optimizations and scaling",
    "days_61_90": "expansion and iteration"
  }},
  "measurement_framework": {{
    "primary_kpis": ["kpi1", "kpi2"],
    "secondary_kpis": ["kpi3"],
    "review_cadence": "weekly/bi-weekly",
    "success_criteria": "what constitutes a successful campaign"
  }}
}}"""
