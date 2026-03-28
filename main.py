"""
Spendon AI Engine — Main Entry Point

Usage:
  # Start the API server
  python main.py serve

  # Generate a strategy directly (CLI mode)  
  python main.py generate --company "MyBrand" --budget 500000 --languages "Hindi,Tamil"

  # Test with sample data
  python main.py test
"""

import os
import sys
import json
import asyncio

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.models import (
    CampaignRequest, ProductScope, PlanTier, Language,
    ProductInfo, BrandDNA
)
from core.engine import StrategyEngine


async def run_test_strategy():
    """Generate a sample strategy to test the pipeline."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("ERROR: Set ANTHROPIC_API_KEY environment variable")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        return

    # Build a sample request
    request = CampaignRequest(
        company_name="FreshBasket",
        scope=ProductScope.SINGLE,
        products=[
            ProductInfo(
                name="Cold-Pressed Juice Combo",
                category="Health & Wellness",
                price=599,
                description="Pack of 6 cold-pressed juices - Orange, ABC, Green Detox",
                usps=["100% natural", "No preservatives", "Farm to bottle in 24hrs"],
                target_audience="Health-conscious urban women, 25-40"
            )
        ],
        monthly_budget=300000,  # ₹3 lakhs
        target_cac=200,
        campaign_goal="Launch cold-pressed juice combo in South India with focus on health-conscious women in Tier 1-2 cities",
        campaign_duration_days=30,
        target_languages=[Language.TAMIL, Language.KANNADA],
        tier=PlanTier.GROWTH,
        brand_dna=BrandDNA(
            company_name="FreshBasket",
            website_url="https://freshbasket.in",
            slogans=["Farm Fresh, Always Fresh", "Nature's Best, Delivered"],
            brand_tone="premium-casual",
            core_values=["health", "freshness", "sustainability"],
        )
    )

    print("=" * 60)
    print("SPENDON AI ENGINE — Test Strategy Generation")
    print("=" * 60)
    print(f"Company: {request.company_name}")
    print(f"Product: {request.products[0].name}")
    print(f"Budget: ₹{request.monthly_budget:,.0f}/month")
    print(f"Languages: {', '.join(l.display_name for l in request.target_languages)}")
    print(f"Scope: {request.scope.value}")
    print(f"Tier: {request.tier.value}")
    print("=" * 60)

    def on_step(name, num, total):
        print(f"\n[{num}/{total}] {name}...")

    engine = StrategyEngine(api_key=api_key)
    strategy = await engine.generate(request, on_step=on_step)

    print("\n" + "=" * 60)
    print("STRATEGY GENERATED SUCCESSFULLY")
    print("=" * 60)
    print(f"Strategy ID: {strategy.strategy_id}")
    print(f"Confidence: {strategy.confidence_score}/100")
    print(f"Predicted CAC: ₹{strategy.predicted_cac:.0f}")
    print(f"Predicted ROAS: {strategy.predicted_roas:.1f}x")
    print(f"\nExecutive Summary:\n{strategy.executive_summary}")

    if strategy.creative_briefs:
        print(f"\nCreative Briefs: {len(strategy.creative_briefs)} generated")
        for cb in strategy.creative_briefs[:2]:
            print(f"  [{cb.language.display_name}] {cb.recommended_format} — {cb.hook_type}")
            if cb.headline_variants:
                print(f"    Headline: {cb.headline_variants[0]}")

    if strategy.creator_matches:
        print(f"\nCreator Matches: {len(strategy.creator_matches)} profiles")
        for cm in strategy.creator_matches[:3]:
            print(f"  [{cm.language.display_name}] {cm.name} — Score: {cm.match_score}")

    if strategy.budget_allocation:
        print(f"\nBudget Allocation:")
        for ch, pct in strategy.budget_allocation.channel_split.items():
            print(f"  {ch}: {pct}%")

    return strategy


def run_server():
    """Start the FastAPI server."""
    import uvicorn
    print("Starting Spendon AI Engine API...")
    print("Docs: http://localhost:8000/docs")
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "serve":
            run_server()
        elif cmd == "test":
            asyncio.run(run_test_strategy())
        else:
            print(f"Unknown command: {cmd}")
            print("Usage: python main.py [serve|test]")
    else:
        print("Spendon AI Engine v2.0")
        print("Usage:")
        print("  python main.py serve  — Start API server")
        print("  python main.py test   — Run test strategy generation")
