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

"""A :mod:`Helpers` module """

__all__ = ["name_to_identifer"]

__docformat__ = "restructuredtext"

# import logging
import re


def name_to_identifer(name):
    """name to identifer"""
    temp = re.sub('[ ]+', '_', name.lower())
    res = re.sub('[^a-z0-9_]+', '', temp)
    if res.isidentifier():
        return res
    else:
        raise Exception('name "{:s}" is not a valid identifier'.format(res))


def trim_dict_name(name, trim_str):
    return name.replace(trim_str, '')
