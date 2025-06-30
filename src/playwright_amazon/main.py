import argparse


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

    args = parser.parse_args()
    print(f"Selected page type: {args.page}")


if __name__ == "__main__":
    main()
