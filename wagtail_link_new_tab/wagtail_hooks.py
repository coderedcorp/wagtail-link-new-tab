from wagtail import hooks
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.whitelist import check_url
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineEntityElementHandler,
)
from wagtail.models import Page

from django.urls import path
from django.utils.translation import gettext

from draftjs_exporter.dom import DOM

from .chooser import ExternalLinkView
from .chooser import AnchorLinkView
from .chooser import EmailLinkView
from .chooser import PhoneLinkView


def link_entity(props):
    """
    <a linktype="page" id="1">internal page link</a>
    """
    id_ = props.get("id")
    link_props = {}

    if id_ is not None:
        link_props["linktype"] = "page"
        link_props["id"] = id_
    else:
        link_props["href"] = check_url(props.get("url"))

    external_ = props.get("open_in_new_tab", False)
    if external_:
        link_props["target"] = "_blank"

    return DOM.create_element("a", link_props, props["children"])


class LinkElementHandler(InlineEntityElementHandler):
    mutability = "MUTABLE"


class ExternalLinkElementHandler(LinkElementHandler):
    def get_attribute_data(self, attrs):
        return {
            "url": attrs["href"],
            "open_in_new_tab": attrs.get("target", "") == "_blank",
        }


class PageLinkElementHandler(LinkElementHandler):
    def get_attribute_data(self, attrs):
        try:
            page = Page.objects.get(id=attrs["id"]).specific
        except Page.DoesNotExist:
            # retain ID so that it's still identified as
            #  a page link (albeit a broken one)
            return {
                "id": int(attrs["id"]),
                "url": None,
                "parentId": None,
                "open_in_new_tab": attrs.get("target", "") == "_blank",
            }

        parent_page = page.get_parent()

        return {
            "id": page.id,
            "url": page.url,
            "parentId": parent_page.id if parent_page else None,
            "open_in_New_tab": attrs.get("target", "") == "_blank",
        }


@hooks.register("register_rich_text_features", order=10)
def register_core_features(features):
    features.register_editor_plugin(
        "draftail",
        "link",
        draftail_features.EntityFeature(
            {
                "type": "LINK",
                "icon": "link",
                "description": gettext("Link"),
                # We want to enforce constraints on which links can be pasted
                # into rich text. Keep only the attributes Wagtail needs.
                "attributes": ["url", "id", "parentId"],
                "allowlist": {
                    # Keep pasted links with http/https protocol, and
                    # not-pasted links (href = undefined).
                    "href": "^(http:|https:|undefined$)",
                },
            },
            js=[
                "wagtailadmin/js/page-chooser-modal.js",
                "js/modal-workflow.js",
            ],
        ),
    )

    features.register_converter_rule(
        "contentstate",
        "link",
        {
            "from_database_format": {
                "a[href]": ExternalLinkElementHandler("LINK"),
                'a[linktype="page"]': PageLinkElementHandler("LINK"),
            },
            "to_database_format": {"entity_decorators": {"LINK": link_entity}},
        },
    )


@hooks.register("register_admin_urls")
def register_custom_chooser_urls():
    return [
        path(
            "new_tab_external_link/",
            ExternalLinkView.as_view(),
            name="new_tab_external_link",
        ),
        path(
            "new_tab_anchor_link/",
            AnchorLinkView.as_view(),
            name="new_tab_anchor_link",
        ),
        path(
            "new_tab_email_link/",
            EmailLinkView.as_view(),
            name="new_tab_email_link",
        ),
        path(
            "new_tab_phone_link/",
            PhoneLinkView.as_view(),
            name="new_tab_phone_link",
        ),
    ]
