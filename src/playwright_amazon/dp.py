from playwright.async_api import async_playwright
from playwright_amazon.utils import get_amazon_detail_page_url


async def extract_dp(asin: str) -> dict:
    """Fetch product details from Amazon using ASIN"""
    url = get_amazon_detail_page_url(asin)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Set user agent to avoid blocking
        await page.set_extra_http_headers(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            }
        )

        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(2000)

        try:
            title = await page.locator("span#productTitle").text_content()
        except Exception:
            title = None

        try:
            price = await page.locator(
                "span.a-price span.a-offscreen"
            ).first.text_content()
        except Exception:
            price = None

        try:
            rating = await page.locator("span.a-icon-alt").first.text_content()
        except Exception:
            rating = None

        try:
            bullets = await page.locator(
                "#feature-bullets ul li span"
            ).all_text_contents()
        except Exception:
            bullets = []

        try:
            images = await page.locator("img#landingImage").get_attribute("src")
        except Exception:
            images = None

        await browser.close()

    return {
        "asin": asin,
        "url": url,
        "title": title.strip() if title else None,
        "price": price.strip() if price else None,
        "rating": rating.strip() if rating else None,
        "features": [b.strip() for b in bullets if b.strip()],
        "image": images,
    }
