"""
Gold price scraper from external website
Scrapes CNY price and converts to USD
"""
import asyncio
import random
import aiohttp
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


async def get_cny_to_usd_rate():
    """Fetch the current CNY to USD exchange rate"""
    try:
        async with aiohttp.ClientSession() as session:
            # Using exchangerate-api.com (free, no API key needed for basic usage)
            url = "https://open.exchangerate-api.com/v6/latest/CNY"
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    usd_rate = data['rates']['USD']
                    logger.info(f"Exchange rate: 1 CNY = {usd_rate} USD")
                    return usd_rate
                else:
                    logger.warning(f"Failed to fetch exchange rate (status {response.status})")
                    return None
    except Exception as e:
        logger.error(f"Error fetching exchange rate: {e}")
        return None


async def scrape_once(p, url):
    """Run a single scrape attempt"""
    logger.info(f"Navigating to {url}...")

    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()
    try:
        # Use "domcontentloaded" instead of full "load" for reliability
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        logger.info("Waiting for WebSocket data (5s)...")
        await asyncio.sleep(5)

        logger.info("Looking for element with id='jzj_au_A'...")
        element = await page.query_selector("#jzj_au_A")

        if element:
            value = await element.text_content()
            logger.info(f"Successfully scraped! Value: {value}")
            return value.strip()

        logger.warning("Element not found this time.")
        return None

    except PlaywrightTimeout:
        logger.warning("Page timeout, skipping this attempt.")
        return None

    except Exception as e:
        logger.error(f"Scraping error: {e}")
        return None

    finally:
        await browser.close()
        logger.info("Browser closed.")


async def scrape_gold_price(max_retries=10):
    """Keep trying until price found or max retries reached"""
    url = "http://fyx9999.com/"
    
    # Get exchange rate first
    logger.info("Fetching CNY to USD exchange rate...")
    exchange_rate = await get_cny_to_usd_rate()
    if not exchange_rate:
        logger.warning("Could not fetch exchange rate. Will show CNY value only.")
        return None
    
    async with async_playwright() as p:
        for attempt in range(1, max_retries + 1):
            logger.info(f"Scraping attempt {attempt}/{max_retries}")

            value = await scrape_once(p, url)
            if value:
                logger.info(f"Got value on attempt {attempt}: {value} CNY")
                
                # Convert to USD if exchange rate is available
                if exchange_rate:
                    try:
                        # Extract numeric value from the scraped string
                        numeric_value = float(value.replace(',', '').strip())
                        usd_value = numeric_value * exchange_rate
                        logger.info(f"Converted to USD: {usd_value:.2f}")
                        return {"cny": value, "usd": usd_value, "rate": exchange_rate}
                    except ValueError:
                        logger.error(f"Could not convert '{value}' to number")
                        return None
                
                return None

            wait_time = random.uniform(2, 5)
            logger.info(f"Retrying in {wait_time:.1f} seconds...")
            await asyncio.sleep(wait_time)

        logger.error("All retries failed. Could not get value.")
        return None


def should_update_gold_price():
    """
    Check if gold price needs to be updated
    Returns True if:
    - No active gold price exists
    - Last update was more than 1 minute ago
    """
    from .models import GoldPrice
    
    active_price = GoldPrice.objects.filter(is_active=True).first()
    
    if not active_price:
        logger.info("No active gold price found. Update needed.")
        return True
    
    # Check if updated more than 1 minute ago
    time_since_update = timezone.now() - active_price.updated_at
    needs_update = time_since_update > timedelta(minutes=1)
    
    if needs_update:
        logger.info(f"Gold price last updated {time_since_update.total_seconds() / 60:.1f} minutes ago. Update needed.")
    else:
        logger.info(f"Gold price updated {time_since_update.total_seconds() / 60:.1f} minutes ago. No update needed.")
    
    return needs_update


def update_gold_price_sync():
    """
    Synchronous wrapper to update gold price in database
    Returns tuple: (success: bool, message: str)
    """
    from .models import GoldPrice
    
    try:
        # Run async scraping
        result = asyncio.run(scrape_gold_price(max_retries=10))
        
        if not result or not result.get('usd'):
            logger.error("Failed to scrape gold price")
            return False, "Failed to scrape gold price"
            return False, "Failed to scrape gold price"
        
        usd_price = Decimal(str(result['usd']))
        
        # Get or create active gold price
        active_price = GoldPrice.objects.filter(is_active=True).first()
        
        if active_price:
            # Update existing price
            active_price.price_per_gram = usd_price
            active_price.save()
            logger.info(f"Updated gold price to ${usd_price}/gram")
            return True, ""
        else:
            # Create new active price
            GoldPrice.objects.create(
                price_per_gram=usd_price,
                markup_percentage=Decimal('25.00'),
                is_active=True
            )
            logger.info(f"Created new gold price: ${usd_price}/gram")
            return True, ""
            
    except Exception as e:
        logger.error(f"Error updating gold price: {e}")
        return False, ""
