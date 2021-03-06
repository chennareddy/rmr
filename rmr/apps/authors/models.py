# -*- coding: utf-8 -*-
"""
    apps.authors.models
    ~~~~~~~~~~~~~~

    authors models
    
    :copyright: (c) 2012 by arruda.
"""

from utils.abs_models import Abs_UniqueNamed_Model, Abs_UserConected_Model

class Author(Abs_UniqueNamed_Model):
    "a book author"
    
        
    class Meta:
        app_label = 'authors'
        ordering = ['name',]