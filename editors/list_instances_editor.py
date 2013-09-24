""" Defines the list instance editor factory for the traits user interface
toolkits..
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from __future__ import absolute_import

from traits.api import (HasTraits, BaseTraitHandler, Range, Any, Int, Instance,
        Property, Bool, Callable, Enum, PrototypedFrom)

# CIRCULAR IMPORT FIXME: Importing from the source rather than traits.ui.api
# to avoid circular imports, as this EditorFactory will be part of
# traits.ui.api as well.
from ..view import View

from ..item import Item

from ..ui_traits import style_trait

from ..editor_factory import EditorFactory

from ..toolkit import toolkit_object

#-------------------------------------------------------------------------------
#  Trait definitions:
#-------------------------------------------------------------------------------

# Trait whose value is a BaseTraitHandler object
handler_trait = Instance( BaseTraitHandler )

# The visible number of rows displayed
rows_trait = Range( 1, 50, 5,
                    desc = 'the number of list rows to display' )

# The visible number of columns displayed
columns_trait = Range( 1, 10, 1,
                    desc = 'the number of list columns to display' )

editor_trait = Instance( EditorFactory )

#-------------------------------------------------------------------------------
#  'ToolkitEditorFactory' class:
#-------------------------------------------------------------------------------

class ToolkitEditorFactory ( EditorFactory ):
    """ Editor factory for list editors.
    """

    #---------------------------------------------------------------------------
    #  Trait definitions:
    #---------------------------------------------------------------------------

    # The editor to use for each list item:
    editor = editor_trait

    # Can the list be reorganized, or have items added and deleted.
    mutable = Bool(True)
    
    # Can items be added
    addable = Bool(True)
    
    #Can items be deleted
    deletable = Bool(True)

    #Factory function to call when a new item should be added to the list
    item_factory = Callable

    # The style of editor to use for each item:
    style = style_trait

    # The trait handler for each list item:
    trait_handler = handler_trait

    # The number of list rows to display:
    rows = rows_trait

    # The number of list columns to create:
    columns = columns_trait

    # The type of UI to construct ('panel', 'subpanel', etc)
    ui_kind = Enum( 'subpanel', 'panel' )

    # A factory function that can be used to define that actual object to be
    # edited (i.e. view_object = factory( object )):
    factory = Callable

    #---------------------------------------------------------------------------
    #  Traits view definition:
    #---------------------------------------------------------------------------

    traits_view = View( [ [ '|[Style]' ],
                          [ Item( 'rows'),
                            '|[Number of list rows to display]<>' ] ] )

    #---------------------------------------------------------------------------
    #  'Editor' factory methods:
    #---------------------------------------------------------------------------

    def _get_custom_editor_class ( self ):
        return toolkit_object('list_instances_editor:CustomEditor')

#-------------------------------------------------------------------------------
#  'ListItemProxy' class:
#   This class is used to update the list editors when the object changes
#   external to the editor.
#-------------------------------------------------------------------------------

class ListItemProxy ( HasTraits ):

    # The list proxy:
    list = Property

    # The item proxies index into the original list:
    index = Int

    # Delegate all other traits to the original object:
    _ = PrototypedFrom( '_zzz_object' )

    # Define all of the private internal use values (the funny names are an
    # attempt to avoid name collisions with delegated trait names):
    _zzz_inited = Any
    _zzz_object = Any
    _zzz_name   = Any

    def __init__ ( self, object, name, index, trait, value ):
        super( ListItemProxy, self ).__init__()

        self._zzz_inited = False
        self._zzz_object = object
        self._zzz_name   = name
        self.index       = index

        if trait is not None:
            self.add_trait( 'value', trait )
            self.value = value

        self._zzz_inited = (self.index < len( self.list ))

    def _get_list ( self ):
        return getattr( self._zzz_object, self._zzz_name )

    def _value_changed ( self, old_value, new_value ):
        if self._zzz_inited:
            self.list[ self.index ] = new_value


# Define the ListEditor class
ListInstanceEditor = ToolkitEditorFactory

### EOF ---------------------------------------------------------------------
