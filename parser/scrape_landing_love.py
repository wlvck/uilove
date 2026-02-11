"""
Landing.love Full Scraper
Extracts: title, description, video_url, original_url for all websites

Structure discovered:
- Category pages: /categories/{slug}/ and /categories/{slug}/page/{n}/
- Site detail pages: /sites/{slug}/
- Videos: https://cdn.landing.love/videos/{slug}.mp4
- Images: https://cdn.landing.love/images/{slug}.webp
- Original site: found in "Visit Site" link with ?ref=landing.love
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
from urllib.parse import urljoin

BASE_URL = "https://www.landing.love"
CDN_URL = "https://cdn.landing.love"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}


def load_categories(filepath='categories.json'):
    """Load categories from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_page(url, retries=3):
    """Fetch a page with retry logic."""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
            else:
                print(f"      Error fetching {url}: {e}")
                return None
    return None


def parse_category_page(html, category_slug):
    """
    Parse a category listing page and extract website cards.
    Returns list of dicts with: slug, title, thumbnail, categories
    """
    soup = BeautifulSoup(html, 'html.parser')
    websites = []
    
    # Find all links to /sites/ pages
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        
        # Match /sites/sitename/ pattern
        match = re.match(r'^/sites/([^/]+)/?$', href)
        if not match:
            continue
        
        slug = match.group(1)
        
        # Get title from link text
        title = link.get_text(strip=True)
        
        # Get thumbnail from img inside link
        img = link.find('img')
        thumbnail = img.get('src', '') if img else f"{CDN_URL}/images/{slug}-thumb.webp"
        
        # Get categories from sibling elements (tags)
        categories = [category_slug]
        parent = link.find_parent()
        if parent:
            for cat_link in parent.find_all('a', href=True):
                cat_href = cat_link.get('href', '')
                if '/categories/' in cat_href:
                    cat_match = re.search(r'/categories/([^/]+)/?', cat_href)
                    if cat_match and cat_match.group(1) not in categories:
                        categories.append(cat_match.group(1))
        
        # Avoid duplicates in this page
        if not any(w['slug'] == slug for w in websites):
            websites.append({
                'slug': slug,
                'title': title if title else slug.replace('-', ' ').title(),
                'thumbnail': thumbnail,
                'categories': categories,
                'detail_url': f"{BASE_URL}/sites/{slug}/",
                'video_url': f"{CDN_URL}/videos/{slug}.mp4",
                'image_url': f"{CDN_URL}/images/{slug}.webp",
            })
    
    return websites


def has_next_page(html, current_page):
    """Check if there's a next page."""
    soup = BeautifulSoup(html, 'html.parser')
    next_page = current_page + 1
    
    # Look for pagination links
    for link in soup.find_all('a', href=True):
        if f'/page/{next_page}' in link.get('href', ''):
            return True
    return False


