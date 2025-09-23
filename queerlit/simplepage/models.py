from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class SimplePage(Page):
    navigation_title = models.CharField(max_length=255, blank=True, null=True,
                                        help_text="Short title for navigation menu if different from main title.")
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + ["body"]

    show_as_top_level = models.BooleanField(
        default=False,
        help_text="Show this page in the top menu next to 'om'."
    )
    show_in_home_submenu = models.BooleanField(
        default=False,
        help_text="Show this page in the submenu under the 'om' dropdown."
    )

    content_panels = Page.content_panels + ["navigation_title", "body"]
    promote_panels = Page.promote_panels + [
        "show_as_top_level", "show_in_home_submenu"]


class FormField(AbstractFormField):
    page = ParentalKey('FormPage',
                       on_delete=models.CASCADE, related_name='form_fields')


class FormPage(AbstractEmailForm):
    navigation_title = models.CharField(max_length=255, blank=True, null=True,
                                        help_text="Short title for navigation menu if different from main title.")
    intro = RichTextField(blank=True, features=['h2', 'h3', 'bold', 'italic',
                                                'link'])
    thank_you_text = RichTextField(blank=True, features=['h2', 'h3', 'bold',
                                                         'italic', 'link'])

    show_as_top_level = models.BooleanField(
        default=False,
        help_text="Show this page in the top menu next to 'om'."
    )
    show_in_home_submenu = models.BooleanField(
        default=False,
        help_text="Show this page in the submenu under the 'om' dropdown."
    )

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('navigation_title'),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields", max_num=4),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', read_only=True),
                FieldPanel('to_address'),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

    promote_panels = Page.promote_panels + [
        "show_as_top_level", "show_in_home_submenu"]
