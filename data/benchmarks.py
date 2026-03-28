"""
Spendon AI Engine — Indian Market Benchmarks v1.0
Real-world digital marketing benchmarks for Indian markets.

Sources: Meta Business Suite aggregates, industry reports (Dentsu, GroupM India),
         influencer platforms, and publicly available campaign data.

Last updated: March 2026
Note: These are baseline benchmarks. Actual performance varies by creative quality,
      targeting precision, and market conditions. Update quarterly.
"""


# ═══════ META ADS BENCHMARKS BY INDUSTRY ═══════

META_ADS_BENCHMARKS = {
    "health_wellness": {
        "industry": "Health & Wellness",
        "keywords": ["health", "wellness", "fitness", "supplement", "organic", "ayurvedic", "yoga", "nutrition", "juice", "protein", "diet"],
        "cpm": {"reels": 85, "feed": 120, "stories": 95, "carousel": 110},
        "cpc": {"min": 8, "max": 25, "avg": 14},
        "ctr": {"reels": 2.8, "feed": 1.6, "stories": 2.1, "carousel": 1.9, "avg": 2.1},
        "conversion_rate": {"cold": 1.8, "warm": 4.2, "retarget": 8.5, "avg": 3.1},
        "avg_roas": 4.2,
        "roas_range": {"low": 2.5, "mid": 4.2, "high": 7.0},
        "best_format": "reels",
        "best_format_reason": "62% lower cost per result vs feed posts. Health content performs best as short-form video demos.",
        "avg_order_value": 800,
        "typical_cac_range": {"low": 150, "mid": 250, "high": 450},
        "audience_notes": "Women 25-40 highest conversion. Interest targeting: yoga, organic food, Ayurveda. Lookalike audiences from purchasers outperform interest targeting by 35%.",
    },
    "fashion_apparel": {
        "industry": "Fashion & Apparel",
        "keywords": ["fashion", "clothing", "apparel", "wear", "textile", "saree", "kurta", "ethnic", "western", "accessories", "jewelry", "jewellery"],
        "cpm": {"reels": 65, "feed": 110, "stories": 80, "carousel": 90},
        "cpc": {"min": 5, "max": 18, "avg": 10},
        "ctr": {"reels": 3.2, "feed": 2.0, "stories": 2.5, "carousel": 2.8, "avg": 2.6},
        "conversion_rate": {"cold": 2.2, "warm": 5.5, "retarget": 11.0, "avg": 4.1},
        "avg_roas": 5.5,
        "roas_range": {"low": 3.0, "mid": 5.5, "high": 9.0},
        "best_format": "carousel",
        "best_format_reason": "38% higher conversion rate. Shoppers want to see multiple angles/options before buying.",
        "avg_order_value": 1200,
        "typical_cac_range": {"low": 100, "mid": 200, "high": 350},
        "audience_notes": "Women 18-35 dominate. Ethnic wear peaks during festival months. Regional fashion preferences vary significantly — saree styles differ by state.",
    },
    "food_beverage": {
        "industry": "Food & Beverage",
        "keywords": ["food", "beverage", "snack", "restaurant", "cafe", "delivery", "grocery", "spice", "masala", "tea", "coffee", "sweet", "bakery"],
        "cpm": {"reels": 55, "feed": 95, "stories": 70, "carousel": 85},
        "cpc": {"min": 4, "max": 15, "avg": 8},
        "ctr": {"reels": 3.5, "feed": 2.2, "stories": 2.8, "carousel": 2.0, "avg": 2.6},
        "conversion_rate": {"cold": 2.5, "warm": 6.0, "retarget": 12.0, "avg": 4.5},
        "avg_roas": 5.0,
        "roas_range": {"low": 3.5, "mid": 5.0, "high": 8.5},
        "best_format": "reels",
        "best_format_reason": "Food content is inherently visual. Recipe/preparation reels get 3x more shares than static food images.",
        "avg_order_value": 500,
        "typical_cac_range": {"low": 60, "mid": 120, "high": 250},
        "audience_notes": "Broadest demographic appeal. Regional taste preferences are extreme — what works in Punjab won't work in Kerala. Always localize.",
    },
    "beauty_cosmetics": {
        "industry": "Beauty & Cosmetics",
        "keywords": ["beauty", "cosmetic", "skincare", "makeup", "haircare", "personal care", "grooming", "derma"],
        "cpm": {"reels": 75, "feed": 115, "stories": 88, "carousel": 100},
        "cpc": {"min": 6, "max": 22, "avg": 12},
        "ctr": {"reels": 3.0, "feed": 1.8, "stories": 2.4, "carousel": 2.2, "avg": 2.4},
        "conversion_rate": {"cold": 2.0, "warm": 5.0, "retarget": 10.0, "avg": 3.8},
        "avg_roas": 4.8,
        "roas_range": {"low": 2.8, "mid": 4.8, "high": 8.0},
        "best_format": "reels",
        "best_format_reason": "Tutorial-style reels drive highest engagement. Before/after content converts 45% better than product shots.",
        "avg_order_value": 650,
        "typical_cac_range": {"low": 80, "mid": 180, "high": 320},
        "audience_notes": "Women 18-35 primary. Men's grooming growing 40% YoY. Influencer content outperforms branded content by 2.5x in this category.",
    },
    "education_edtech": {
        "industry": "Education & EdTech",
        "keywords": ["education", "edtech", "course", "learning", "tuition", "coaching", "exam", "skill", "certification", "training"],
        "cpm": {"reels": 95, "feed": 140, "stories": 110, "carousel": 125},
        "cpc": {"min": 12, "max": 40, "avg": 22},
        "ctr": {"reels": 2.2, "feed": 1.4, "stories": 1.8, "carousel": 1.6, "avg": 1.8},
        "conversion_rate": {"cold": 1.2, "warm": 3.5, "retarget": 7.0, "avg": 2.4},
        "avg_roas": 3.5,
        "roas_range": {"low": 2.0, "mid": 3.5, "high": 6.0},
        "best_format": "reels",
        "best_format_reason": "Short explainer/teaser reels drive sign-ups. Success stories and testimonials in regional languages convert 3x better than English.",
        "avg_order_value": 5000,
        "typical_cac_range": {"low": 300, "mid": 600, "high": 1200},
        "audience_notes": "Parents 28-45 for K-12. Students 18-25 for competitive exams. Working professionals 22-35 for upskilling. Regional language courses growing 60% YoY.",
    },
    "electronics_tech": {
        "industry": "Electronics & Technology",
        "keywords": ["electronics", "tech", "gadget", "mobile", "phone", "laptop", "computer", "software", "app", "saas"],
        "cpm": {"reels": 90, "feed": 130, "stories": 100, "carousel": 115},
        "cpc": {"min": 10, "max": 35, "avg": 18},
        "ctr": {"reels": 2.5, "feed": 1.5, "stories": 2.0, "carousel": 1.8, "avg": 2.0},
        "conversion_rate": {"cold": 1.5, "warm": 3.8, "retarget": 8.0, "avg": 2.8},
        "avg_roas": 3.8,
        "roas_range": {"low": 2.2, "mid": 3.8, "high": 6.5},
        "best_format": "reels",
        "best_format_reason": "Unboxing and feature demo reels. Comparison content drives highest intent.",
        "avg_order_value": 3000,
        "typical_cac_range": {"low": 200, "mid": 450, "high": 900},
        "audience_notes": "Men 18-35 primary. Feature-comparison content in regional languages underserved — big opportunity.",
    },
    "home_lifestyle": {
        "industry": "Home & Lifestyle",
        "keywords": ["home", "decor", "furniture", "kitchen", "appliance", "interior", "garden", "lifestyle", "living"],
        "cpm": {"reels": 70, "feed": 105, "stories": 82, "carousel": 95},
        "cpc": {"min": 7, "max": 20, "avg": 12},
        "ctr": {"reels": 2.6, "feed": 1.7, "stories": 2.2, "carousel": 2.4, "avg": 2.2},
        "conversion_rate": {"cold": 1.6, "warm": 4.0, "retarget": 9.0, "avg": 3.2},
        "avg_roas": 4.0,
        "roas_range": {"low": 2.5, "mid": 4.0, "high": 7.0},
        "best_format": "carousel",
        "best_format_reason": "Room makeover carousels and before/after content. Video tours of decorated spaces perform well as Reels.",
        "avg_order_value": 2500,
        "typical_cac_range": {"low": 180, "mid": 350, "high": 600},
        "audience_notes": "Women 25-45 primary. New homeowners and newlyweds are highest-intent audiences. Festival seasons (Diwali, Griha Pravesh) spike demand.",
    },
    "general": {
        "industry": "General / Other",
        "keywords": [],
        "cpm": {"reels": 80, "feed": 115, "stories": 90, "carousel": 105},
        "cpc": {"min": 8, "max": 25, "avg": 14},
        "ctr": {"reels": 2.5, "feed": 1.6, "stories": 2.0, "carousel": 1.9, "avg": 2.0},
        "conversion_rate": {"cold": 1.8, "warm": 4.0, "retarget": 8.5, "avg": 3.0},
        "avg_roas": 3.8,
        "roas_range": {"low": 2.0, "mid": 3.8, "high": 6.5},
        "best_format": "reels",
        "best_format_reason": "Reels have lowest CPM across all categories in India as of 2025-2026.",
        "avg_order_value": 1000,
        "typical_cac_range": {"low": 120, "mid": 250, "high": 500},
        "audience_notes": "Default benchmarks. Actual performance depends heavily on product-market fit and creative quality.",
    }
}


