# -*- coding: utf-8 -*-

import gtk

from kiwi.ui.delegates import Delegate

import bbcalc.gui.calculators.idealbody as idealbody
import bbcalc.gui.calculators.onerepmax as onerepmax
import bbcalc.gui.calculators.bmi as bmi
import bbcalc.gui.calculators.running as running
import bbcalc.gui.calculators.bodyfat as bodyfat
import bbcalc.gui.calculators.weightunits as weightunits


class MainWindow(Delegate):

    gladefile = 'main_window'

    def __init__(self):
        Delegate.__init__(self, delete_handler=gtk.main_quit)

        # Create calculators
        self._create_calculators()

    def _set_active(self, calculator):
        """Set active calculator"""
        if hasattr(self, '_calculator'):
            self.detach_slave('calc_box')
        self._calculator = calculator
        self.attach_slave('calc_box', calculator)
        calculator.focus_toplevel() # Must be done after attach

    def _create_calculators(self):
        """Create calculators and set default"""
        # Create dictionary of calculators
        onerep_max_calc = onerepmax.OneRepMax()
        idealbody_calc = idealbody.IdealBody()
        bodyfat_calc = bodyfat.Bodyfat()
        bmi_calc = bmi.BMI()
        running_calc = running.Running()
        weightunits_calc = weightunits.WeightUnitsConverter()

        self._calculators = {'onerep_max' : onerep_max_calc,
                             'ideal_body' : idealbody_calc,
                             'bodyfat' : bodyfat_calc,
                             'body_mass_index' : bmi_calc,
                             'running' : running_calc,
                             'weightunits' : weightunits_calc
                             }
        # Set default calculator
        self._set_active(self._calculators['bodyfat'])

    # Signal handlers

    def on_quit_menu__activate(self, *args):
        gtk.main_quit()

    def on_preferences_menu__activate(self, action):
        from bbcalc.gui.preferences import PreferencesDialog
        dialog = PreferencesDialog()
        dialog.show()

    def on_about_menu__activate(self, action):
        from bbcalc.gui.about import about_dialog
        about_dialog()

    def on_calculator_activate(self, widget):
        """Activate selected calculator"""
        if widget.get_active() == True:
            # widget.name is short name of selected calculator
            self._set_active(self._calculators[widget.name])


def main(name=None, version=None):
    delegate = MainWindow()
    delegate.show()
    gtk.main()