from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductView


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    search_fields = ("name", "slug")
    list_filter = ("is_active",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price_kzt", "is_active", "views_total", "updated_at", "image_preview")
    list_filter = ("is_active", "category")
    search_fields = ("name", "slug", "description")
    ordering = ("-updated_at",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.image.url)
        if obj.image_url:
            return format_html('<img src="{}" style="height:40px;border-radius:6px;" />', obj.image_url)
        return "—"

    image_preview.short_description = "Фото"


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ("product", "viewed_at", "session_key")
    list_filter = ("viewed_at",)
    search_fields = ("product__name", "session_key")