# ═══════ REGIONAL COST DATA (PER INDIAN STATE) ═══════

REGIONAL_DATA = {
    "hi": {
        "language": "Hindi",
        "states": ["Uttar Pradesh", "Madhya Pradesh", "Rajasthan", "Bihar", "Jharkhand", "Chhattisgarh", "Uttarakhand", "Himachal Pradesh", "Delhi", "Haryana"],
        "population_reach": 528000000,
        "digital_penetration": 48,
        "avg_cpm": 70,
        "cpm_by_city_tier": {"tier1": 120, "tier2": 75, "tier3": 40},
        "competition_level": "high",
        "top_platforms": ["Instagram", "YouTube", "Facebook", "ShareChat"],
        "content_preference": "Short-form video (Reels/Shorts), devotional content, family-oriented",
        "avg_engagement_rate": 3.8,
        "notes": "Largest market by reach. Highly competitive for national brands. Tier-2/3 cities offer best CPM value. Hindi belt has the widest demographic spread."
    },
    "ta": {
        "language": "Tamil",
        "states": ["Tamil Nadu", "Puducherry"],
        "population_reach": 77000000,
        "digital_penetration": 52,
        "avg_cpm": 75,
        "cpm_by_city_tier": {"tier1": 105, "tier2": 65, "tier3": 38},
        "competition_level": "medium",
        "top_platforms": ["YouTube", "Instagram", "Facebook"],
        "content_preference": "Cinema-inspired content, humor, family values, food culture",
        "avg_engagement_rate": 4.2,
        "notes": "Strong regional brand loyalty. Tamil audiences respond best to culturally rooted content. Cinema references boost engagement 40%. Very high YouTube consumption."
    },
    "te": {
        "language": "Telugu",
        "states": ["Andhra Pradesh", "Telangana"],
        "population_reach": 83000000,
        "digital_penetration": 46,
        "avg_cpm": 65,
        "cpm_by_city_tier": {"tier1": 95, "tier2": 58, "tier3": 32},
        "competition_level": "medium-low",
        "top_platforms": ["YouTube", "Instagram", "ShareChat"],
        "content_preference": "Entertainment-driven, film culture, aspirational lifestyle",
        "avg_engagement_rate": 4.5,
        "notes": "Underserved market with low competition. Hyderabad is a key urban hub. Telugu audiences are highly responsive to influencer marketing. Best ROI potential among South Indian markets."
    },
    "kn": {
        "language": "Kannada",
        "states": ["Karnataka"],
        "population_reach": 44000000,
        "digital_penetration": 55,
        "avg_cpm": 80,
        "cpm_by_city_tier": {"tier1": 115, "tier2": 68, "tier3": 42},
        "competition_level": "medium-high",
        "top_platforms": ["Instagram", "YouTube", "Facebook"],
        "content_preference": "Tech-savvy audience, startup culture (Bangalore), traditional values in Tier-2/3",
        "avg_engagement_rate": 3.9,
        "notes": "Bangalore skews the data — very urban, tech-savvy, English-comfortable. But Tier-2/3 Karnataka is deeply Kannada-first. Two different strategies needed."
    },
    "ml": {
        "language": "Malayalam",
        "states": ["Kerala"],
        "population_reach": 35000000,
        "digital_penetration": 62,
        "avg_cpm": 90,
        "cpm_by_city_tier": {"tier1": 125, "tier2": 80, "tier3": 55},
        "competition_level": "medium",
        "top_platforms": ["YouTube", "Instagram", "WhatsApp"],
        "content_preference": "Intellectual content, socially conscious, humor, food/travel",
        "avg_engagement_rate": 4.8,
        "notes": "Highest digital penetration and literacy in India. Audience is discerning — low tolerance for hard-sell. Content must be intelligent and authentic. WhatsApp marketing is uniquely effective here."
    },
    "bn": {
        "language": "Bengali",
        "states": ["West Bengal", "Tripura"],
        "population_reach": 100000000,
        "digital_penetration": 42,
        "avg_cpm": 55,
        "cpm_by_city_tier": {"tier1": 90, "tier2": 50, "tier3": 28},
        "competition_level": "low-medium",
        "top_platforms": ["YouTube", "Facebook", "Instagram", "ShareChat"],
        "content_preference": "Cultural pride, literary/artistic content, food culture, Durga Puja",
        "avg_engagement_rate": 4.0,
        "notes": "Large market with relatively low ad competition = excellent CPM value. Bengali audiences have strong cultural identity. Durga Puja season (Oct) is the biggest marketing window."
    },
    "mr": {
        "language": "Marathi",
        "states": ["Maharashtra"],
        "population_reach": 83000000,
        "digital_penetration": 54,
        "avg_cpm": 85,
        "cpm_by_city_tier": {"tier1": 145, "tier2": 72, "tier3": 40},
        "competition_level": "high",
        "top_platforms": ["Instagram", "YouTube", "Facebook"],
        "content_preference": "Progressive content, Marathi cinema/theater, food, cricket",
        "avg_engagement_rate": 3.6,
        "notes": "Mumbai inflates CPMs significantly. Target Pune, Nagpur, Nashik for better value. Marathi content has a loyal niche audience that responds well to regional pride."
    },
    "gu": {
        "language": "Gujarati",
        "states": ["Gujarat"],
        "population_reach": 55000000,
        "digital_penetration": 50,
        "avg_cpm": 70,
        "cpm_by_city_tier": {"tier1": 100, "tier2": 62, "tier3": 35},
        "competition_level": "medium",
        "top_platforms": ["YouTube", "Instagram", "WhatsApp", "Facebook"],
        "content_preference": "Business/entrepreneurship, food (Gujarati cuisine), family values, Navratri/Garba",
        "avg_engagement_rate": 3.7,
        "notes": "Entrepreneurial audience — business/money content performs well. Navratri is THE marketing event (Oct). Gujarati diaspora also reachable. Strong WhatsApp commerce culture."
    },
    "pa": {
        "language": "Punjabi",
        "states": ["Punjab", "Haryana", "parts of Delhi"],
        "population_reach": 33000000,
        "digital_penetration": 52,
        "avg_cpm": 75,
        "cpm_by_city_tier": {"tier1": 110, "tier2": 65, "tier3": 38},
        "competition_level": "medium",
        "top_platforms": ["YouTube", "Instagram", "Facebook"],
        "content_preference": "Music/entertainment, agriculture, food, Bollywood-Punjabi crossover",
        "avg_engagement_rate": 4.3,
        "notes": "Punjabi music/entertainment content has massive organic reach. Agricultural products and food brands perform exceptionally well. Baisakhi (Apr) and Lohri (Jan) are key festivals."
    },
    "or": {
        "language": "Odia",
        "states": ["Odisha"],
        "population_reach": 37000000,
        "digital_penetration": 38,
        "avg_cpm": 45,
        "cpm_by_city_tier": {"tier1": 70, "tier2": 40, "tier3": 22},
        "competition_level": "low",
        "top_platforms": ["YouTube", "Facebook", "ShareChat"],
        "content_preference": "Cultural heritage, Jagannath devotion, local news, entertainment",
        "avg_engagement_rate": 4.6,
        "notes": "Lowest CPMs among major language markets — exceptional value. Very low competition. Rath Yatra (Jul) is the biggest cultural moment. Growing digital adoption."
    },
    "as": {
        "language": "Assamese",
        "states": ["Assam"],
        "population_reach": 15000000,
        "digital_penetration": 35,
        "avg_cpm": 40,
        "cpm_by_city_tier": {"tier1": 60, "tier2": 35, "tier3": 20},
        "competition_level": "very_low",
        "top_platforms": ["YouTube", "Facebook", "ShareChat"],
        "content_preference": "Nature/tea culture, Bihu celebrations, local music, community content",
        "avg_engagement_rate": 5.0,
        "notes": "Smallest market but highest engagement rates. Almost zero brand competition in Assamese language. Bihu festival (Apr) drives massive engagement. Tea industry is key."
    },
    "ur": {
        "language": "Urdu",
        "states": ["Uttar Pradesh", "Jammu & Kashmir", "Telangana", "Bihar"],
        "population_reach": 52000000,
        "digital_penetration": 40,
        "avg_cpm": 50,
        "cpm_by_city_tier": {"tier1": 85, "tier2": 45, "tier3": 25},
        "competition_level": "low",
        "top_platforms": ["YouTube", "Facebook", "Instagram", "ShareChat"],
        "content_preference": "Poetry/shayari, food culture, religious content, entertainment",
        "avg_engagement_rate": 4.4,
        "notes": "Spread across multiple states — not geographically concentrated. Urdu content has aesthetic/poetic appeal. Ramzan and Eid are major marketing windows. Poetry-style ad copy outperforms direct selling."
    }
}


