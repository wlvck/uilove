"""
Phase 1: Parse all categories from landing.love
Output: categories.json with title, url, and count
"""

import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.landing.love"

def parse_categories():
    """Parse all categories from the main page."""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(f"{BASE_URL}/about/", headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    categories = []
    
    # Find all category links - they follow pattern /categories/name/
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if '/categories/' in href:
            # Extract text and count
            text = link.get_text(strip=True)
            
            # Skip if already processed this URL
            full_url = href if href.startswith('http') else BASE_URL + href
            if any(c['url'] == full_url for c in categories):
                continue
            
            # Parse title and count (format: "Title\n123" or "Title 123")
            parts = text.split('\n')
            if len(parts) >= 2:
                title = parts[0].strip()
                try:
                    count = int(parts[-1].strip())
                except ValueError:
                    count = None
            else:
                # Try to extract number from end
                import re
                match = re.match(r'(.+?)\s*(\d+)$', text)
                if match:
                    title = match.group(1).strip()
                    count = int(match.group(2))
                else:
                    title = text
                    count = None
            
            categories.append({
                'title': title,
                'url': full_url,
                'count': count,
                'slug': href.split('/categories/')[-1].rstrip('/')
            })
    
    # Remove duplicates based on slug
    seen_slugs = set()
    unique_categories = []
    for cat in categories:
        if cat['slug'] not in seen_slugs:
            seen_slugs.add(cat['slug'])
            unique_categories.append(cat)
    
    return unique_categories


def parse_styles():
    """Parse all styles."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(f"{BASE_URL}/about/", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    styles = []
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if '/style/' in href:
            text = link.get_text(strip=True)
            full_url = href if href.startswith('http') else BASE_URL + href
            
            if any(s['url'] == full_url for s in styles):
                continue
                
            parts = text.split('\n')
            title = parts[0].strip() if parts else text
            try:
                count = int(parts[-1].strip()) if len(parts) > 1 else None
            except:
                count = None
                
            styles.append({
                'title': title,
                'url': full_url,
                'count': count,
                'slug': href.split('/style/')[-1].rstrip('/')
            })
    
    return styles


def parse_collections():
    """Parse all collections (GSAP, WebGL, ThreeJS)."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(f"{BASE_URL}/about/", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    collections = []
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if '/collection/' in href:
            text = link.get_text(strip=True)
            full_url = href if href.startswith('http') else BASE_URL + href
            
            if any(c['url'] == full_url for c in collections):
                continue
                
            parts = text.split('\n')
            title = parts[0].strip() if parts else text
            try:
                count = int(parts[-1].strip()) if len(parts) > 1 else None
            except:
                count = None
                
            collections.append({
                'title': title,
                'url': full_url,
                'count': count,
                'slug': href.split('/collection/')[-1].rstrip('/')
            })
    
    return collections


def parse_platforms():
    """Parse all platforms (Webflow, Framer, etc.)."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(f"{BASE_URL}/about/", headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    platforms = []
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if '/platform/' in href:
            text = link.get_text(strip=True)
            full_url = href if href.startswith('http') else BASE_URL + href
            
            if any(p['url'] == full_url for p in platforms):
                continue
                
            parts = text.split('\n')
            title = parts[0].strip() if parts else text
            try:
                count = int(parts[-1].strip()) if len(parts) > 1 else None
            except:
                count = None
                
            platforms.append({
                'title': title,
                'url': full_url,
                'count': count,
                'slug': href.split('/platform/')[-1].rstrip('/')
            })
    
    return platforms


def main():
    print("=" * 50)
    print("Landing.love Scraper - Phase 1 & 2")
    print("=" * 50)
    
    # Parse categories
    print("\n[1/4] Parsing categories...")
    categories = parse_categories()
    print(f"      Found {len(categories)} categories")
    
    with open('categories.json', 'w', encoding='utf-8') as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
    print("      Saved to categories.json")
    
    # Parse styles
    print("\n[2/4] Parsing styles...")
    styles = parse_styles()
    print(f"      Found {len(styles)} styles")
    
    with open('styles.json', 'w', encoding='utf-8') as f:
        json.dump(styles, f, indent=2, ensure_ascii=False)
    print("      Saved to styles.json")
    
    # Parse collections
    print("\n[3/4] Parsing collections...")
    collections = parse_collections()
    print(f"      Found {len(collections)} collections")
    
    with open('collections.json', 'w', encoding='utf-8') as f:
        json.dump(collections, f, indent=2, ensure_ascii=False)
    print("      Saved to collections.json")
    
    # Parse platforms
    print("\n[4/4] Parsing platforms...")
    platforms = parse_platforms()
    print(f"      Found {len(platforms)} platforms")
    
    with open('platforms.json', 'w', encoding='utf-8') as f:
        json.dump(platforms, f, indent=2, ensure_ascii=False)
    print("      Saved to platforms.json")
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Categories: {len(categories)}")
    print(f"Styles:     {len(styles)}")
    print(f"Collections:{len(collections)}")
    print(f"Platforms:  {len(platforms)}")
    print("\nPhase 1 & 2 complete! Run parse_websites.py next.")


if __name__ == "__main__":
    main()
