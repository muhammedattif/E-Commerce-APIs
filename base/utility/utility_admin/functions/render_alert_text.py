# Django Imports
from django.utils.safestring import mark_safe


def render_alert(message, tag="small", color="orange"):
    html_body = f'<{tag} style="color:{color}">{message}</{tag}>'
    return mark_safe(html_body)
