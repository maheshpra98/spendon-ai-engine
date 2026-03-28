"""
Spendon AI Engine — Strategy Engine
Orchestrates the multi-step prompt chain to generate marketing strategies.

Flow:
  CampaignRequest → Brand Analysis → Market Intel → Budget Opt → 
  Creative Strategy (per language) → Creator Matching → Synthesis → MarketingStrategy
"""

import json
import uuid
import asyncio
from typing import Optional

from core.models import (
    CampaignRequest, MarketingStrategy, BudgetAllocation,
    CreativeBrief, CreatorMatch, ProductScope, PlanTier, Language
)
from prompts.chains import (
    SYSTEM_PROMPT,
    build_brand_analysis_prompt,
    build_market_intelligence_prompt,
    build_budget_optimization_prompt,
    build_creative_strategy_prompt,
    build_creator_matching_prompt,
    build_synthesis_prompt
)


class AIClient:
    """Wrapper for the AI API (Claude / OpenAI compatible)."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key
        self.model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError("Install anthropic: pip install anthropic")
        return self._client

    async def generate(self, prompt: str, max_tokens: int = 4096) -> dict:
        """Send prompt to AI and parse JSON response."""
        client = self._get_client()

        # Run sync client in thread pool for async compatibility
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
        )

        # Extract text content
        text = ""
        for block in response.content:
            if block.type == "text":
                text += block.text

        # Parse JSON from response (handle markdown code blocks)
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Try to find JSON object in the text
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
            raise ValueError(f"Could not parse JSON from AI response: {text[:200]}...")


class StrategyEngine:
    """
    Main orchestrator for the multi-step strategy generation pipeline.

    Usage:
        engine = StrategyEngine(api_key="sk-...")
        strategy = await engine.generate(campaign_request)
    """

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.ai = AIClient(api_key=api_key, model=model)

    async def generate(
        self,
        request: CampaignRequest,
        on_step: Optional[callable] = None
    ) -> MarketingStrategy:
        """
        Run the full strategy generation pipeline.

        Args:
            request: Complete campaign request with all available data
            on_step: Optional callback(step_name, step_number, total_steps)
                     for progress tracking

        Returns:
            MarketingStrategy with all components filled
        """

        is_free = request.tier == PlanTier.FREE
        total_steps = 6 if not is_free else 4  # free skips creatives + creators detail

        def notify(step_name: str, step_num: int):
            if on_step:
                on_step(step_name, step_num, total_steps)

        # ── Step 1: Brand Analysis ────────────────────────────────
        notify("Analyzing brand DNA", 1)
        brand_prompt = build_brand_analysis_prompt(request)
        brand_analysis = await self.ai.generate(brand_prompt)

        # ── Step 2: Market Intelligence ───────────────────────────
        notify("Analyzing regional markets", 2)
        market_prompt = build_market_intelligence_prompt(request, brand_analysis)
        market_intelligence = await self.ai.generate(market_prompt, max_tokens=6000)

        # ── Step 3: Budget Optimization ───────────────────────────
        notify("Optimizing budget allocation", 3)
        budget_prompt = build_budget_optimization_prompt(
            request, brand_analysis, market_intelligence
        )
        budget_data = await self.ai.generate(budget_prompt, max_tokens=4096)

        if is_free:
            # ── Free tier: generate teaser synthesis only ─────────
            notify("Generating insights", 4)
            synthesis_prompt = build_synthesis_prompt(
                request, brand_analysis, market_intelligence,
                budget_data, [], {}, is_free_tier=True
            )
            synthesis = await self.ai.generate(synthesis_prompt)
            return self._build_free_strategy(request, synthesis, market_intelligence)

        # ── Step 4: Creative Strategy (per language) ──────────────
        notify("Generating regional creatives", 4)
        creative_briefs = []
        # Run language creative generation concurrently
        creative_tasks = []
        for lang in request.target_languages:
            creative_prompt = build_creative_strategy_prompt(
                request, brand_analysis, market_intelligence,
                budget_data, lang
            )
            creative_tasks.append(self.ai.generate(creative_prompt, max_tokens=4096))

        creative_results = await asyncio.gather(*creative_tasks, return_exceptions=True)
        for result in creative_results:
            if isinstance(result, dict):
                creative_briefs.append(result)

        # ── Step 5: Creator Matching ──────────────────────────────
        notify("Matching regional creators", 5)
        creator_prompt = build_creator_matching_prompt(
            request, brand_analysis, market_intelligence, creative_briefs
        )
        creator_data = await self.ai.generate(creator_prompt, max_tokens=4096)

        # ── Step 6: Synthesis ─────────────────────────────────────
        notify("Assembling final strategy", 6)
        synthesis_prompt = build_synthesis_prompt(
            request, brand_analysis, market_intelligence,
            budget_data, creative_briefs, creator_data,
            is_free_tier=False
        )
        synthesis = await self.ai.generate(synthesis_prompt, max_tokens=6000)

        # ── Build final MarketingStrategy object ──────────────────
        return self._build_full_strategy(
            request, synthesis, brand_analysis, market_intelligence,
            budget_data, creative_briefs, creator_data
        )

    def _build_free_strategy(
        self, request: CampaignRequest,
        synthesis: dict, market_intel: dict
    ) -> MarketingStrategy:
        """Build a free-tier strategy (teasers only)."""
        return MarketingStrategy(
            strategy_id=str(uuid.uuid4())[:8],
            company_name=request.company_name,
            scope=request.scope,
            confidence_score=synthesis.get("confidence_score", 70),
            executive_summary=synthesis.get("executive_summary", ""),
            teaser_insights=synthesis.get("teaser_insights", []),
            is_full_strategy=False,
            predicted_cac=0,
            predicted_roas=0,
        )

    def _build_full_strategy(
        self, request: CampaignRequest,
        synthesis: dict, brand: dict, market: dict,
        budget: dict, creatives: list, creators: dict
    ) -> MarketingStrategy:
        """Build the complete paid-tier strategy."""

        # Parse budget allocation
        ba = budget.get("budget_allocation", {})
        budget_alloc = BudgetAllocation(
            total_budget=request.monthly_budget,
            channel_split={k: v.get("percentage", 0) for k, v in ba.get("channel_split", {}).items()},
            regional_split={k: v.get("percentage", 0) for k, v in ba.get("regional_split", {}).items()},
            product_split={k: v.get("percentage", 0) for k, v in ba.get("product_split", {}).items()},
            scenarios=budget.get("scenarios", {})
        )

        # Parse creative briefs
        creative_brief_objects = []
        for cb in creatives:
            lang_code = cb.get("language", "")
            try:
                lang = Language(lang_code)
            except ValueError:
                continue
            for concept in cb.get("creative_concepts", []):
                creative_brief_objects.append(CreativeBrief(
                    language=lang,
                    headline_variants=concept.get("headline_variants", []),
                    body_copy_variants=concept.get("body_copy_variants", []),
                    cta_options=concept.get("cta_options", []),
                    recommended_format=concept.get("recommended_format", ""),
                    hook_type=concept.get("hook_type", ""),
                    visual_direction=concept.get("visual_direction", ""),
                    cultural_notes=concept.get("cultural_reference", ""),
                ))

        # Parse creator recommendations
        creator_matches = []
        for lang_group in creators.get("creator_recommendations", []):
            lang_code = lang_group.get("language", "")
            try:
                lang = Language(lang_code)
            except ValueError:
                continue
            for profile in lang_group.get("creator_profiles", []):
                creator_matches.append(CreatorMatch(
                    name=profile.get("profile_type", "Unknown") + " " + profile.get("niche", ""),
                    platform=profile.get("platform", "Instagram"),
                    language=lang,
                    niche=profile.get("niche", ""),
                    followers=0,
                    engagement_rate=0,
                    match_score=profile.get("match_score", 0),
                    estimated_cost=0,
                    brief_suggestion=profile.get("brief_direction", "")
                ))

        # Parse predictions
        predictions = synthesis.get("predicted_outcomes", {})
        moderate = budget.get("scenarios", {}).get("moderate", {})

        return MarketingStrategy(
            strategy_id=str(uuid.uuid4())[:8],
            company_name=request.company_name,
            scope=request.scope,
            confidence_score=synthesis.get("confidence_score", 80),
            executive_summary=synthesis.get("executive_summary", ""),
            market_analysis=synthesis.get("market_analysis", ""),
            budget_allocation=budget_alloc,
            channel_recommendations=synthesis.get("key_recommendations", []),
            timing_recommendations=synthesis.get("30_60_90_plan", {}),
            creative_briefs=creative_brief_objects,
            creator_matches=creator_matches,
            predicted_cac=predictions.get("predicted_cac", moderate.get("predicted_cac", 0)),
            predicted_roas=predictions.get("predicted_roas", moderate.get("predicted_roas", 0)),
            predicted_conversions=predictions.get("predicted_conversions", moderate.get("predicted_conversions", 0)),
            is_full_strategy=True,
        )
