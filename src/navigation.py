"""Two compact category entry points and optional cross-category search.

The query itself encodes the active category; no extra process or persistent
UI state is needed. This leaves existing Jinja variable handling unchanged.
"""

PHRASES_PREFIX = "常用短语/"
TEMPLATES_PREFIX = "变量模板/"
MAX_RESULTS = 5


def parse_query(argument):
    """Return (mode, term): home, phrases, templates or all."""
    text = (argument or "").strip()
    if not text:
        return ("home", "")
    if text.startswith(PHRASES_PREFIX):
        return ("phrases", text[len(PHRASES_PREFIX):].strip())
    if text.startswith(TEMPLATES_PREFIX):
        return ("templates", text[len(TEMPLATES_PREFIX):].strip())
    return ("all", text)


def select_results(items, query, score_function, limit=MAX_RESULTS):
    """Filter and sort matches, keeping original order for category browsing."""
    try:
        max_results = max(1, min(MAX_RESULTS, int(limit)))
    except (ValueError, TypeError):
        max_results = MAX_RESULTS

    if not query:
        return list(items)[:max_results]

    scored = []
    for item in items:
        score = score_function(query, item.name)
        if score > 0:
            scored.append((score, item))
    # Python stable sort preserves order on equal scores.
    scored.sort(key=lambda result: result[0], reverse=True)
    return [item for _, item in scored[:max_results]]
