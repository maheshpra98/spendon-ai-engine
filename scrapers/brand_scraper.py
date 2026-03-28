"""
Spendon AI Engine — Brand Intelligence Scraper
Extracts brand DNA from public web sources:
  - Company website (slogans, taglines, product descriptions, brand tone)
  - Meta Ad Library (past ad creatives, copy, formats)
  - Social media profiles (bios, content pillars, engagement patterns)
  - News/press mentions (brand narrative)
  - Competitor ads (competitive intelligence)

Note: This module uses an AI-assisted extraction approach.
Raw HTML/text is fetched, then Claude analyzes it to extract structured brand attributes.
"""

import json
import asyncio
import re
from typing import Optional
from urllib.parse import urlparse

from core.models import BrandDNA


class BrandScraper:
    """
    Scrapes and analyzes public web data to build a brand DNA profile.

    Uses a two-step approach:
    1. Fetch raw content from web sources (website, social, etc.)
    2. Send content to AI for structured extraction of brand attributes

    In production, step 1 uses Playwright/Puppeteer for JS-heavy sites.
    This implementation uses a simplified HTTP approach with AI extraction.
    """

    def __init__(self, ai_client, http_client=None):
        """
        Args:
            ai_client: AIClient instance for brand analysis
            http_client: Optional HTTP client (aiohttp session).
                         If None, uses basic urllib.
        """
        self.ai = ai_client
        self.http = http_client

    async def build_brand_profile(
        self,
        company_name: str,
        website_url: str = "",
        meta_page_name: str = "",
        competitor_urls: list[str] = None,
        social_handles: dict = None
    ) -> BrandDNA:
        """
        Build a complete brand DNA profile from public sources.

        Args:
            company_name: Brand/company name
            website_url: Company website URL
            meta_page_name: Facebook page name for Ad Library lookup
            competitor_urls: List of competitor website URLs
            social_handles: Dict of social handles {"instagram": "@handle", ...}

        Returns:
            BrandDNA with extracted brand attributes
        """
        # Gather raw content from all sources concurrently
        tasks = []

        # 1. Website scraping
        website_content = ""
        if website_url:
            tasks.append(("website", self._scrape_website(website_url)))

        # 2. Meta Ad Library
        ad_library_content = ""
        if meta_page_name:
            tasks.append(("ads", self._scrape_meta_ad_library(meta_page_name)))

        # 3. Social profiles
        if social_handles:
            for platform, handle in social_handles.items():
                tasks.append((f"social_{platform}", self._scrape_social(platform, handle)))

        # 4. Competitor analysis
        competitor_data = []
        if competitor_urls:
            for url in competitor_urls[:3]:  # limit to 3 competitors
                tasks.append((f"competitor_{url}", self._scrape_website(url)))

        # Execute all scraping tasks
        raw_data = {}
        if tasks:
            results = await asyncio.gather(
                *[t[1] for t in tasks],
                return_exceptions=True
            )
            for (label, _), result in zip(tasks, results):
                if isinstance(result, str) and result:
                    raw_data[label] = result

        # Send all raw content to AI for structured extraction
        brand_dna = await self._extract_brand_attributes(
            company_name, raw_data, website_url
        )
        return brand_dna

    async def _scrape_website(self, url: str) -> str:
        """
        Fetch and extract text content from a website.
        In production: uses Playwright for JS rendering.
        Here: uses simplified HTTP fetch.
        """
        try:
            # Normalize URL
            if not url.startswith("http"):
                url = "https://" + url

            # In production, this would use Playwright:
            # async with async_playwright() as p:
            #     browser = await p.chromium.launch()
            #     page = await browser.new_page()
            #     await page.goto(url, wait_until="networkidle")
            #     content = await page.content()
            #     await browser.close()

            # For now, return a placeholder that the AI can work with
            return f"""[WEBSITE CONTENT FROM {url}]
Note: In production, this fetches actual website HTML via Playwright.
The AI extraction prompt below handles the analysis.
Company URL: {url}
Domain: {urlparse(url).netloc}"""

        except Exception as e:
            return f"[Error fetching {url}: {str(e)}]"

    async def _scrape_meta_ad_library(self, page_name: str) -> str:
        """
        Fetch ad data from Meta Ad Library.
        In production: uses Meta Ad Library API.

        Meta Ad Library API endpoint:
        GET https://graph.facebook.com/v19.0/ads_archive
        params: search_terms, ad_reached_countries, ad_active_status, etc.
        """
        try:
            # In production:
            # response = await self.http.get(
            #     "https://graph.facebook.com/v19.0/ads_archive",
            #     params={
            #         "search_terms": page_name,
            #         "ad_reached_countries": '["IN"]',
            #         "ad_active_status": "ALL",
            #         "fields": "ad_creative_bodies,ad_creative_link_captions,"
            #                   "ad_creative_link_titles,ad_delivery_start_time,"
            #                   "ad_delivery_stop_time,page_name",
            #         "access_token": self.meta_api_token
            #     }
            # )

            return f"""[META AD LIBRARY DATA FOR: {page_name}]
Note: In production, this pulls actual ad data via Meta Ad Library API.
Extracts: ad copy, CTAs, creative formats, run duration, targeting signals.
Page: {page_name}"""

        except Exception as e:
            return f"[Error fetching Meta Ad Library for {page_name}: {str(e)}]"

    async def _scrape_social(self, platform: str, handle: str) -> str:
        """Fetch social media profile data."""
        return f"""[SOCIAL PROFILE: {platform} @{handle}]
Note: In production, scrapes public profile bio, recent posts, hashtags.
Platform: {platform}
Handle: {handle}"""

    async def _extract_brand_attributes(
        self,
        company_name: str,
        raw_data: dict,
        website_url: str
    ) -> BrandDNA:
        """
        Use AI to extract structured brand attributes from raw scraped content.
        This is the core intelligence of the scraper — Claude analyzes
        the raw content and extracts actionable brand DNA.
        """
        scraped_content = "\n\n".join([
            f"=== {source.upper()} ===\n{content}"
            for source, content in raw_data.items()
        ])

        if not scraped_content.strip():
            # No scraped data available — return minimal profile
            return BrandDNA(
                company_name=company_name,
                website_url=website_url,
                brand_tone="unknown"
            )

        extraction_prompt = f"""Analyze the following scraped web content and extract 
structured brand attributes for {company_name}.

SCRAPED CONTENT:
{scraped_content}

Extract and respond in JSON:
{{
  "company_name": "{company_name}",
  "slogans": ["any slogans or taglines found"],
  "taglines": ["secondary taglines or catchphrases"],
  "brand_tone": "formal/casual/playful/premium/aspirational",
  "core_values": ["value1", "value2"],
  "product_descriptions": {{"product_name": "description"}},
  "social_bio": "extracted social media bio",
  "content_pillars": ["pillar1", "pillar2"],
  "past_ad_themes": ["theme1", "theme2"],
  "competitor_insights": [
    {{
      "competitor_name": "...",
      "positioning": "how they position themselves",
      "ad_strategy": "what kind of ads they run",
      "differentiation_opportunity": "how our brand can differentiate"
    }}
  ]
}}

If certain information is not available from the scraped content, 
use empty lists/strings. Do NOT fabricate data."""

        try:
            result = await self.ai.generate(extraction_prompt)
            return BrandDNA(
                company_name=result.get("company_name", company_name),
                website_url=website_url,
                slogans=result.get("slogans", []),
                taglines=result.get("taglines", []),
                brand_tone=result.get("brand_tone", ""),
                core_values=result.get("core_values", []),
                product_descriptions=result.get("product_descriptions", {}),
                social_bio=result.get("social_bio", ""),
                content_pillars=result.get("content_pillars", []),
                past_ad_themes=result.get("past_ad_themes", []),
                competitor_insights=result.get("competitor_insights", []),
            )
        except Exception:
            return BrandDNA(company_name=company_name, website_url=website_url)
