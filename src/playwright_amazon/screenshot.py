from pathlib import Path
from playwright.async_api import async_playwright


async def take_screenshot(url: str, output_path: str, full_page: bool = True):
    """Take a screenshot of the given URL and save it to a local file.
    If full_page is True, capture the entire page; otherwise, capture just the viewport.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Set user agent to reduce bot detection
        await page.set_extra_http_headers(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            }
        )

        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(2000)

        await page.screenshot(path=output_path, full_page=full_page)
        await browser.close()


async def take_dual_screenshots(url: str, base_path: str, page_type: str):
    """Take both full-page and viewport-only screenshots.
    Filenames include page_type like '-search-' or '-dp-'."""
    base = Path(base_path)
    suffix = base.suffix
    stem = base.stem

    # Decorate filename with page_type
    full_name = stem + f"-{page_type}" + suffix
    screen_name = stem + f"-{page_type}-sc" + suffix

    full_path = base.with_name(full_name)
    screen_path = base.with_name(screen_name)

    await take_screenshot(url, str(full_path), full_page=True)
    await take_screenshot(url, str(screen_path), full_page=False)

    return str(full_path), str(screen_path)
