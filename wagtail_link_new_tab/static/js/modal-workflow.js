class CustomLinkModalWorkflowSource extends window.draftail
  .LinkModalWorkflowSource {
  getChooserConfig(entity, selectedText) {
    let url = window.chooserUrls.pageChooser;
    const urlParams = {
      page_type: 'wagtailcore.page',
      allow_external_link: true,
      allow_email_link: true,
      allow_phone_link: true,
      allow_anchor_link: true,
      link_text: selectedText,
    };

    if (entity) {
      const data = entity.getData();

      if (data.id) {
        if (data.parentId !== null) {
          url = `${window.chooserUrls.pageChooser}${data.parentId}/`;
        } else {
          url = window.chooserUrls.pageChooser;
        }
      } else if (data.url.startsWith('mailto:')) {
        url = window.chooserUrls.emailLinkChooser;
        urlParams.link_url = data.url.replace('mailto:', '');
      } else if (data.url.startsWith('tel:')) {
        url = window.chooserUrls.phoneLinkChooser;
        urlParams.link_url = data.url.replace('tel:', '');
      } else if (data.url.startsWith('#')) {
        url = window.chooserUrls.anchorLinkChooser;
        urlParams.link_url = data.url.replace('#', '');
      } else {
        url = window.chooserUrls.externalLinkChooser;
        urlParams.link_url = data.url;
      }
      if (data.open_in_new_tab) {
        urlParams.open_in_new_tab = true;
      }
    }

    return {
      url,
      urlParams,
      onload: window.PAGE_CHOOSER_MODAL_ONLOAD_HANDLERS,
      responses: {
        pageChosen: this.onChosen,
      },
    };
  }

  filterEntityData(data) {
    if (data.id) {
      return {
        url: data.url,
        id: data.id,
        parentId: data.parentId,
        open_in_new_tab: data.open_in_new_tab ?? false,
      };
    }

    return {
      url: data.url,
      open_in_new_tab: data.open_in_new_tab ?? false,
    };
  }
}

const Plugins = window.draftail.registerPlugin({ type: null });

let LinkPlugin = Plugins['LINK'];
LinkPlugin.source = CustomLinkModalWorkflowSource;

window.draftail.registerPlugin(LinkPlugin, 'entityTypes');
