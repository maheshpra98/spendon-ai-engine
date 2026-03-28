"""
Spendon AI Engine — Data Processors
Handles ingestion and normalization of different data inputs:
  - CSV/Excel uploads (sales, campaigns)
  - Meta Ads API data
  - Manual form inputs
"""

import csv
import io
import json
from typing import Optional
from core.models import SalesData, MetaAdsData, ProductInfo, CampaignRequest, ProductScope, Language, PlanTier


class CSVProcessor:
    """Process uploaded CSV/Excel files into structured data."""

    SALES_COLUMNS = {
        "product", "sku", "revenue", "units", "region", "state",
        "city", "date", "month", "category", "price"
    }
    CAMPAIGN_COLUMNS = {
        "campaign", "spend", "impressions", "clicks", "conversions",
        "ctr", "cpc", "cpm", "roas", "cac", "channel", "region"
    }

    @staticmethod
    def detect_type(headers: list[str]) -> str:
        """Detect if CSV is sales data or campaign data."""
        normalized = {h.lower().strip().replace(" ", "_") for h in headers}
        sales_match = len(normalized & CSVProcessor.SALES_COLUMNS)
        campaign_match = len(normalized & CSVProcessor.CAMPAIGN_COLUMNS)
        return "sales" if sales_match >= campaign_match else "campaign"

    @staticmethod
    def process_sales_csv(content: str) -> SalesData:
        """Parse sales CSV into SalesData."""
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)
        if not rows:
            return SalesData(total_revenue=0, period_months=0)

        headers = {h.lower().strip().replace(" ", "_") for h in rows[0].keys()}

        # Find revenue column
        rev_col = None
        for col in rows[0].keys():
            if col.lower().strip().replace(" ", "_") in {"revenue", "sales", "amount", "total"}:
                rev_col = col
                break

        total_revenue = 0
        product_revenues = {}
        regional_revenues = {}

        for row in rows:
            # Revenue
            if rev_col and row.get(rev_col):
                try:
                    rev = float(str(row[rev_col]).replace(",", "").replace("₹", ""))
                    total_revenue += rev
                except ValueError:
                    pass

            # Product breakdown
            for pcol in ["product", "sku", "item", "product_name"]:
                if pcol in {k.lower().strip().replace(" ", "_") for k in row.keys()}:
                    for k, v in row.items():
                        if k.lower().strip().replace(" ", "_") == pcol:
                            name = v
                            if name:
                                product_revenues[name] = product_revenues.get(name, 0) + (rev if rev_col else 0)
                            break

            # Regional breakdown
            for rcol in ["region", "state", "city"]:
                if rcol in {k.lower().strip().replace(" ", "_") for k in row.keys()}:
                    for k, v in row.items():
                        if k.lower().strip().replace(" ", "_") == rcol:
                            region = v
                            if region:
                                regional_revenues[region] = regional_revenues.get(region, 0) + (rev if rev_col else 0)
                            break

        # Sort top products
        top_products = sorted(
            [{"name": k, "revenue": v} for k, v in product_revenues.items()],
            key=lambda x: x["revenue"], reverse=True
        )[:10]

        return SalesData(
            total_revenue=total_revenue,
            period_months=max(1, len(rows) // 30),  # rough estimate
            top_products=top_products,
            regional_breakdown=regional_revenues,
            growth_trend="stable"  # would need time-series analysis for real detection
        )

    @staticmethod
    def process_campaign_csv(content: str) -> MetaAdsData:
        """Parse campaign CSV into MetaAdsData."""
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)
        if not rows:
            return MetaAdsData(
                total_spend=0, period_days=0, avg_cac=0,
                avg_cpm=0, avg_cpc=0, avg_ctr=0, avg_roas=0
            )

        total_spend = 0
        total_conversions = 0
        total_impressions = 0
        total_clicks = 0
        campaigns = []

        for row in rows:
            spend = 0
            conversions = 0
            impressions = 0
            clicks = 0

            for k, v in row.items():
                key = k.lower().strip().replace(" ", "_")
                try:
                    val = float(str(v).replace(",", "").replace("₹", "")) if v else 0
                except ValueError:
                    val = 0

                if key in {"spend", "cost", "ad_spend", "amount_spent"}:
                    spend = val
                    total_spend += val
                elif key in {"conversions", "purchases", "sales"}:
                    conversions = val
                    total_conversions += val
                elif key in {"impressions", "views"}:
                    impressions = val
                    total_impressions += val
                elif key in {"clicks", "link_clicks"}:
                    clicks = val
                    total_clicks += val

            campaign_name = ""
            for k in row.keys():
                if k.lower().strip().replace(" ", "_") in {"campaign", "campaign_name", "name"}:
                    campaign_name = row[k]
                    break

            if spend > 0:
                campaigns.append({
                    "name": campaign_name,
                    "spend": spend,
                    "conversions": conversions,
                    "roas": (conversions * 500) / spend if spend > 0 else 0  # assume ₹500 AOV
                })

        campaigns.sort(key=lambda x: x.get("roas", 0), reverse=True)

        avg_cac = total_spend / total_conversions if total_conversions > 0 else 0
        avg_cpm = (total_spend / total_impressions * 1000) if total_impressions > 0 else 0
        avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0

        return MetaAdsData(
            total_spend=total_spend,
            period_days=max(1, len(rows)),
            avg_cac=avg_cac,
            avg_cpm=avg_cpm,
            avg_cpc=avg_cpc,
            avg_ctr=avg_ctr,
            avg_roas=campaigns[0].get("roas", 0) if campaigns else 0,
            best_performing_campaigns=campaigns[:5],
        )


