# -*- coding: utf-8 -*-

import gtk

from kiwi.ui.delegates import Delegate


class MainWindow(Delegate):
    gladefile = 'main_window'

    def __init__(self):
        Delegate.__init__(self, delete_handler=self.quit_if_last)

    # Signal handlers

    def on_quit_menu__activate(self, *args):
        self.hide_and_quit()

    def on_about_menu__activate(self, action):
        from bbcalc.gui.about import about_dialog
        about_dialog()

def main(name=None, version=None):
    delegate = MainWindow()
    delegate.show()
    gtk.main()

