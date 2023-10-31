from wagtail.admin.views.chooser import ExternalLinkView as BaseExternaLinkView
from wagtail.admin.views.chooser import EmailLinkView as BaseEmailLinkView
from wagtail.admin.views.chooser import AnchorLinkView as BaseAnchorLinkView
from wagtail.admin.views.chooser import PhoneLinkView as BasePhoneLinkView

from .forms import ExternalLinkChooserForm
from .forms import AnchorLinkChooserForm
from .forms import EmailLinkChooserForm
from .forms import PhoneLinkChooserForm


class NewTabMixin:
    def get_result_data(self):
        url_field_value = self.form.cleaned_data[self.link_url_field_name]
        return {
            "url": self.get_url_from_field_value(url_field_value),
            "title": (self.form.cleaned_data["link_text"].strip() or url_field_value),
            # If the user has explicitly entered /
            # edited something in the link_text field,
            # always use that text. If not, we should favour
            #  keeping the existing link/selection
            # text, where applicable.
            # (Normally this will match the link_text
            #  passed in the URL here anyhow,
            # but that won't account for non-text content such as images.)
            "prefer_this_title_as_link_text": ("link_text" in self.form.changed_data),
            "open_in_new_tab": self.form.cleaned_data.get("open_in_new_tab", False),
        }

    def get_initial_data(self):
        data = super().get_initial_data()
        data["open_in_new_tab"] = self.request.GET.get("open_in_new_tab", False)
        return data


class ExternalLinkView(NewTabMixin, BaseExternaLinkView):
    form_class = ExternalLinkChooserForm


class AnchorLinkView(NewTabMixin, BaseAnchorLinkView):
    form_class = AnchorLinkChooserForm


class EmailLinkView(NewTabMixin, BaseEmailLinkView):
    form_class = EmailLinkChooserForm


class PhoneLinkView(NewTabMixin, BasePhoneLinkView):
    form_class = PhoneLinkChooserForm