# ═══════ SEASONAL / FESTIVAL CALENDAR ═══════

SEASONAL_CALENDAR = {
    "january": {
        "festivals": [
            {"name": "Pongal / Thai Pongal", "regions": ["ta"], "dates": "Jan 14-17", "category_impact": {"food": 50, "home": 40, "fashion": 60}, "cpm_impact": -10, "notes": "Harvest festival. Traditional wear, cookware, gold jewelry spike. CPMs actually DROP because fewer national advertisers target Tamil market specifically."},
            {"name": "Makar Sankranti", "regions": ["mr", "kn", "te", "gu"], "dates": "Jan 14-15", "category_impact": {"food": 40, "fashion": 35}, "cpm_impact": 5, "notes": "Kite flying in Gujarat, til-gul in Maharashtra. Regional food brands peak."},
            {"name": "Lohri", "regions": ["pa"], "dates": "Jan 13", "category_impact": {"food": 45, "fashion": 30}, "cpm_impact": 0, "notes": "Bonfire festival. Family gatherings. Food and winter clothing."},
            {"name": "Republic Day", "regions": ["all"], "dates": "Jan 26", "category_impact": {"electronics": 25, "fashion": 20}, "cpm_impact": 15, "notes": "National sale events from e-commerce. Patriotic-themed campaigns."}
        ],
        "overall_ad_climate": "Post-new-year. Good time to launch — budgets reset, audience attention refreshed."
    },
    "february": {
        "festivals": [
            {"name": "Valentines Week", "regions": ["all"], "dates": "Feb 7-14", "category_impact": {"fashion": 45, "beauty": 50, "food": 40, "electronics": 30}, "cpm_impact": 25, "notes": "Urban-focused. Gift category spikes massively. CPMs rise due to competition."},
        ],
        "overall_ad_climate": "Moderate competition. Good month for product launches in beauty, fashion."
    },
    "march": {
        "festivals": [
            {"name": "Holi", "regions": ["hi", "pa", "gu", "bn"], "dates": "Mar 14-15 (varies)", "category_impact": {"food": 55, "beauty": 40, "fashion": 45}, "cpm_impact": 20, "notes": "Color-themed campaigns. Food and beverage brands peak. Skincare brands do pre-Holi campaigns."},
            {"name": "Ugadi / Gudi Padwa", "regions": ["te", "kn", "mr"], "dates": "Late Mar/Apr", "category_impact": {"fashion": 40, "home": 35, "food": 30}, "cpm_impact": 10, "notes": "New year for these regions. Auspicious purchases — gold, property, vehicles."},
        ],
        "overall_ad_climate": "Financial year end — B2B budgets flush, consumer savings mode until next salary."
    },
    "april": {
        "festivals": [
            {"name": "Tamil New Year (Puthandu)", "regions": ["ta"], "dates": "Apr 14", "category_impact": {"fashion": 50, "home": 40, "food": 35}, "cpm_impact": 5, "notes": "New beginnings. Traditional shopping."},
            {"name": "Vishu", "regions": ["ml"], "dates": "Apr 14", "category_impact": {"fashion": 45, "food": 40, "electronics": 30}, "cpm_impact": 5, "notes": "Kerala new year. Vishu Kani (auspicious items) shopping."},
            {"name": "Baisakhi", "regions": ["pa"], "dates": "Apr 13-14", "category_impact": {"food": 50, "fashion": 40}, "cpm_impact": 5, "notes": "Harvest festival. Agricultural products, food brands."},
            {"name": "Bihu (Rongali)", "regions": ["as"], "dates": "Apr 14-15", "category_impact": {"fashion": 55, "food": 45}, "cpm_impact": -5, "notes": "Biggest Assamese festival. Traditional wear, food. Very low CPMs."},
        ],
        "overall_ad_climate": "New financial year. B2B budgets fresh. Multiple regional new years — good for regional campaigns."
    },
    "may": {
        "festivals": [],
        "overall_ad_climate": "Summer. Low festival activity. Good for summer products (beverages, cooling appliances, travel). School vacation — family/kids products peak."
    },
    "june": {
        "festivals": [
            {"name": "Eid ul-Fitr", "regions": ["ur", "hi"], "dates": "Varies (lunar)", "category_impact": {"fashion": 65, "food": 55, "beauty": 40}, "cpm_impact": 15, "notes": "Massive shopping event. Fashion and food brands see 2-3x sales. Plan campaigns 2 weeks before."},
        ],
        "overall_ad_climate": "Monsoon begins in South India. Indoor activities increase → digital engagement rises."
    },
    "july": {
        "festivals": [
            {"name": "Rath Yatra", "regions": ["or"], "dates": "Jul (varies)", "category_impact": {"food": 40, "fashion": 35}, "cpm_impact": -10, "notes": "Biggest Odia cultural event. Religious tourism. Very low CPMs — underutilized marketing window."},
        ],
        "overall_ad_climate": "Monsoon across India. E-commerce comfort rises. In-home product categories perform well."
    },
    "august": {
        "festivals": [
            {"name": "Independence Day", "regions": ["all"], "dates": "Aug 15", "category_impact": {"electronics": 30, "fashion": 25}, "cpm_impact": 20, "notes": "Patriotic campaigns + freedom sales from e-commerce platforms."},
            {"name": "Raksha Bandhan", "regions": ["hi", "gu", "mr"], "dates": "Aug (varies)", "category_impact": {"food": 50, "fashion": 40, "electronics": 35}, "cpm_impact": 20, "notes": "Gift-driven. Sweet boxes, rakhis, gift sets. Brother-sister emotional content."},
            {"name": "Onam", "regions": ["ml"], "dates": "Aug-Sep (10 days)", "category_impact": {"fashion": 70, "food": 60, "electronics": 50, "home": 45}, "cpm_impact": 15, "notes": "Kerala's biggest festival. Kerala Gold purchases. Onam sadya (feast). 10-day window. Massive spending."},
        ],
        "overall_ad_climate": "Festival season starts ramping up. CPMs begin rising."
    },
    "september": {
        "festivals": [
            {"name": "Ganesh Chaturthi", "regions": ["mr", "kn", "te"], "dates": "Sep (varies)", "category_impact": {"food": 50, "home": 40, "fashion": 35}, "cpm_impact": 15, "notes": "Maharashtra's biggest festival. Eco-friendly Ganesh idols trending. Sweet shops, decorations."},
            {"name": "Eid ul-Adha", "regions": ["ur", "hi"], "dates": "Varies (lunar)", "category_impact": {"fashion": 45, "food": 50}, "cpm_impact": 10, "notes": "Important Muslim festival. Fashion and food brands."},
        ],
        "overall_ad_climate": "Pre-Diwali buildup begins. CPMs starting to rise. Good time to lock in ad accounts and creative."
    },
    "october": {
        "festivals": [
            {"name": "Navratri / Durga Puja / Dussehra", "regions": ["all"], "dates": "Oct (9 days + Dussehra)", "category_impact": {"fashion": 80, "food": 55, "electronics": 45, "beauty": 50, "home": 40}, "cpm_impact": 35, "notes": "PAN-INDIA mega festival. Garba in Gujarat, Durga Puja in Bengal, Navratri everywhere. Biggest fashion buying window. CPMs spike 30-40%. Launch campaigns 2 weeks BEFORE."},
        ],
        "overall_ad_climate": "PEAK SEASON BEGINS. Highest CPMs of the year. But also highest conversion intent. Budget allocation critical."
    },
    "november": {
        "festivals": [
            {"name": "Diwali", "regions": ["all"], "dates": "Nov (varies)", "category_impact": {"electronics": 70, "fashion": 65, "food": 60, "home": 55, "beauty": 50}, "cpm_impact": 45, "notes": "BIGGEST shopping event in India. Every category spikes. CPMs are at yearly peak. Pre-Diwali (2 weeks before) offers better CPMs than Diwali week itself."},
            {"name": "Bhai Dooj", "regions": ["hi", "bn"], "dates": "2 days after Diwali", "category_impact": {"food": 35, "fashion": 30}, "cpm_impact": 25, "notes": "Gift-giving between siblings. Similar to Raksha Bandhan but smaller."},
        ],
        "overall_ad_climate": "PEAK SEASON. Highest CPMs, highest competition, but also highest purchase intent. Post-Diwali CPMs drop sharply — good time for deals."
    },
    "december": {
        "festivals": [
            {"name": "Christmas", "regions": ["all"], "dates": "Dec 25", "category_impact": {"food": 40, "fashion": 35, "electronics": 30}, "cpm_impact": 10, "notes": "Urban-focused. Gift category. Less impactful in Tier-3 but growing."},
            {"name": "New Year's Eve", "regions": ["all"], "dates": "Dec 31", "category_impact": {"food": 45, "fashion": 40}, "cpm_impact": 15, "notes": "Party/celebration category. Restaurant, fashion, travel bookings."},
        ],
        "overall_ad_climate": "Post-Diwali cooldown. CPMs normalize. Year-end sales. Good for clearance campaigns and setting up January launches."
    }
}


