def get_amazon_detail_page_url(asin: str) -> str:
    """Construct the Amazon product detail page URL for a given ASIN"""
    return f"https://www.amazon.com/dp/{asin}"


def get_amazon_search_page_url(query: str) -> str:
    """Construct the Amazon search result page URL for a given query"""
    return f"https://www.amazon.com/s?k={query.replace(' ', '+')}"


def get_amazon_page_url(page_type: str, value: str) -> str:
    """Unified page URL builder for supported Amazon page types"""
    page_type = page_type.lower()
    if page_type == "dp":
        return get_amazon_detail_page_url(value)
    elif page_type == "search":
        return get_amazon_search_page_url(value)
    else:
        raise ValueError(
            f"Unsupported page_type '{page_type}'. Expected 'dp' or 'search'."
        )
