from django.utils.translation import gettext_lazy as _

from django import forms
from wagtail.admin.forms.choosers import URLOrAbsolutePathField


class ExternalLinkChooserForm(forms.Form):
    url = URLOrAbsolutePathField(required=True, label=_("URL"))
    link_text = forms.CharField(required=False)
    open_in_new_tab = forms.BooleanField(required=False)


class AnchorLinkChooserForm(forms.Form):
    url = forms.CharField(required=True, label="#")
    link_text = forms.CharField(required=False)
    open_in_new_tab = forms.BooleanField(required=False)


class EmailLinkChooserForm(forms.Form):
    email_address = forms.EmailField(required=True)
    link_text = forms.CharField(required=False)
    open_in_new_tab = forms.BooleanField(required=False)


class PhoneLinkChooserForm(forms.Form):
    phone_number = forms.CharField(required=True)
    link_text = forms.CharField(required=False)
    open_in_new_tab = forms.BooleanField(required=False)
