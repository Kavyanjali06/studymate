import re
from datetime import date

from .data.articles import ARTICLES, ARTICLE_MAP
from .data.categories import CATEGORIES, CATEGORY_MAP, get_category

PRODUCTION_DOMAIN = "https://studymate-rho-rouge.vercel.app"


def get_all_articles():
    return list(ARTICLES)


def get_article(slug):
    return ARTICLE_MAP.get(slug)


def get_articles_by_category(category_slug):
    return [a for a in ARTICLES if a["category"] == category_slug]


def get_featured_article():
    for article in ARTICLES:
        if article.get("featured"):
            return article
    return ARTICLES[0] if ARTICLES else None


def get_popular_articles(limit=4):
    sorted_articles = sorted(ARTICLES, key=lambda a: a.get("reading_time_minutes", 0), reverse=True)
    return sorted_articles[:limit]


def get_related_articles(article, limit=3):
    related_slugs = article.get("related", [])
    related = [get_article(slug) for slug in related_slugs if get_article(slug)]
    if len(related) < limit:
        category_articles = [a for a in ARTICLES if a["category"] == article["category"] and a["slug"] != article["slug"]]
        for a in category_articles:
            if a not in related:
                related.append(a)
            if len(related) >= limit:
                break
    return related[:limit]


def get_prev_next_articles(article):
    index = next((i for i, a in enumerate(ARTICLES) if a["slug"] == article["slug"]), None)
    if index is None:
        return None, None
    prev_article = ARTICLES[index - 1] if index > 0 else None
    next_article = ARTICLES[index + 1] if index < len(ARTICLES) - 1 else None
    return prev_article, next_article


def search_articles(query):
    query = (query or "").strip().lower()
    if not query:
        return get_all_articles()
    results = []
    for article in ARTICLES:
        category = get_category(article["category"])
        category_name = category["name"].lower() if category else ""
        searchable = " ".join([
            article["title"].lower(),
            article["excerpt"].lower(),
            strip_html(article["content"]).lower(),
            category_name,
        ])
        if query in searchable:
            results.append(article)
    return results


def strip_html(html):
    return re.sub(r"<[^>]+>", " ", html)


def extract_headings(html):
    headings = []
    pattern = re.compile(r"<h([23])[^>]*>(.*?)</h\1>", re.IGNORECASE | re.DOTALL)
    for match in pattern.finditer(html):
        level = int(match.group(1))
        text = strip_html(match.group(2)).strip()
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        headings.append({"level": level, "text": text, "slug": slug})
    return headings


def add_heading_ids(html):
    def replacer(match):
        tag = match.group(1)
        attrs = match.group(2) or ""
        inner = match.group(3)
        text = strip_html(inner).strip()
        slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        if "id=" in attrs:
            return match.group(0)
        return f'<h{tag} id="{slug}"{attrs}>{inner}</h{tag}>'

    return re.sub(r"<h([23])([^>]*)>(.*?)</h\1>", replacer, html, flags=re.IGNORECASE | re.DOTALL)


def format_date(value):
    if isinstance(value, date):
        return value.strftime("%B %d, %Y")
    return str(value)
