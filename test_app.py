# test_app.py
import pytest
from connectors.cars24 import Cars24Scraper
from connectors.olx import OlxScraper
from connectors.cardekho import CardekhoScraper

# Configuration for each scraper
SCRAPER_CONFIGS = [
    (Cars24Scraper, "Cars24"),
    (OlxScraper, "OLX"),
    (CardekhoScraper, "Cardekho"),
]

# Test that each scraper implements fetch_listings and returns valid data
@pytest.mark.parametrize("ScraperClass, source_name", SCRAPER_CONFIGS)
def test_scraper_fetch_listings(ScraperClass, source_name):
    scraper = ScraperClass()
    
    filters = {
        "brand": "honda",
        "model": "city",
        "city": "bangalore",
        "fuel": "petrol",
        "year_min": 2008,
        "year_max": 2020,
        "transmission": "manual"
    }
    
    # Ensure fetch_listings exists
    assert hasattr(scraper, "fetch_listings"), f"{source_name}: Missing fetch_listings method"
    
    result = scraper.fetch_listings(filters=filters)
    
    # Check basic structure
    assert isinstance(result, list), f"{source_name}: Result should be a list"
    if result:
        first_item = result[0]
        assert isinstance(first_item, dict), f"{source_name}: Each item should be a dict"
        required_keys = ["brand", "model", "price", "year", "mileage", "transmission", "fuel", "url", "source"]
        for key in required_keys:
            assert key in first_item, f"{source_name}: Missing key {key}"
    
    print(f"{source_name} scraper test passed!")

# Optional: test combined pipeline
def test_combined_scrapers():
    filters = {
        "brand": "honda",
        "model": "city",
        "city": "bangalore",
        "fuel": "petrol",
        "year_min": 2008,
        "year_max": 2020,
        "transmission": "manual"
    }
    
    all_data = []
    for ScraperClass, source_name in SCRAPER_CONFIGS:
        scraper = ScraperClass()
        data = scraper.fetch_listings(filters=filters)
        all_data.extend(data)
    
    # Ensure combined results
    assert isinstance(all_data, list), "Combined data should be a list"
    assert len(all_data) > 0, "Combined data should not be empty"
    for item in all_data:
        assert "brand" in item and "model" in item and "price" in item, "Missing essential keys"

    print("Combined scraper pipeline test passed!")
