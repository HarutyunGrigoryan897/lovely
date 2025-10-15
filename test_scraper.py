import asyncio
import random
import aiohttp
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout


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
                    print(f"📊 Exchange rate: 1 CNY = {usd_rate} USD")
                    return usd_rate
                else:
                    print(f"⚠️  Failed to fetch exchange rate (status {response.status})")
                    return None
    except Exception as e:
        print(f"⚠️  Error fetching exchange rate: {e}")
        return None


async def scrape_once(p, url):
    """Run a single scrape attempt"""
    print(f"Navigating to {url}...")

    browser = await p.chromium.launch(headless=True)
    page = await browser.new_page()
    try:
        # Use "domcontentloaded" instead of full "load" for reliability
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        print("Waiting for WebSocket data (5s)...")
        await asyncio.sleep(5)

        print("Looking for element with id='jzj_au_A'...")
        element = await page.query_selector("#jzj_au_A")

        if element:
            value = await element.text_content()
            print(f"\n✓ Successfully scraped! Value: {value}")
            return value.strip()

        print("✗ Element not found this time.")
        return None

    except PlaywrightTimeout:
        print("✗ Page timeout, skipping this attempt.")
        return None

    except Exception as e:
        print(f"✗ Error: {e}")
        return None

    finally:
        await browser.close()
        print("Browser closed.\n")


async def scrape_website(max_retries=10):
    """Keep trying until price found or max retries reached"""
    url = "http://fyx9999.com/"
    
    # Get exchange rate first
    print("Fetching CNY to USD exchange rate...")
    exchange_rate = await get_cny_to_usd_rate()
    if not exchange_rate:
        print("⚠️  Warning: Could not fetch exchange rate. Will show CNY value only.")
    
    async with async_playwright() as p:
        for attempt in range(1, max_retries + 1):
            print("=" * 60)
            print(f"Attempt {attempt}/{max_retries}")
            print("=" * 60)

            value = await scrape_once(p, url)
            if value:
                print(f"🎯 Got value on attempt {attempt}: {value} CNY")
                
                # Convert to USD if exchange rate is available
                if exchange_rate:
                    try:
                        # Extract numeric value from the scraped string
                        numeric_value = float(value.replace(',', '').strip())
                        usd_value = numeric_value * exchange_rate
                        print(f"💵 Converted to USD: {usd_value:.2f}")
                        return {"cny": value, "usd": f"{usd_value:.2f}", "rate": exchange_rate}
                    except ValueError:
                        print(f"⚠️  Could not convert '{value}' to number")
                        return {"cny": value, "usd": None, "rate": exchange_rate}
                
                return {"cny": value, "usd": None, "rate": None}

            wait_time = random.uniform(2, 5)
            print(f"Retrying in {wait_time:.1f} seconds...\n")
            await asyncio.sleep(wait_time)

        print("⚠️  All retries failed. Could not get value.")
        return None


def main():
    print("=" * 60)
    print("Auto-Retry Web Scraper - Playwright Chromium")
    print("=" * 60)

    result = asyncio.run(scrape_website(max_retries=10))

    print("\n" + "=" * 60)
    if result:
        print(f"✅ Final Result:")
        print(f"   CNY: {result['cny']}")
        if result['usd']:
            print(f"   USD: ${result['usd']}")
            print(f"   Rate: 1 CNY = {result['rate']} USD")
    else:
        print("❌ Scraping failed after all retries.")
    print("=" * 60)


if __name__ == "__main__":
    main()
