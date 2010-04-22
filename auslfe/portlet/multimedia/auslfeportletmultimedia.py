from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

#from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

#from auslfe.portlet.multimedia import AuslfePortletMultimediaMessageFactory as _


class IAuslfePortletMultimedia(IPortletDataProvider):
    """A portlet"""
    

class Assignment(base.Assignment):
    """Portlet assignment"""

    implements(IAuslfePortletMultimedia)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Auslfe Portlet Multimedia"


class Renderer(base.Renderer):
    """Portlet renderer"""

    render = ViewPageTemplateFile('auslfeportletmultimedia.pt')


class AddForm(base.AddForm):
    """Portlet add form"""
    form_fields = form.Fields(IAuslfePortletMultimedia)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form"""
    form_fields = form.Fields(IAuslfePortletMultimedia)
