from django.db import models


class Category(models.Model):
    name = models.CharField("Название", max_length=120, unique=True)
    slug = models.SlugField("Слаг (slug, латиницей)", max_length=140, unique=True)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Категория",
    )

    name = models.CharField("Название", max_length=200)
    slug = models.SlugField("Слаг (slug, латиницей)", max_length=220, unique=True)

    price_kzt = models.DecimalField("Цена (KZT)", max_digits=12, decimal_places=0)
    description = models.TextField("Описание", blank=True)

    image = models.ImageField("Изображение (файл)", upload_to="products/", blank=True, null=True)
    image_url = models.URLField("Ссылка на изображение (URL, опционально)", blank=True)

    is_active = models.BooleanField("Активен", default=True)
    views_total = models.PositiveIntegerField("Просмотров всего", default=0)

    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class ProductView(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="views",
        verbose_name="Товар",
    )
    viewed_at = models.DateTimeField("Дата просмотра", auto_now_add=True)
    session_key = models.CharField("Ключ сессии", max_length=40, blank=True)

    class Meta:
        verbose_name = "Просмотр товара"
        verbose_name_plural = "Просмотры товаров"
        indexes = [
            models.Index(fields=["viewed_at"]),
            models.Index(fields=["product", "viewed_at"]),
        ]

    def __str__(self):
        return f"{self.product_id} @ {self.viewed_at}"
