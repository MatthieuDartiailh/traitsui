# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 18:19:47 2013

@author: Matthieu
"""
#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from __future__ import absolute_import

from traits.api import List, Callable, Tuple

from ..editor_factory import EditorFactory


#-------------------------------------------------------------------------------
#  'ToolkitEditorFactory' class:
#-------------------------------------------------------------------------------

class LineCompleterEditor ( EditorFactory ):
    """ Editor factory for text editors.
    """

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    entries = List

    entries_updater = Callable

    delimiters = Tuple(('{','}'))


