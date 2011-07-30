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


class ProcessStrategyEngraving(pycam.Plugins.PluginBase):

    DEPENDS = ["ProcessStrategyManager", "PathParamStepDown",
            "PathParamMillingStyle", "PathParamRadiusCompensation",
            "PathParamTraceModel"]

    def setup(self):
        parameters = {"step_down": 1.0,
                "milling_style": "ignore",
                "radius_compensation": False,
                "trace_model": None
        }
        self.core.get("register_strategy")("engraving", "Engraving",
                self.run_strategy, parameters=parameters, weight=80)
        return True

    def teardown(self):
        self.core.get("unregister_strategy")("engraving")

    def run_strategy(self):
        pass



