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
from pycam.Exporters.GCodeExporter import GCodeGenerator

class PostprocessorEMC2(pycam.Plugins.PluginBase):

    DEPENDS = ["ToolpathExport"]
    CATEGORIES = ["Postprocessor"]

    def setup(self):
        self.core.get("register_postprocessor")("emc2", "EMC2", GCodeGenerator)
        return True

    def teardown(self):
        self.core.get("unregister_postprocessor")("emc2")

