#!/usr/bin/env python3
"""Search official Godot online docs and print compact snippets."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser


BASE_URL = "https://docs.godotengine.org/en/{version}"
USER_AGENT = "godot-game-dev-skill/1.0"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.skip_depth = 0
        self.parts: list[str] = []
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "nav", "footer"}:
            self.skip_depth += 1
        if tag == "title":
            self._in_title = True
        if tag in {"p", "br", "li", "h1", "h2", "h3", "tr", "dt", "dd"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav", "footer"} and self.skip_depth:
            self.skip_depth -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = data.strip()
        if not text:
            return
        if self._in_title:
            self.title += text
        self.parts.append(text)

    def text(self) -> str:
        raw = " ".join(self.parts)
        raw = html.unescape(raw)
        raw = re.sub(r"[ \t]+", " ", raw)
        raw = re.sub(r"\n\s+", "\n", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return raw.strip()


def fetch(url: str, timeout: int, retries: int = 3) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset, errors="replace")
        except (urllib.error.URLError, TimeoutError) as error:
            last_error = error
            if attempt < retries - 1:
                time.sleep(0.75 * (attempt + 1))
    if last_error:
        raise last_error
    raise RuntimeError(f"Failed to fetch {url}")


def class_url(version: str, class_name: str) -> str:
    return f"{BASE_URL.format(version=version)}/classes/class_{class_name.lower()}.html"


def search_url(version: str, query: str) -> str:
    encoded = urllib.parse.urlencode({"q": query, "check_keywords": "yes", "area": "default"})
    return f"{BASE_URL.format(version=version)}/search.html?{encoded}"


def search_index_url(version: str) -> str:
    return f"{BASE_URL.format(version=version)}/searchindex.js"


def github_api_search_url(version: str, query: str, max_results: int) -> str:
    branch = "master" if version in {"latest", "master"} else version
    q = f"{query} repo:godotengine/godot-docs path:/"
    encoded = urllib.parse.urlencode({"q": q, "per_page": str(max_results)})
    return f"https://api.github.com/search/code?{encoded}", branch


def github_raw_url(branch: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/godotengine/godot-docs/{branch}/{path}"


def parse_search_index(page_js: str) -> dict:
    prefix = "Search.setIndex("
    if not page_js.startswith(prefix) or not page_js.endswith(")"):
        raise ValueError("Unexpected Sphinx search index format")
    return json.loads(page_js[len(prefix) : -1])


def as_doc_ids(value: object) -> list[int]:
    if value is None:
        return []
    if isinstance(value, int):
        return [value]
    if isinstance(value, list):
        ids: list[int] = []
        for item in value:
            if isinstance(item, int):
                ids.append(item)
            elif isinstance(item, list) and item and isinstance(item[0], int):
                ids.append(item[0])
        return ids
    return []


def lookup_term(index: dict, term: str, field: str) -> list[int]:
    table = index.get(field, {})
    direct = as_doc_ids(table.get(term))
    if direct:
        return direct
    # Sphinx often stores stemmed keys. Prefix matching is a useful fallback for
    # query words like "callable" -> "callabl".
    matches: list[int] = []
    for key, value in table.items():
        if term.startswith(key) or key.startswith(term):
            matches.extend(as_doc_ids(value))
    return matches


def docs_from_search_index(version: str, query: str, max_results: int, timeout: int) -> list[str]:
    index = parse_search_index(fetch(search_index_url(version), timeout))
    docnames: list[str] = index.get("docnames", [])
    titles: list[str] = index.get("titles", [])
    terms = [token.lower() for token in re.findall(r"[A-Za-z0-9_@.]+", query) if len(token) >= 2]
    ranked: dict[int, int] = {}

    for term in terms:
        for doc_id in lookup_term(index, term, "titleterms"):
            ranked[doc_id] = ranked.get(doc_id, 0) + 8
        for doc_id in lookup_term(index, term, "terms"):
            ranked[doc_id] = ranked.get(doc_id, 0) + 2

    lowered_query = query.lower()
    for doc_id, docname in enumerate(docnames):
        title = titles[doc_id] if doc_id < len(titles) else ""
        haystack = f"{docname} {title}".lower()
        if lowered_query and lowered_query in haystack:
            ranked[doc_id] = ranked.get(doc_id, 0) + 20
        for term in terms:
            if term in haystack:
                ranked[doc_id] = ranked.get(doc_id, 0) + 4

    base = BASE_URL.format(version=version) + "/"
    urls: list[str] = []
    for doc_id, _ in sorted(ranked.items(), key=lambda item: item[1], reverse=True):
        if 0 <= doc_id < len(docnames):
            urls.append(urllib.parse.urljoin(base, docnames[doc_id] + ".html"))
        if len(urls) >= max_results:
            break
    return urls


def extract_search_links(page_html: str, version: str, max_results: int) -> list[str]:
    links: list[str] = []
    seen_pages: set[str] = set()
    base = BASE_URL.format(version=version) + "/"
    for href in re.findall(r'href="([^"]+\.html(?:#[^"]+)?)"', page_html):
        if href.startswith(("http://", "https://")):
            url = href
        else:
            url = urllib.parse.urljoin(base + "search.html", href)
        if "/genindex.html" in url or "/search.html" in url:
            continue
        page_key = url.split("#", 1)[0]
        if page_key not in seen_pages:
            seen_pages.add(page_key)
            links.append(url)
        if len(links) >= max_results:
            break
    return links


def score(text: str, terms: list[str]) -> int:
    lowered = text.lower()
    total = 0
    for term in terms:
        if term in lowered:
            total += 10
        for token in term.split():
            if len(token) >= 3 and token in lowered:
                total += 1
    return total


def make_snippet(text: str, terms: list[str], context: int) -> str:
    lowered = text.lower()
    index = -1
    for term in terms:
        index = lowered.find(term)
        if index >= 0:
            break
    if index < 0:
        for term in terms:
            for token in term.split():
                if len(token) >= 3:
                    index = lowered.find(token)
                    if index >= 0:
                        break
            if index >= 0:
                break
    if index < 0:
        index = 0
    start = max(0, index - context)
    end = min(len(text), index + context)
    return text[start:end].strip()


def fetch_doc_snippet(url: str, terms: list[str], timeout: int, context: int) -> tuple[int, str]:
    page_html = fetch(url, timeout)
    extractor = TextExtractor()
    extractor.feed(page_html)
    text = extractor.text()
    title = extractor.title.strip() or url
    return score(text, terms), f"{title}\n{url}\n{make_snippet(text, terms, context)}"


def github_code_search(query: str, version: str, max_results: int, timeout: int) -> list[str]:
    api_url, branch = github_api_search_url(version, query, max_results)
    try:
        payload = json.loads(fetch(api_url, timeout))
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError):
        return []
    urls: list[str] = []
    for item in payload.get("items", [])[:max_results]:
        path = item.get("path")
        if path:
            urls.append(github_raw_url(branch, path))
    return urls


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="*", help="Search query")
    parser.add_argument("--class", dest="class_name", help="Open a class reference directly")
    parser.add_argument("--version", default="stable", help="Docs version: stable, latest, 4.6, 4.5, etc.")
    parser.add_argument("--max-results", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--context", type=int, default=500)
    parser.add_argument("--github-fallback", action="store_true", help="Use GitHub code search fallback if docs search returns nothing")
    args = parser.parse_args()

    terms = [term.lower() for term in args.query if term.strip()]
    query = " ".join(args.query).strip()

    urls: list[str] = []
    if args.class_name:
        urls.append(class_url(args.version, args.class_name))
        if not terms:
            terms = [args.class_name.lower()]
    if query:
        try:
            urls.extend(docs_from_search_index(args.version, query, args.max_results, args.timeout))
        except (urllib.error.URLError, ValueError, json.JSONDecodeError) as error:
            print(f"Search index failed, falling back to search page: {error}", file=sys.stderr)
            try:
                page_html = fetch(search_url(args.version, query), args.timeout)
                urls.extend(extract_search_links(page_html, args.version, args.max_results))
            except urllib.error.URLError as search_error:
                print(f"Docs search failed: {search_error}", file=sys.stderr)

    if not urls and args.github_fallback and query:
        urls.extend(github_code_search(query, args.version, args.max_results, args.timeout))

    if not urls:
        raise SystemExit("No online docs results. Try --class, --github-fallback, another --version, or local search.")

    seen: set[str] = set()
    results: list[tuple[int, str]] = []
    for url in urls:
        if url in seen:
            continue
        seen.add(url)
        try:
            result_score, output = fetch_doc_snippet(url, terms or [query.lower()], args.timeout, args.context)
        except urllib.error.HTTPError as error:
            output = f"HTTP {error.code}: {url}"
            result_score = 0
        except urllib.error.URLError as error:
            output = f"Fetch failed: {url}\n{error}"
            result_score = 0
        results.append((result_score, output))

    for index, (_, output) in enumerate(sorted(results, key=lambda item: item[0], reverse=True)[: args.max_results], 1):
        print(f"\n## Result {index}\n{output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