class ManualInputProcessor:
    """Process manual form inputs into CampaignRequest."""

    @staticmethod
    def build_request(
        company_name: str,
        monthly_budget: float,
        target_cac: Optional[float] = None,
        campaign_goal: str = "",
        scope: str = "single",
        products: list[dict] = None,
        target_languages: list[str] = None,
        campaign_duration_days: int = 30,
        tier: str = "free"
    ) -> CampaignRequest:
        """Build a CampaignRequest from manual form data."""

        # Parse products
        product_list = []
        if products:
            for p in products:
                product_list.append(ProductInfo(
                    name=p.get("name", "Product"),
                    category=p.get("category", "General"),
                    price=float(p.get("price", 0)),
                    description=p.get("description", ""),
                    usps=p.get("usps", []),
                    target_audience=p.get("target_audience", "")
                ))

        # Parse languages
        lang_list = []
        if target_languages:
            lang_map = {l.value: l for l in Language}
            name_map = {l.display_name.lower(): l for l in Language}
            for lang_str in target_languages:
                lang_lower = lang_str.lower().strip()
                if lang_lower in lang_map:
                    lang_list.append(lang_map[lang_lower])
                elif lang_lower in name_map:
                    lang_list.append(name_map[lang_lower])

        # Parse scope
        scope_map = {"single": ProductScope.SINGLE, "top": ProductScope.TOP_PRODUCTS, "catalog": ProductScope.FULL_CATALOG}
        product_scope = scope_map.get(scope.lower(), ProductScope.SINGLE)

        # Parse tier
        tier_map = {"free": PlanTier.FREE, "growth": PlanTier.GROWTH, "pro": PlanTier.PRO, "enterprise": PlanTier.ENTERPRISE}
        plan_tier = tier_map.get(tier.lower(), PlanTier.FREE)

        return CampaignRequest(
            company_name=company_name,
            scope=product_scope,
            products=product_list,
            monthly_budget=monthly_budget,
            target_cac=target_cac,
            campaign_goal=campaign_goal,
            campaign_duration_days=campaign_duration_days,
            target_languages=lang_list if lang_list else [Language.HINDI],
            tier=plan_tier,
        )
