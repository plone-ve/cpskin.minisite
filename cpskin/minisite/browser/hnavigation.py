# -*- coding: utf-8 -*-
from Acquisition import aq_base, aq_parent, aq_inner
from Products.Five.browser import BrowserView

from plone import api

from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import noLongerProvides

from cpskin.locales import CPSkinMessageFactory as _
from cpskin.minisite.browser.interfaces import (IHNavigationActivated,
                                                IHNavigationActivationView
                                                )
from cpskin.minisite.minisite import Minisite


def get_minisite_root(context, request):
    minisite = request.get('cpskin_minisite', None)
    obj = context
    portal = api.portal.get()
    while (not minisite.search_path == "/".join(obj.getPhysicalPath()) and
            aq_base(obj) is not aq_base(portal)):
        parent = aq_parent(aq_inner(obj))
        if parent is None:
            return obj
        obj = parent
    return obj


class MSHorizontalNavigation(BrowserView):
    implements(IHNavigationActivationView)
    """
    Horizontal navigation activation helper view
    """

    @property
    def is_in_minisite_mode(self):
        minisite = self.request.get('cpskin_minisite', None)
        if not isinstance(minisite, Minisite):
            return
        if minisite.is_in_minisite_mode:
            return True
        else:
            return False

    @property
    def can_enable_hnavigation(self):
        context = self.context
        minisite_root = get_minisite_root(context, self.request)
        return self.is_in_minisite_mode and not (IHNavigationActivated.providedBy(minisite_root))

    @property
    def can_disable_hnavigation(self):
        context = self.context
        minisite_root = get_minisite_root(context, self.request)
        return self.is_in_minisite_mode and (IHNavigationActivated.providedBy(minisite_root))


def _redirect(self, msg=''):
    if self.request:
        if msg:
            api.portal.show_message(message=msg,
                                    request=self.request,
                                    type='info')

        self.request.response.redirect(self.context.absolute_url())
    return msg


class MSHorizontalNavigationEnable(BrowserView):
    """
    Horizontal navigation activation helper view
    """

    def __init__(self, context, request):
        super(MSHorizontalNavigationEnable, self).__init__(context, request)
        alsoProvides(get_minisite_root(context, request), IHNavigationActivated)
        _redirect(self, msg=_(u'Minisite horizontal Navigation enabled on content'))


class MSHorizontalNavigationDisable(BrowserView):
    """
    Horizontal navigation activation helper view
    """

    def __init__(self, context, request):
        super(MSHorizontalNavigationDisable, self).__init__(context, request)
        noLongerProvides(get_minisite_root(context, request), IHNavigationActivated)
        _redirect(self, msg=_(u'Minisite horizontal Navigation disabled on content'))
