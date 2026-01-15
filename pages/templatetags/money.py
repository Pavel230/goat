from decimal import Decimal, InvalidOperation
from django import template
from django.conf import settings

register = template.Library()

def _fmt_int(n: Decimal) -> str:
    return f"{int(n):,}".replace(",", " ")

@register.simple_tag(takes_context=True)
def money(context, amount_kzt):
    try:
        amount = Decimal(str(amount_kzt))
    except (InvalidOperation, TypeError):
        amount = Decimal("0")

    request = context.get("request")
    currency = "KZT"
    if request and hasattr(request, "session"):
        currency = request.session.get("currency", "KZT")

    if currency == "USD":
        rate = Decimal(str(getattr(settings, "USD_RATE", 500)))
        usd = (amount / rate) if rate else Decimal("0")
        return f"${usd:.2f}"
    return f"{_fmt_int(amount)} ₸"