def parse_site_detail(html, slug):
    """
    Parse a site detail page to extract description and original URL.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    details = {
        'description': '',
        'original_url': '',
        'tags': [],
    }
    
    # Get description from meta tag or h1 sibling paragraph
    meta_desc = soup.find('meta', {'name': 'description'})
    if meta_desc:
        details['description'] = meta_desc.get('content', '')
    
    # If no meta description, try to find it in the page content
    if not details['description']:
        h1 = soup.find('h1')
        if h1:
            # Description is often in a p tag after h1
            next_p = h1.find_next('p')
            if next_p:
                details['description'] = next_p.get_text(strip=True)
    
    # Find original website URL (Visit Site link)
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        text = link.get_text(strip=True).lower()
        
        if 'visit site' in text or 'visit' in text:
            # Remove the ref parameter to get clean URL
            original = re.sub(r'\?ref=landing\.love$', '', href)
            if original and not original.startswith('/') and BASE_URL not in original:
                details['original_url'] = original
                break
    
    # Alternative: find external link that's not social/sponsor
    if not details['original_url']:
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if href.startswith('http') and 'landing.love' not in href:
                # Skip known non-original URLs
                skip_patterns = ['webflow.com', 'framer.link', 'twitter.com', 'x.com', 
                               'instagram', 'youtube', 'linkedin', 'bsky.app', 
                               'lemonsqueezy', 'lapa.ninja', 'uistore', 'bookmarks']
                if not any(p in href.lower() for p in skip_patterns):
                    details['original_url'] = re.sub(r'\?ref=landing\.love$', '', href)
                    break
    
    # Extract tags/categories
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if '/categories/' in href or '/style/' in href or '/collection/' in href:
            tag = link.get_text(strip=True)
            if tag and tag not in details['tags']:
                details['tags'].append(tag)
    
    return details


def scrape_category(category, all_websites):
    """Scrape all pages of a single category."""
    slug = category['slug']
    base_url = category['url']
    
    page = 1
    category_sites = []
    
    while True:
        # Build URL for current page
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}page/{page}/"
        
        print(f"      Page {page}...", end=" ", flush=True)
        
        html = get_page(url)
        if not html:
            print("no content")
            break
        
        # Parse websites from this page
        sites = parse_category_page(html, slug)
        
        # Filter out already seen sites (from other categories)
        new_sites = []
        for site in sites:
            if site['slug'] not in all_websites:
                new_sites.append(site)
                all_websites[site['slug']] = site
            else:
                # Add this category to existing site
                if slug not in all_websites[site['slug']]['categories']:
                    all_websites[site['slug']]['categories'].append(slug)
        
        print(f"found {len(sites)} sites ({len(new_sites)} new)")
        category_sites.extend(new_sites)
        
        # Check for next page
        if not has_next_page(html, page):
            break
        
        page += 1
        time.sleep(1)  # Be polite
    
    return category_sites


def fetch_site_details(websites, batch_size=10, delay=1):
    """
    Fetch detailed info (description, original_url) for each website.
    """
    total = len(websites)
    
    for i, (slug, site) in enumerate(websites.items()):
        if site.get('description') and site.get('original_url'):
            continue  # Already have details
        
        print(f"  [{i+1}/{total}] Fetching details for {slug}...", end=" ", flush=True)
        
        html = get_page(site['detail_url'])
        if html:
            details = parse_site_detail(html, slug)
            site.update(details)
            print(f"OK")
        else:
            print(f"FAILED")
        
        # Save progress periodically
        if (i + 1) % batch_size == 0:
            save_progress(websites, 'websites_progress.json')
        
        time.sleep(delay)
    
    return websites


def save_progress(data, filepath):
    """Save current progress to JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        if isinstance(data, dict):
            json.dump(list(data.values()), f, indent=2, ensure_ascii=False)
        else:
            json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    print("=" * 60)
    print("Landing.love Full Scraper")
    print("=" * 60)
    
    # Load categories
    if not os.path.exists('categories.json'):
        print("\nError: categories.json not found!")
        print("Please provide the categories.json file.")
        return
    
    categories = load_categories()
    print(f"\nLoaded {len(categories)} categories")
    
    # Phase 1: Scrape all category pages
    print("\n" + "-" * 60)
    print("PHASE 1: Scraping category listings")
    print("-" * 60)
    
    all_websites = {}  # slug -> website data
    
    for i, category in enumerate(categories):
        print(f"\n[{i+1}/{len(categories)}] {category['title']} ({category['count']} sites)")
        scrape_category(category, all_websites)
        time.sleep(2)  # Pause between categories
    
    print(f"\n✓ Found {len(all_websites)} unique websites")
    save_progress(all_websites, 'websites_basic.json')
    print("  Saved to websites_basic.json")
    
    # Phase 2: Fetch detailed info for each site
    print("\n" + "-" * 60)
    print("PHASE 2: Fetching detailed information")
    print("-" * 60)
    print("(This will take a while - progress is saved automatically)\n")
    
    all_websites = fetch_site_details(all_websites, batch_size=20, delay=1.5)
    
    # Save final output
    output = list(all_websites.values())
    
    with open('websites_complete.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    # Generate summary
    print("\n" + "=" * 60)
    print("COMPLETE!")
    print("=" * 60)
    print(f"Total websites:      {len(output)}")
    print(f"With description:    {sum(1 for w in output if w.get('description'))}")
    print(f"With original URL:   {sum(1 for w in output if w.get('original_url'))}")
    print(f"With video URL:      {sum(1 for w in output if w.get('video_url'))}")
    print("\nSaved to: websites_complete.json")
    
    # Also save as CSV for easy viewing
    try:
        import csv
        with open('websites_complete.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'title', 'slug', 'description', 'original_url', 
                'video_url', 'image_url', 'thumbnail', 'detail_url', 
                'categories', 'tags'
            ])
            writer.writeheader()
            for site in output:
                row = site.copy()
                row['categories'] = ', '.join(site.get('categories', []))
                row['tags'] = ', '.join(site.get('tags', []))
                writer.writerow(row)
        print("Saved to: websites_complete.csv")
    except Exception as e:
        print(f"Note: CSV export failed: {e}")


if __name__ == "__main__":
    main()
