# -*- coding: utf-8 -*-
"""
    apps.books.models
    ~~~~~~~~~~~~~~

    books models
    
    :copyright: (c) 2012 by arruda.
"""
from decimal import  Decimal
import datetime

from django.db import models

from django.utils.translation import ugettext_lazy as _

from model_utils import Choices

from utils.abs_models import Abs_Named_Model, Abs_UniqueNamed_Model


class Genre(Abs_UniqueNamed_Model):
    "define a genre, like: action, romance, etc.."
    
    class Meta:
        app_label = 'books'
        ordering = ['name',]
        
        
class Book(Abs_Named_Model):
    "a book. simple as that"
    
    
    author = models.ForeignKey('authors.Author',related_name='books')
    publisher = models.ForeignKey('publishers.Publisher',related_name='books')
    
    synopsis = models.TextField(_('Synopsis'), null=True,blank=True)
    genres = models.ManyToManyField(Genre)
    
    release_date =  models.DateField(_("Release Date"), default=datetime.date.today, null=True, blank=True)
    
    
    def just_released(self):
        "returns True if the release_date - this date is less then one year"
        release_time=datetime.timedelta(days=365)
        return datetime.date.today() - self.release_date < release_time
    
    just_released.short_description = 'Just Released?'
    
    class Meta:
        app_label = 'books'
        ordering = ['name',]
        unique_together = (('name','author' ),)
    
        
class UserBook(models.Model):
    "Relation between user and book"
    
    DESIRE_CHOICES = Choices(
                             (1,'curious',_("1 - Curious About")),
                             (2,'collection',_("2 - Complete Collection")),
                             (3,'survive',_("3 - Can Survive Without It")),
                             (4,'wait',_("4 - Can Wait a Little Longer")),
                             (5,'now',_("5 - I NEED THIS... NOW!!!")),
                     )
    
    user = models.ForeignKey('auth.User',related_name='books')
    book = models.ForeignKey(Book,related_name='users')
    
    desired = models.PositiveSmallIntegerField(_("Desired"), choices=DESIRE_CHOICES, default=DESIRE_CHOICES.curious)
    
    #purchase data
    purchase_store = models.ForeignKey('stores.Store',related_name='books',null=True,blank=True)
    purchased       = models.BooleanField(_("Purchased?"),default=False)
    purchase_value = models.DecimalField(_("Purchase Value"),max_digits=10, decimal_places=2, null=True, blank=True)
    purchase_date =  models.DateField(_("Purchase Date"),  null=True, blank=True)#, default=datetime.date.today,)
    
    class Meta:
        app_label = 'books'
        
    @property
    def desired_text(self):
        "return the correct self.desired text"
        return self.DESIRE_CHOICES[self.desired-1][1].__unicode__()
        
    def save(self, *args, **kwargs):
        """
        if has any purchased information, then mark as purchased
        """
        #if has a purchase value or date then mark as purchased
        if self.purchase_value or self.purchase_date or self.purchase_store:
            self.purchased = True
        
        super(UserBook, self).save(*args, **kwargs)
        
        