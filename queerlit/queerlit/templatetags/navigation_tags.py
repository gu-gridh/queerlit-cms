from django import template
from django.db.models import Q
from wagtail.models import Site

register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return Site.find_for_request(context["request"]).root_page


@register.simple_tag(takes_context=True)
def get_current_language(context):
    request = context.get("request")
    return getattr(request, "LANGUAGE_CODE", None) or "sv"


@register.simple_tag(takes_context=True)
def other_locale_translation(context, page):
    """
    Return the live translation of `page` in the OTHER language (sv<->en),
    deciding "current" from request.LANGUAGE_CODE (not from page.locale).
    """
    current = get_current_language(context)
    target_code = "sv" if str(current).startswith("en") else "en"

    # Include self so we can safely exclude by pk
    qs = (
        page.get_translations(inclusive=True)
            .live()
            .filter(locale__language_code=target_code)
    )
    return qs.exclude(pk=page.pk).first() or qs.first()


@register.inclusion_tag("navigation.html", takes_context=True)
def navigation(context):
    request = context["request"]
    page = Site.find_for_request(request).root_page.specific

    page_children = (
        page.get_children()
        .live()
        .specific()
        .filter(Q(simplepage__show_in_home_submenu=True)
                | Q(formpage__show_in_home_submenu=True)
                | Q(imagepage__show_in_home_submenu=True)).specific()
    )

    top_level = (
        page.get_children()
        .live()
        .filter(Q(simplepage__show_as_top_level=True)
                | Q(formpage__show_as_top_level=True)).specific()
    )

    is_top_level = any(page.url == request.path for page in top_level)
    if is_top_level:
        parent_url = ""
    else:
        parent_url = request.path.split("/")[1]

    return {
        "request": request,
        "page": page,
        "page_children": page_children,
        "parent_url": parent_url,
        "top_level": top_level,
    }
