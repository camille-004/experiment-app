import re

from django import template
from django.utils.safestring import SafeString, mark_safe

register = template.Library()


@register.filter
def exclude_file_input_text(value: str | SafeString) -> str | SafeString:
    if isinstance(value, str):
        cleaned_value = re.sub(
            r"Currently:.*?<br>\s*Change:", "Change:", value, flags=re.DOTALL
        )
        return mark_safe(cleaned_value)
    return value
