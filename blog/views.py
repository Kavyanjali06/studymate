from django.http import Http404
from django.shortcuts import render

from .data.categories import CATEGORIES, get_category
from .utils import (
    PRODUCTION_DOMAIN,
    add_heading_ids,
    extract_headings,
    format_date,
    get_all_articles,
    get_article,
    get_articles_by_category,
    get_featured_article,
    get_popular_articles,
    get_prev_next_articles,
    get_related_articles,
    search_articles,
)


def _base_context(request):
    return {
        "production_domain": PRODUCTION_DOMAIN,
        "canonical_url": request.build_absolute_uri(request.path),
    }


def post_list(request):
    search_query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()

    if search_query:
        posts = search_articles(search_query)
    elif category_slug:
        posts = get_articles_by_category(category_slug)
    else:
        posts = get_all_articles()

    featured = get_featured_article() if not search_query and not category_slug else None
    if featured and featured in posts:
        posts = [p for p in posts if p["slug"] != featured["slug"]]

    popular = get_popular_articles(limit=4)

    context = {
        **_base_context(request),
        "posts": posts,
        "featured": featured,
        "popular": popular,
        "categories": CATEGORIES,
        "selected_category": category_slug,
        "search_query": search_query,
        "page_title": "Study Smarter, Not Harder. | StudyMate Blog",
        "meta_description": "Practical guides to help you plan better, stay focused, and achieve your academic goals. Study tips, time management, exam prep, and more.",
    }
    return render(request, "blog/post_list.html", context)


def post_detail(request, slug):
    article = get_article(slug)
    if not article:
        raise Http404("Article not found")

    article = dict(article)
    article["content"] = add_heading_ids(article["content"])

    category = get_category(article["category"])
    headings = extract_headings(article["content"])
    related = get_related_articles(article, limit=3)
    prev_article, next_article = get_prev_next_articles(article)

    context = {
        **_base_context(request),
        "post": article,
        "category": category,
        "headings": headings,
        "related_posts": related,
        "prev_post": prev_article,
        "next_post": next_article,
        "format_date": format_date,
        "page_title": f"{article['title']} | StudyMate Blog",
        "meta_description": article["excerpt"],
    }
    return render(request, "blog/post_detail.html", context)
