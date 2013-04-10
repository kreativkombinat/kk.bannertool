from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from kk.bannertool import MessageFactory as _


# Interface class; used to define content-type schema.

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


class Banner(dexterity.Container):
    grok.implements(IBanner)


class View(grok.View):
    grok.context(IBanner)
    grok.require('zope2.View')
    grok.name('view')