# ═══════ CREATOR / INFLUENCER RATE CARDS ═══════

CREATOR_BENCHMARKS = {
    "tier_definitions": {
        "nano": {"followers": "1K-10K", "min": 1000, "max": 10000},
        "micro": {"followers": "10K-50K", "min": 10000, "max": 50000},
        "mid": {"followers": "50K-200K", "min": 50000, "max": 200000},
        "macro": {"followers": "200K-1M", "min": 200000, "max": 1000000},
        "mega": {"followers": "1M+", "min": 1000000, "max": 999999999}
    },
    "rate_cards_by_language": {
        "hi": {
            "nano": {"reel": {"min": 2000, "max": 8000}, "post": {"min": 1500, "max": 5000}, "story": {"min": 500, "max": 2000}},
            "micro": {"reel": {"min": 10000, "max": 35000}, "post": {"min": 8000, "max": 25000}, "story": {"min": 3000, "max": 10000}},
            "mid": {"reel": {"min": 40000, "max": 100000}, "post": {"min": 30000, "max": 80000}, "story": {"min": 15000, "max": 40000}},
            "macro": {"reel": {"min": 120000, "max": 350000}, "post": {"min": 80000, "max": 250000}, "story": {"min": 40000, "max": 120000}},
            "engagement_benchmarks": {"nano": 6.5, "micro": 4.2, "mid": 2.8, "macro": 1.8}
        },
        "ta": {
            "nano": {"reel": {"min": 2000, "max": 6000}, "post": {"min": 1500, "max": 4000}, "story": {"min": 500, "max": 1500}},
            "micro": {"reel": {"min": 8000, "max": 25000}, "post": {"min": 6000, "max": 18000}, "story": {"min": 2500, "max": 8000}},
            "mid": {"reel": {"min": 30000, "max": 80000}, "post": {"min": 25000, "max": 60000}, "story": {"min": 10000, "max": 30000}},
            "macro": {"reel": {"min": 100000, "max": 300000}, "post": {"min": 70000, "max": 200000}, "story": {"min": 35000, "max": 100000}},
            "engagement_benchmarks": {"nano": 7.0, "micro": 4.5, "mid": 3.0, "macro": 2.0}
        },
        "te": {
            "nano": {"reel": {"min": 1500, "max": 5000}, "post": {"min": 1000, "max": 3500}, "story": {"min": 400, "max": 1200}},
            "micro": {"reel": {"min": 7000, "max": 22000}, "post": {"min": 5000, "max": 15000}, "story": {"min": 2000, "max": 7000}},
            "mid": {"reel": {"min": 25000, "max": 70000}, "post": {"min": 20000, "max": 55000}, "story": {"min": 8000, "max": 25000}},
            "macro": {"reel": {"min": 80000, "max": 250000}, "post": {"min": 60000, "max": 180000}, "story": {"min": 30000, "max": 80000}},
            "engagement_benchmarks": {"nano": 7.5, "micro": 5.0, "mid": 3.2, "macro": 2.2}
        },
        "kn": {
            "nano": {"reel": {"min": 2000, "max": 6000}, "post": {"min": 1500, "max": 4500}, "story": {"min": 500, "max": 1800}},
            "micro": {"reel": {"min": 8000, "max": 28000}, "post": {"min": 6000, "max": 20000}, "story": {"min": 2500, "max": 9000}},
            "mid": {"reel": {"min": 30000, "max": 85000}, "post": {"min": 25000, "max": 65000}, "story": {"min": 10000, "max": 30000}},
            "macro": {"reel": {"min": 100000, "max": 280000}, "post": {"min": 75000, "max": 200000}, "story": {"min": 35000, "max": 90000}},
            "engagement_benchmarks": {"nano": 6.8, "micro": 4.3, "mid": 2.9, "macro": 1.9}
        },
        "ml": {
            "nano": {"reel": {"min": 2500, "max": 7000}, "post": {"min": 2000, "max": 5000}, "story": {"min": 800, "max": 2000}},
            "micro": {"reel": {"min": 10000, "max": 30000}, "post": {"min": 8000, "max": 22000}, "story": {"min": 3000, "max": 10000}},
            "mid": {"reel": {"min": 35000, "max": 90000}, "post": {"min": 28000, "max": 70000}, "story": {"min": 12000, "max": 35000}},
            "macro": {"reel": {"min": 100000, "max": 320000}, "post": {"min": 80000, "max": 220000}, "story": {"min": 40000, "max": 100000}},
            "engagement_benchmarks": {"nano": 7.2, "micro": 4.8, "mid": 3.2, "macro": 2.1}
        },
        "bn": {
            "nano": {"reel": {"min": 1500, "max": 5000}, "post": {"min": 1000, "max": 3500}, "story": {"min": 400, "max": 1200}},
            "micro": {"reel": {"min": 6000, "max": 20000}, "post": {"min": 5000, "max": 15000}, "story": {"min": 2000, "max": 6000}},
            "mid": {"reel": {"min": 22000, "max": 65000}, "post": {"min": 18000, "max": 50000}, "story": {"min": 8000, "max": 22000}},
            "macro": {"reel": {"min": 70000, "max": 220000}, "post": {"min": 55000, "max": 160000}, "story": {"min": 25000, "max": 70000}},
            "engagement_benchmarks": {"nano": 6.8, "micro": 4.5, "mid": 3.0, "macro": 2.0}
        },
        "mr": {
            "nano": {"reel": {"min": 2000, "max": 7000}, "post": {"min": 1500, "max": 5000}, "story": {"min": 600, "max": 1800}},
            "micro": {"reel": {"min": 9000, "max": 28000}, "post": {"min": 7000, "max": 20000}, "story": {"min": 2500, "max": 8000}},
            "mid": {"reel": {"min": 32000, "max": 85000}, "post": {"min": 25000, "max": 65000}, "story": {"min": 10000, "max": 30000}},
            "macro": {"reel": {"min": 100000, "max": 300000}, "post": {"min": 75000, "max": 220000}, "story": {"min": 35000, "max": 95000}},
            "engagement_benchmarks": {"nano": 6.5, "micro": 4.0, "mid": 2.7, "macro": 1.7}
        },
        "gu": {
            "nano": {"reel": {"min": 1500, "max": 5000}, "post": {"min": 1200, "max": 3500}, "story": {"min": 400, "max": 1200}},
            "micro": {"reel": {"min": 7000, "max": 22000}, "post": {"min": 5000, "max": 16000}, "story": {"min": 2000, "max": 7000}},
            "mid": {"reel": {"min": 25000, "max": 70000}, "post": {"min": 20000, "max": 55000}, "story": {"min": 8000, "max": 25000}},
            "macro": {"reel": {"min": 80000, "max": 240000}, "post": {"min": 60000, "max": 170000}, "story": {"min": 28000, "max": 75000}},
            "engagement_benchmarks": {"nano": 7.0, "micro": 4.5, "mid": 3.0, "macro": 2.0}
        },
        "pa": {
            "nano": {"reel": {"min": 2000, "max": 6000}, "post": {"min": 1500, "max": 4500}, "story": {"min": 500, "max": 1500}},
            "micro": {"reel": {"min": 8000, "max": 25000}, "post": {"min": 6000, "max": 18000}, "story": {"min": 2500, "max": 8000}},
            "mid": {"reel": {"min": 28000, "max": 75000}, "post": {"min": 22000, "max": 58000}, "story": {"min": 9000, "max": 28000}},
            "macro": {"reel": {"min": 85000, "max": 260000}, "post": {"min": 65000, "max": 190000}, "story": {"min": 30000, "max": 85000}},
            "engagement_benchmarks": {"nano": 7.2, "micro": 4.8, "mid": 3.1, "macro": 2.1}
        },
        "or": {
            "nano": {"reel": {"min": 1000, "max": 3500}, "post": {"min": 800, "max": 2500}, "story": {"min": 300, "max": 1000}},
            "micro": {"reel": {"min": 4000, "max": 15000}, "post": {"min": 3000, "max": 10000}, "story": {"min": 1500, "max": 5000}},
            "mid": {"reel": {"min": 18000, "max": 50000}, "post": {"min": 14000, "max": 38000}, "story": {"min": 6000, "max": 18000}},
            "macro": {"reel": {"min": 55000, "max": 160000}, "post": {"min": 40000, "max": 120000}, "story": {"min": 20000, "max": 55000}},
            "engagement_benchmarks": {"nano": 8.0, "micro": 5.5, "mid": 3.5, "macro": 2.5}
        },
        "as": {
            "nano": {"reel": {"min": 800, "max": 3000}, "post": {"min": 600, "max": 2000}, "story": {"min": 250, "max": 800}},
            "micro": {"reel": {"min": 3500, "max": 12000}, "post": {"min": 2500, "max": 8000}, "story": {"min": 1200, "max": 4000}},
            "mid": {"reel": {"min": 15000, "max": 42000}, "post": {"min": 12000, "max": 32000}, "story": {"min": 5000, "max": 15000}},
            "macro": {"reel": {"min": 45000, "max": 130000}, "post": {"min": 35000, "max": 100000}, "story": {"min": 15000, "max": 45000}},
            "engagement_benchmarks": {"nano": 8.5, "micro": 6.0, "mid": 4.0, "macro": 2.8}
        },
        "ur": {
            "nano": {"reel": {"min": 1500, "max": 5000}, "post": {"min": 1000, "max": 3500}, "story": {"min": 400, "max": 1200}},
            "micro": {"reel": {"min": 6000, "max": 20000}, "post": {"min": 4500, "max": 14000}, "story": {"min": 2000, "max": 6500}},
            "mid": {"reel": {"min": 22000, "max": 60000}, "post": {"min": 17000, "max": 45000}, "story": {"min": 7000, "max": 22000}},
            "macro": {"reel": {"min": 65000, "max": 200000}, "post": {"min": 50000, "max": 150000}, "story": {"min": 22000, "max": 65000}},
            "engagement_benchmarks": {"nano": 7.5, "micro": 5.0, "mid": 3.3, "macro": 2.2}
        }
    },
    "best_roi_tier": "micro",
    "best_roi_reasoning": "Micro-influencers (10K-50K) consistently deliver the best cost-per-conversion across Indian language markets. They have high trust with their niche audience, engagement rates 2-3x higher than macro creators, and costs are 5-10x lower. A portfolio of 5-8 micro-influencers outperforms 1 macro influencer for the same budget in 80% of cases.",
    "platform_preferences": {
        "Instagram": {"best_for": "Fashion, Beauty, Food, Lifestyle", "format": "Reels + Stories", "audience": "18-35 urban"},
        "YouTube": {"best_for": "Education, Tech, Long-form reviews, Entertainment", "format": "Shorts + dedicated videos", "audience": "18-45 broad"},
        "ShareChat": {"best_for": "Tier-2/3 targeting, regional language focus", "format": "Short videos", "audience": "18-30 semi-urban/rural"},
        "Moj": {"best_for": "Mass reach in regional languages", "format": "Short videos", "audience": "16-28 tier-2/3"},
    }
}


