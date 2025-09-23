from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.fields import RichTextField
from wagtail.models import Page, Orderable
from wagtail.snippets.models import register_snippet


class SimplePage(Page):
    navigation_title = models.CharField(max_length=255, blank=True, null=True,
                                        help_text="Short title for navigation menu if different from main title.")
    body = RichTextField(blank=True)

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


class ImagePage(Page):
    navigation_title = models.CharField(max_length=255, blank=True, null=True,
                                        help_text="Short title for navigation menu if different from main title.")
    intro = RichTextField(blank=True)

    show_as_top_level = models.BooleanField(
        default=False,
        help_text="Show this page in the top menu next to 'om'."
    )
    show_in_home_submenu = models.BooleanField(
        default=False,
        help_text="Show this page in the submenu under the 'om' dropdown."
    )

    content_panels = Page.content_panels + ["navigation_title", "intro",
                                            InlinePanel("sections",
                                                        label="Sections"),]
    promote_panels = Page.promote_panels + [
        "show_as_top_level", "show_in_home_submenu"]


class ImagePageSection(ClusterableModel, Orderable):
    """A section on the page with a heading and ordered image cards."""
    page = ParentalKey(
        "ImagePage", on_delete=models.CASCADE, related_name="sections"
    )
    heading = models.CharField(max_length=255)

    panels = [
        FieldPanel("heading"),
        InlinePanel("cards", label="Cards"),
    ]


class ImagePageSectionCard(Orderable):
    """A single card inside a section, pointing to an ImageCard snippet."""
    section = ParentalKey(
        "ImagePageSection", on_delete=models.CASCADE, related_name="cards"
    )
    image_card = models.ForeignKey("ImageCard", on_delete=models.PROTECT,
                                  related_name="+")

    panels = [FieldPanel("image_card")]


@register_snippet
class ImageCard(models.Model):
    """Reusable snippet with an image and downloadable files."""
    title = models.CharField(max_length=255)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=False, on_delete=models.SET_NULL, related_name="+"
    )
    image_download = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    pdf_download = models.ForeignKey(
        "wagtaildocs.Document",
        null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("image"),
        MultiFieldPanel(
            [
                FieldPanel("image_download"),
                FieldPanel("pdf_download"),
            ],
            heading="Download files (optional)",
        ),
    ]

    def __str__(self):
        return self.title


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
        InlinePanel('form_fields', label="Form fields", max_num=6),
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
