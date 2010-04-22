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
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
import random


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
    
    random = schema.Bool(title=_(u"Seleziona elementi a caso"),
                         description=_(u"Se abilitato, gli elementi verranno estratti dalla collezione in ordine casuale,"
                                        " invece che nell'ordine stabilito dalla collezione stessa."),
                         required=False,
                         default=True)
    
    portlet_class = schema.TextLine(title=_(u"Classe CSS"),
                                   description=_(u"In questo campo puoi aggiungere una classe CSS."),
                                   required=False)

class Assignment(base.Assignment):
    """Portlet assignment"""

    implements(IAuslfePortletMultimedia)
    
    def __init__(self,portlet_title='',portlet_text='',target_collection=None,target_collection_title='',random=True,portlet_class=''):
        """
        """        
        base.Assignment.__init__(self)
        self.portlet_title = portlet_title
        self.portlet_text = portlet_text
        self.target_collection = target_collection
        self.target_collection_title = target_collection_title
        self.random = random
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
    
    def getPortletClass(self):
        if self.data.portlet_class:
            return self.data.portlet_class
        else:
            return ""
    
    @memoize
    def targetCollection(self):
        """Get the collection the portlet is pointing to"""
        
        target_collection = self.data.target_collection
        if not target_collection:
            return None

        if target_collection.startswith('/'):
            target_collection = target_collection[1:]
        
        if not target_collection:
            return None

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        return portal.restrictedTraverse(target_collection, default=None)
    
    def getTargetCollectionPath(self):
        """Restituisce l'url della collezione che fornisce le foto da visualizzare"""
        
        collection = self.targetCollection()
        if collection is None:
            return None
        else:
            return collection.absolute_url()
        
    def results(self):
        """Get the actual result brains from the collection"""
        if self.data.random:
            return self.randomResults()
        else:
            return self.standardResults()
        
    @memoize
    def standardResults(self):
        results = []
        collection = self.targetCollection()
        if collection is not None:
            results = collection.queryCatalog()
        return results
        
    def randomResults(self):
        results = []
        collection = self.targetCollection()
        if collection is not None:
            results = collection.queryCatalog(sort_on=None)
            random.shuffle(results)
        return results
    

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
