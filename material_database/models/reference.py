#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the material_database module.
#
# material_database is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2021 Felix Steinbach, Daniel Schick, Martin Borchert

"""A :mod:`Reference` module """

__all__ = ["Reference"]

__docformat__ = "restructuredtext"

import logging
from ..helpers import trim_dict_name


class Reference():
    """Reference

    Reference holding information of references

    """

    def __init__(self, ID, data = None, log_level = logging.WARNING):
        self.logger = logging.getLogger(__name__)
        self.log_level = log_level
        self.logger.setLevel(level=self.log_level)
        self.ref_ID = ID
        self.author = ''
        self.journal = ''
        self.pages = ''
        self.title = ''
        self.volume = ''
        self.year = ''
        self.ENTRYTYPE = ''

        if data is not None:
            for k_first, v_first in data.items():
                setattr(self, k_first, v_first)
#        for key, value in data.items():
#            self.__dict__[key] = value

    def validate(self):
        """validate

        Some documentation here.

        """
        pass

    def dump(self):
        ref_dict = {}
        for ref_name, ref_data in self.__dict__.items():
            trim_name = trim_dict_name(ref_name, '')
            if not (trim_name == 'log_level' or trim_name == 'logger' or
                    trim_name == 'ref_ID' or trim_name == 'name'):
                ref_dict[trim_name] = ref_data
        return ref_dict
