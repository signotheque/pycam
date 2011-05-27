# -*- coding: utf-8 -*-
"""
$Id$

Copyright 2011 Lars Kruse <devel@sumpfralle.de>

This file is part of PyCAM.

PyCAM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyCAM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyCAM.  If not, see <http://www.gnu.org/licenses/>.
"""


import pycam.Plugins


class ModelPosition(pycam.Plugins.PluginBase):

    UI_FILE = "model_position.ui"

    def setup(self):
        if self.gui:
            position_box = self.gui.get_object("ModelPositionBox")
            position_box.unparent()
            self.core.register_ui("model_handling", "Position", position_box, -20)
            shift_model_button = self.gui.get_object("ShiftModelButton")
            shift_model_button.connect("clicked", self._shift_model)
            align_model_button = self.gui.get_object("AlignPositionButton")
            align_model_button.connect("clicked", self._align_model)
            # grab default button for shift/align controls
            for axis in "XYZ":
                obj = self.gui.get_object("ShiftPosition%s" % axis)
                obj.connect("focus-in-event", lambda widget, data: \
                        shift_model_button.grab_default())
                obj.connect("focus-out-event", lambda widget, data: \
                        shift_model_button.get_toplevel().set_default(None))
            for axis in "XYZ":
                for name_template in ("AlignPosition%s", "AlignPosition%sMin",
                        "AlignPosition%sCenter", "AlignPosition%sMax"):
                    obj = self.gui.get_object("AlignPosition%s" % axis)
                    obj.connect("focus-in-event", lambda widget, data: \
                            align_model_button.grab_default())
                    obj.connect("focus-out-event", lambda widget, data: \
                            align_model_button.get_toplevel().set_default(None))
        return True

    def teardown(self):
        if self.gui:
            self.core.unregister_ui("model_handling",
                    self.gui.get_object("ModelPositionBox"))

    def _shift_model(self, widget=None):
        model = self.core.get("model")
        if not model:
            return
        self.core.emit_event("model-change-before")
        self.core.get("update_progress")("Aligning model")
        self.core.get("disable_progress_cancel_button")()
        shift = [self.gui.get_object("ShiftPosition%s" % axis).get_value()
                for axis in "XYZ"]
        model.shift(shift[0], shift[1], shift[2],
                callback=self.core.get("update_progress"))
        self.core.emit_event("model-change-after")

    def _align_model(self, widget=None):
        model = self.core.get("model")
        if not model:
            return
        self.core.emit_event("model-change-before")
        self.core.get("update_progress")("Shifting model")
        self.core.get("disable_progress_cancel_button")()
        dest = [self.gui.get_object("AlignPosition%s" % axis).get_value()
                for axis in "XYZ"]
        shift_values = []
        for axis in "XYZ":
            dest = self.gui.get_object("AlignPosition%s" % axis).get_value()
            alignments = ("Min", "Center", "Max")
            for alignment in alignments:
                objname = "AlignPosition%s%s" % (axis, alignment)
                min_axis = getattr(model, "min%s" % axis.lower())
                max_axis = getattr(model, "max%s" % axis.lower())
                if self.gui.get_object(objname).get_active():
                    if alignment == "Min":
                        shift = dest - min_axis
                    elif alignment == "Center":
                        shift = dest - (min_axis + max_axis) / 2.0
                    else:
                        shift = dest - max_axis
                    shift_values.append(shift)
        model.shift(shift_values[0], shift_values[1], shift_values[2],
                callback=self.core.get("update_progress"))
        self.core.emit_event("model-change-after")

