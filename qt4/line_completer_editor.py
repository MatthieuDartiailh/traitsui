# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 18:04:21 2013

@author: Matthieu
"""

""" Defines the various text editors for the PyQt user interface toolkit.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from pyface.qt import QtCore, QtGui

from traits.api import TraitError

from .editor import Editor

class CompleterLineEdit(QtGui.QLineEdit):
    """
    """
    completionNeeded = QtCore.Signal(str)

    def __init__(self, str_value, delimiters, entries, entries_updater):

        self.delimiters = delimiters

        super(CompleterLineEdit, self).__init__(str_value)
        self.textChanged[str].connect(self.text_changed)
        self.completer = QtGui.QCompleter(self)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setModel(QtGui.QStringListModel(entries,self.completer))

        self.completionNeeded.connect(self.completer.complete)
        self.completer.activated[str].connect(self.complete_text)
        self.completer.setWidget(self)

        self._upddate_entries = True
        self.editingFinished.connect(self.on_editing_finished)
        self.entries_updater = entries_updater

    def text_changed(self, text):
        """
        """
        if self._upddate_entries and self.entries_updater:
            entries = self.entries_updater()
            self.completer.setModel(
                                QtGui.QStringListModel(entries,self.completer)
                                   )
            self._upddate_entries = False

        all_text = unicode(text)
        text = all_text[:self.cursorPosition()]
        split = text.split(self.delimiters[0])
        prefix = split[-1].strip()

        if len(split) > 0:
            self.completer.setCompletionPrefix(prefix)
            self.completionNeeded.emit(prefix)

        self.string = text

    def complete_text(self, text):
        """
        """
        cursor_pos = self.cursorPosition()
        before_text = unicode(self.text())[:cursor_pos]
        after_text = unicode(self.text())[cursor_pos:]
        prefix_len = len(before_text.split(self.delimiters[0])[-1].strip())

        if after_text.startswith(self.delimiters[1]):
            self.setText(before_text[:cursor_pos - prefix_len] + text +
                            after_text)
        else:
            self.setText(before_text[:cursor_pos - prefix_len] + text +
                        self.delimiters[1] + after_text)

        self.string = before_text[:cursor_pos - prefix_len] + text +\
                        self.delimiters[1] + after_text

        self.setCursorPosition(cursor_pos - prefix_len + len(text) + 2)
        self.textEdited.emit(self.string)

    def on_editing_finished(self):
        self._upddate_entries = True

#-------------------------------------------------------------------------------
#  'SimpleEditor' class:
#-------------------------------------------------------------------------------

class SimpleEditor ( Editor ):
    """ Simple style text editor, which displays a text field.
    """

    #---------------------------------------------------------------------------
    #  Finishes initializing the editor by creating the underlying toolkit
    #  widget:
    #---------------------------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        factory = self.factory
        delimiters = factory.delimiters
        entries = factory.entries
        entries_updater = factory.entries_updater

        control = CompleterLineEdit(self.str_value, delimiters, entries,
                                    entries_updater)

        control.textEdited.connect(self.update_object)

        self.control = control
        # default horizontal policy is Expand, set this to Minimum
        if not (self.item.resizable == True) and not self.item.springy:
            policy = self.control.sizePolicy()
            policy.setHorizontalPolicy(QtGui.QSizePolicy.Minimum)
            self.control.setSizePolicy(policy)
        self.set_error_state( False )
        self.set_tooltip()

    #---------------------------------------------------------------------------
    #  Handles the user entering input data in the edit control:
    #---------------------------------------------------------------------------

    def update_object ( self ):
        """ Handles the user entering input data in the edit control.
        """
        if (not self._no_update) and (self.control is not None):
            try:
                self.value = self._get_user_value()

                if self._error is not None:
                    self._error = None
                    self.ui.errors -= 1

                self.set_error_state( False )

            except TraitError, excp:
                pass

    #---------------------------------------------------------------------------
    #  Updates the editor when the object trait changes external to the editor:
    #---------------------------------------------------------------------------

    def update_editor ( self ):
        """ Updates the editor when the object trait changes externally to the
            editor.
        """
        user_value = self._get_user_value()
        try:
            unequal = bool(user_value != self.value)
        except ValueError:
            # This might be a numpy array.
            unequal = True

        if unequal:
            self._no_update = True
            self.control.setText(self.str_value)
            self._no_update = False

        if self._error is not None:
            self._error = None
            self.ui.errors -= 1
            self.set_error_state( False )

    #---------------------------------------------------------------------------
    #  Gets the actual value corresponding to what the user typed:
    #---------------------------------------------------------------------------

    def _get_user_value ( self ):
        """ Gets the actual value corresponding to what the user typed.
        """
        try:
            value = self.control.text()
        except AttributeError:
            value = self.control.toPlainText()

        value = unicode(value)

        try:
            value = self.evaluate( value )
        except:
            pass

        return value

    #---------------------------------------------------------------------------
    #  Handles an error that occurs while setting the object's trait value:
    #---------------------------------------------------------------------------

    def error ( self, excp ):
        """ Handles an error that occurs while setting the object's trait value.
        """
        if self._error is None:
            self._error = True
            self.ui.errors += 1

        self.set_error_state( True )

    #---------------------------------------------------------------------------
    #  Returns whether or not the editor is in an error state:
    #---------------------------------------------------------------------------

    def in_error_state ( self ):
        """ Returns whether or not the editor is in an error state.
        """
        return (self.invalid or self._error)