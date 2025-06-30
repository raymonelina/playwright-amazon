import argparse
import asyncio

from playwright_amazon.dp import extract_dp
from playwright_amazon.search import extract_search


def main():
    parser = argparse.ArgumentParser(
        prog="playwright_amazon", description="Playwright Amazon CLI"
    )
    parser.add_argument(
        "-p",
        "--page",
        required=True,
        choices=["search", "dp"],
        help="The type of Amazon page to process: 'search' or 'dp'.",
    )
    parser.add_argument(
        "--asin", type=str, help="Amazon ASIN (required if --page is 'dp')"
    )
    parser.add_argument(
        "--query", help="Search query string (required if --page is 'search')"
    )

    args = parser.parse_args()

    if args.page == "dp":
        if not args.asin:
            parser.error("--asin is required when --page is 'dp'")
        result = asyncio.run(extract_dp(args.asin))
        print("📦 Product Details:")
        for k, v in result.items():
            print(f"{k}: {v}")

    elif args.page == "search":
        if not args.query:
            parser.error("--query is required when --page is 'search'")
        results = asyncio.run(extract_search(args.query))
        print(f"🔍 Found {len(results)} results:")
        for item in results:
            print(f"- {item['title']} ({item['asin']}): {item['url']}")


if __name__ == "__main__":
    main()
