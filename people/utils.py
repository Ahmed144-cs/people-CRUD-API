from datetime import datetime, date


# =========================
# Pagination
# =========================
def paginate_queryset(queryset, page: int, page_size: int = 20):
    page_size = min(max(1, page_size), 100)

    total_items = queryset.count()
    total_pages = (total_items + page_size - 1) // page_size

    page = max(1, min(page, total_pages if total_pages > 0 else 1))

    start = (page - 1) * page_size
    end = start + page_size

    items = queryset[start:end]

    return {
        "items": list(items.values()),
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        "next_page": page + 1 if page < total_pages else None,
        "prev_page": page - 1 if page > 1 else None,
    }


# =========================
# Calculate Age
# =========================
def calculate_age(birth_date: date) -> int:
    today = date.today()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


# =========================
# Parse Date
# =========================
def parse_date(date_str: str) -> date:
    return datetime.fromisoformat(date_str).date()