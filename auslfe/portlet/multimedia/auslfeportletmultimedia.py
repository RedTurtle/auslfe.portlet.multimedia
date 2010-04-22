from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from auslfe.portlet.multimedia import AuslfePortletMultimediaMessageFactory as _

from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from Products.ATContentTypes.interface import IATTopic
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget


class IAuslfePortletMultimedia(IPortletDataProvider):
    """A portlet"""

    portlet_title = schema.TextLine(title=_(u"Titolo del riquadro"),
                               description = _(u"Inserisci il titolo del riquadro."),
                               required = True)
    
    portlet_text = schema.Text(title=_(u"Testo del riquadro"),
                               description=_(u"Inserire il testo da visualizzare nell'intestazione del riquadro."),
                               required=False)
    
    target_collection = schema.Choice(title=_(u"Archivio fotografico"),
                                      description=_(u"Seleziona la collezione che fornisce le foto da visualizzare."),
                                      required=False,
                                      source=SearchableTextSourceBinder({'object_provides' : IATTopic.__identifier__},
                                                                        default_query='path:'))
    
    target_collection_title = schema.TextLine(title=_(u"Testo del link all'archivio fotografico"),
                                              description=_(u"Puoi personalizzare il testo del link all'archivio (se vuoto sara\'  'Tutte le foto')."),
                                              required=False)
    
    portlet_class = schema.TextLine(title=_(u"Classe CSS"),
                                   description=_(u"In questo campo puoi aggiungere una classe CSS."),
                                   required=False)

class Assignment(base.Assignment):
    """Portlet assignment"""

    implements(IAuslfePortletMultimedia)
    
    def __init__(self,portlet_title='',portlet_text='',target_collection=None,target_collection_title='',portlet_class=''):
        """
        """        
        base.Assignment.__init__(self)
        self.portlet_title = portlet_title
        self.portlet_text = portlet_text
        self.target_collection = target_collection
        self.target_collection_title = target_collection_title
        self.portlet_class = portlet_class

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Riquadro Multimedia"
        #target_collection = str(self.data.target_collection[1:])
        #return "Riquadro Multimedia: %s" % target_collection

class Renderer(base.Renderer):
    """Portlet renderer"""

    render = ViewPageTemplateFile('auslfeportletmultimedia.pt')


class AddForm(base.AddForm):
    """Portlet add form"""
    form_fields = form.Fields(IAuslfePortletMultimedia)
    form_fields['portlet_text'].custom_widget = WYSIWYGWidget
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form"""
    form_fields = form.Fields(IAuslfePortletMultimedia)
    form_fields['portlet_text'].custom_widget = WYSIWYGWidget
    form_fields['target_collection'].custom_widget = UberSelectionWidget