# ═══════ HELPER FUNCTIONS ═══════

def detect_industry(products: list, company_name: str = "", campaign_goal: str = "") -> str:
    """Auto-detect industry from product info, company name, and goal."""
    all_text = " ".join([
        company_name.lower(),
        campaign_goal.lower(),
        " ".join(p.get("name", "").lower() + " " + p.get("category", "").lower() + " " + p.get("description", "").lower()
                for p in products if isinstance(p, dict))
    ])

    best_match = "general"
    best_score = 0

    for key, data in META_ADS_BENCHMARKS.items():
        if key == "general":
            continue
        score = sum(1 for kw in data["keywords"] if kw in all_text)
        if score > best_score:
            best_score = score
            best_match = key

    return best_match


def get_benchmarks_for_request(products: list, target_languages: list, company_name: str = "", campaign_goal: str = "", current_month: str = "") -> dict:
    """Get all relevant benchmarks for a campaign request."""
    import datetime

    industry = detect_industry(products, company_name, campaign_goal)
    industry_data = META_ADS_BENCHMARKS[industry]

    if not current_month:
        current_month = datetime.datetime.now().strftime("%B").lower()

    regional_benchmarks = {}
    for lang_code in target_languages:
        code = lang_code.lower()[:2] if len(lang_code) > 2 else lang_code.lower()
        if code in REGIONAL_DATA:
            regional_benchmarks[code] = REGIONAL_DATA[code]
            # Add creator rates
            if code in CREATOR_BENCHMARKS["rate_cards_by_language"]:
                regional_benchmarks[code]["creator_rates"] = CREATOR_BENCHMARKS["rate_cards_by_language"][code]

    seasonal = SEASONAL_CALENDAR.get(current_month, {"festivals": [], "overall_ad_climate": "No specific seasonal data."})

    # Filter festivals relevant to target languages
    relevant_festivals = []
    lang_codes = [l.lower()[:2] if len(l) > 2 else l.lower() for l in target_languages]
    for f in seasonal.get("festivals", []):
        if "all" in f["regions"] or any(lc in f["regions"] for lc in lang_codes):
            relevant_festivals.append(f)

    return {
        "industry": industry_data,
        "regional": regional_benchmarks,
        "seasonal": {
            "month": current_month,
            "festivals": relevant_festivals,
            "ad_climate": seasonal.get("overall_ad_climate", ""),
        },
        "creator_strategy": {
            "best_roi_tier": CREATOR_BENCHMARKS["best_roi_tier"],
            "best_roi_reasoning": CREATOR_BENCHMARKS["best_roi_reasoning"],
            "platform_preferences": CREATOR_BENCHMARKS["platform_preferences"],
        }
    }
