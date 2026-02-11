# Landing.love Scraper

Parse all website data from landing.love - a curated gallery of animated landing pages.

## Setup

```bash
pip install -r requirements.txt
```

## Usage - Run in Order

### Phase 1 & 2: Parse Categories, Styles, Collections, Platforms
```bash
python parse_categories.py
```
**Output:**
- `categories.json` - All website categories (48+)
- `styles.json` - Design styles (dark mode, gradient, etc.)
- `collections.json` - Tech collections (GSAP, WebGL, ThreeJS)
- `platforms.json` - Platforms (Webflow, Framer, Wix)

### Phase 3: Parse Website Listings
```bash
python parse_websites.py
```
**Output:**
- `websites_list.json` - All websites with basic info
- `websites_by_category.json` - Websites grouped by category

### Phase 4: Parse Detailed Information
```bash
python parse_details.py
```
**Output:**
- `websites_detailed.json` - Full details including:
  - Title & description
  - Video recording URL
  - Original website URL
  - Tags & categories
  - Screenshots

## Data Structure

### categories.json
```json
[
  {
    "title": "Minimal",
    "url": "https://www.landing.love/categories/minimal/",
    "count": 1298,
    "slug": "minimal"
  }
]
```

### websites_detailed.json
```json
[
  {
    "title": "Example Site",
    "url": "https://www.landing.love/example-site/",
    "slug": "example-site",
    "original_url": "https://example.com",
    "video_url": "https://..../video.mp4",
    "description": "...",
    "categories": ["minimal", "portfolio"],
    "tags": ["Minimal", "Dark Mode"],
    "images": ["..."]
  }
]
```

## Notes

- Scripts save progress automatically - safe to interrupt and resume
- Be respectful: includes delays between requests
- Adjust `max_workers` in parse_details.py for speed vs. server load
- Some selectors may need adjustment if site structure changes
