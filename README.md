# 🎭 playwright-amazon

A lightweight Playwright-based automation tool for scraping or testing Amazon product pages.

---



## 🚀 Getting Started

### 1. Install Dependencies

Make sure you have [`uv`](https://github.com/astral-sh/uv) installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then install dependencies:

```bash
uv pip install -e .
```

> ✅ The `-e` installs the project in editable mode using `pyproject.toml`.

---

### 2. Run the App

You can run the app in either of the following ways:

**As a module**:
```bash
uv run python -m playwright_amazon
```

---

## 🧪 Running Tests

To run tests (if you add `pytest` or similar):

```bash
uv run pytest
```

---

## 🔧 Configuration

All config (if any) can go into `pyproject.toml` or a separate `config.py` file.

---

## 📜 License

[MIT](LICENSE)

---

## 🙋‍♀️ Contributing

Pull requests welcome! Please open an issue first to discuss what you’d like to change.

---

## 📍 Notes

- This project uses the modern [`src/`](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout) layout for clean package isolation.
- `uv` is a drop-in faster alternative to `pip`, `pip-tools`, and `virtualenv`, all in one.

---
