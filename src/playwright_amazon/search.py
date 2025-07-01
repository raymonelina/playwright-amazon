from playwright.async_api import async_playwright
from playwright_amazon.utils import get_amazon_search_page_url


async def extract_search(query: str, limit: int = 100) -> list[dict]:
    """Extracts search result summaries for a given Amazon search query (fast version)"""
    url = get_amazon_search_page_url(query)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Set user agent to avoid bot detection
        await page.set_extra_http_headers(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            }
        )

        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(2000)

        results = []

        base = page.locator(
            "div.s-main-slot div[data-asin][data-index][role='listitem']"
        )
        count = await base.count()

        for i in range(min(count, limit)):
            item = base.nth(i)
            try:
                data = await item.evaluate(
                    """
                    (el) => {
                        const asin = el.getAttribute('data-asin');
                        const index = el.getAttribute('data-index');
                        const span = el.querySelector('a h2 span');
                        const title = span ? span.textContent.trim() : null;

                        return {
                            asin: asin?.trim() || null,
                            index: index ? parseInt(index) : null,
                            title: title
                        };
                    }
                    """
                )
                if data:
                    results.append(data)
            except Exception:
                continue

        await browser.close()
        return results
