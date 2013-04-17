from Acquisition import aq_inner
from five import grok
from plone import api

from zope.interface import Interface
from zope.component import getMultiAdapter

from plone.app.layout.viewlets.interfaces import IPortalFooter

from kk.bannertool.banner import IBanner
from kk.bannertool.bannermanager import IBannerManager
from kk.bannertool.interfaces import IBannerTool


class BannerViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.layer(IBannerTool)
    grok.viewletmanager(IPortalFooter)
    grok.name('kk.bannertool.BannerViewlet')

    def update(self):
        self.available = len(self.banners()) > 0
        self.has_bm = len(self.bannermanager()) > 0

    def banners(self):
        banners = []
        for banner in self.banner_content():
            obj = banner.getObject()
            banners.append({
                'url': obj.absolute_url(),
                'image_tag': self.contruct_image_tag(obj),
                'text': obj.text.output,
                'banner_class': obj.position,
            })
        return banners

    def banner_content(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        items = catalog(object_provides=IBanner.__identifier__,
                        review_state='published',
                        sort_on='getObjPositionInParent')
        return items

    def bannermanager(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        bms = catalog(object_provides=IBannerManager.__identifier__,
                      review_state='published',
                      sort_on='getObjPositionInParent')
        if len(bms) > 0:
            return bms[0]

    def contruct_image_tag(self, obj):
        scales = getMultiAdapter((obj, self.request), name='images')
        scale = scales.scale('image', scale='preview')
        imageTag = None
        if scale is not None:
            imageTag = scale.tag()
        return imageTag
