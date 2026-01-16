from django.core.paginator import Paginator
from django.db.models import Q, F
from django.shortcuts import render, get_object_or_404
from django.utils.http import url_has_allowed_host_and_scheme

from .models import Product, Category, ProductView


def product_list(request):
    q = (request.GET.get("q") or "").strip()
    category_slug = (request.GET.get("category") or "").strip()
    sort = (request.GET.get("sort") or "new").strip()

    products = (
        Product.objects
        .select_related("category")
        .filter(is_active=True, category__is_active=True)
    )

    if q:
        products = products.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )

    if category_slug:
        products = products.filter(category__slug=category_slug)

    sort_map = {
        "new": "-created_at",
        "price_asc": "price_kzt",
        "price_desc": "-price_kzt",
        "popular": "-views_total",
    }
    products = products.order_by(sort_map.get(sort, "-created_at"))

    categories = Category.objects.filter(is_active=True).order_by("name")

    paginator = Paginator(products, 12)  # 12 карточек на страницу
    page_number = request.GET.get("page") or 1
    page_obj = paginator.get_page(page_number)

    ctx = {
        "categories": categories,
        "page_obj": page_obj,
        "q": q,
        "category_slug": category_slug,
        "sort": sort,
    }
    return render(request, "catalog/product_list.html", ctx)


def product_detail(request, slug: str):
    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        is_active=True,
        category__is_active=True,
    )

    # Учёт просмотров: увеличиваем счётчик + пишем событие
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key or ""

    Product.objects.filter(pk=product.pk).update(views_total=F("views_total") + 1)
    ProductView.objects.create(product=product, session_key=session_key)

    # Обновим объект в памяти (чтобы на странице показывалось актуальное число)
    product.refresh_from_db(fields=["views_total"])

    return render(request, "catalog/product_detail.html", {"product": product})
