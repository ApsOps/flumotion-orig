# -*- Mode: Python; fill-column: 80 -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# Flumotion - a streaming media server
# Copyright (C) 2004,2005 Fluendo, S.L. (www.fluendo.com). All rights reserved.

# This file may be distributed and/or modified under the terms of
# the GNU General Public License version 2 as published by
# the Free Software Foundation.
# This file is distributed without any warranty; without even the implied
# warranty of merchantability or fitness for a particular purpose.
# See "LICENSE.GPL" in the source distribution for more information.

# Licensees having purchased or holding a valid Flumotion Advanced
# Streaming Server license may use this file in accordance with th
# Flumotion Advanced Streaming Server Commercial License Agreement.
# See "LICENSE.Flumotion" in the source distribution for more information.

# Headers in this file shall remain intact.


import os

import gtk
import gtk.glade
import gobject

from flumotion.configure import configure


class GladeWidget(gtk.VBox):
    '''
    Base class for composite widgets backed by glade interface definitions.

    Example:
    class MyWidget(GladeWidget):
        glade_file = 'my_glade_file.glade'
        ...
    gobject.type_register(MyWidget)

    Remember to chain up if you customize __init__().
    '''
        
    glade_file = None

    def __init__(self):
        gtk.VBox.__init__(self)
        wtree = gtk.glade.XML(os.path.join(configure.gladedir,
                                           self.glade_file))
        win = None
        for widget in wtree.get_widget_prefix(''):
            wname = widget.get_name()
            if isinstance(widget, gtk.Window):
                assert win == None
                win = widget
                continue
            
            if hasattr(self, wname) and getattr(self, wname):
                raise AssertionError (
                    "There is already an attribute called %s in %r" %
                    (wname, self))
            setattr(self, wname, widget)

        assert win != None
        w = win.get_child()
        win.remove(w)
        self.add(w)
        win.destroy()
        wtree.signal_autoconnect(self)
gobject.type_register(GladeWidget)


class GladeWindow(gobject.GObject):
    """
    Base class for dialogs or windows backed by glade interface definitions.

    Example:
    class MyWindow(GladeWindow):
        glade_file = 'my_glade_file.glade'
        ...

    Remember to chain up if you customize __init__(). Also note that GladeWindow
    does *not* descend from GtkWindow, so you can't treat the resulting object
    as a GtkWindow. The show, hide, destroy, and present methods are provided as
    convenience wrappers.
    """

    glade_dir = configure.gladedir
    glade_file = None

    window = None

    def __init__(self, parent=None):
        gobject.GObject.__init__(self)
        wtree = gtk.glade.XML(os.path.join(self.glade_dir, self.glade_file))
        self.widgets = {}
        for widget in wtree.get_widget_prefix(''):
            wname = widget.get_name()
            if isinstance(widget, gtk.Window):
                assert self.window == None
                self.window = widget
                continue
            
            if wname in self.widgets:
                raise AssertionError("Two objects with same name (%s): %r %r"
                                     % (wname, self.widgets[wname], widget))
            self.widgets[wname] = widget

        if parent:
            self.window.set_transient_for(parent)

        wtree.signal_autoconnect(self)

        self.destroy = self.window.destroy
        self.show = self.window.show
        self.hide = self.window.hide
        self.present = self.window.present
gobject.type_register(GladeWindow)
