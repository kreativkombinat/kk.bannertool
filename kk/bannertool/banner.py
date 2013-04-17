from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage

from plone.app.textfield import RichText

from kk.bannertool import MessageFactory as _


positions = SimpleVocabulary(
    [SimpleTerm(value=u'caption-top-left', title=_(u'Top Left')),
     SimpleTerm(value=u'caption-top-right', title=_(u'Top Right')),
     SimpleTerm(value=u'caption-bottom-left', title=_(u'Bottom Left')),
     SimpleTerm(value=u"caption-bottom-right", title=_(u"Bottom Right"))])


class IBanner(form.Schema, IImageScaleTraversable):
    """
    A singel banner containing images and captions
    """
    image = NamedBlobImage(
        title=_(u"Banner Image"),
        required=True,
    )
    text = RichText(
        title=_(u"Formated Banner Text"),
        description=_(u"Optional banner text with html formatting. If you "
                      u"leave this field empty the description will be used "
                      u"instead."),
        required=False,
    )
    position = schema.Choice(
        title=_(u"Teaser Text Position"),
        vocabulary=positions,
        required=False,
        default=u"caption-bottom-left",
    )


class Banner(dexterity.Container):
    grok.implements(IBanner)


class View(grok.View):
    grok.context(IBanner)
    grok.require('zope2.View')
    grok.name('view')
