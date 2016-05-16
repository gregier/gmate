# -*- coding: utf-8 -*-

from gi.repository import GObject, Gdk, Gtk, Gedit


_KEYS = (Gdk.KEY_Tab, Gdk.KEY_KP_Tab, Gdk.KEY_ISO_Left_Tab)
_MODIFIERS = (Gdk.ModifierType.CONTROL_MASK,
              Gdk.ModifierType.CONTROL_MASK |
              Gdk.ModifierType.SHIFT_MASK)


class TabSwitchPlugin(GObject.Object, Gedit.WindowActivatable):
    window = GObject.Property(type=Gedit.Window)

    def __init__(self):
        super().__init__()

    def do_activate(self):
        self._key_press_id = self.window.connect('key-press-event',
                                                 self.on_key_press_event)

    def do_deactivate(self):
        self.window.disconnect(self._key_press_id)

    def on_key_press_event(self, window, event):
        if event.keyval not in _KEYS:
            return False

        modifiers = event.state & Gtk.accelerator_get_default_mod_mask()
        if modifiers not in _MODIFIERS:
            return False

        tabs = [Gedit.Tab.get_from_document(doc)
                for doc in self.window.get_documents()]
        move_forward = not modifiers & Gdk.ModifierType.SHIFT_MASK
    
        index = tabs.index(self.window.get_active_tab())
        index += 1 if move_forward else -1

        self.window.set_active_tab(tabs[index % len(tabs)])
        return True

# ex:ts=4:et:
