from playwright.async_api import async_playwright


def get_amazon_search_page_url(query: str) -> str:
    """Construct the Amazon search result page URL for a given query"""
    return f"https://www.amazon.com/s?k={query.replace(' ', '+')}"


async def extract_search(query: str, limit: int = 10) -> list[dict]:
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
            "div.s-main-slot div[data-asin][role='listitem'][data-index]"
        )
        count = await base.count()

        print(f"Found {count} items for query '{query}'")

        for i in range(min(count, limit)):
            item = base.nth(i)
            try:
                data = await item.evaluate(
                    """
                    (el) => {
                        const asin = el.getAttribute('data-asin');

                        return {
                            asin: asin.trim(),
                            title: '',
                            url: ''
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
