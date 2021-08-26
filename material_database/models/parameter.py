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

"""A :mod:`Parameter` module """

__all__ = ["Parameter"]

__docformat__ = "restructuredtext"

import logging
from ..helpers import trim_dict_name


class Parameter():
    """Parameter

    Parameter holding information of pyhsical parameters

    """

    def __init__(self, name, ref_Id, data=None, log_level=logging.WARNING):
        self.logger = logging.getLogger(__name__)
        self.log_level = log_level
        self.logger.setLevel(level=self.log_level)
        self.name = name
        self.ref_ID = ref_Id
        self.__value = None
        self.__uncertainty = 0
        self.__unit = ''
        self.__comment = ''

        if data is not None:

            for par_name, par_data in data.items():
                setattr(self, par_name, par_data)

    def addValueList(self, name, valList):
        setattr(self, name, valList)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, v):
        self.logger.info('setting the value is not that simple')
        self.logger.info('we need to change the value also in the'
                         'dict of them corresponding reference'
                         'ID: "{:s}"'.format(self.ref_ID))
        self.__value = v
        # self.__dict__[self.ref_ID]['value'] = v

    @property
    def uncertainty(self):
        return self.__uncertainty

    @uncertainty.setter
    def uncertainty(self, v):
        self.logger.info('setting the value is not that simple')
        self.logger.info('we need to change the value also in the'
                         'dict of them corresponding reference'
                         'ID: "{:s}"'.format(self.ref_ID))
        self.__uncertainty = v
        # self.__dict__[self.ref_ID]['value'] = v

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, v):
        self.logger.info('setting the value is not that simple')
        self.logger.info('we need to change the value also in the'
                         'dict of them corresponding reference'
                         'ID: "{:s}"'.format(self.ref_ID))
        self.__comment = v
        # self.__dict__[self.ref_ID]['value'] = v

    @property
    def unit(self):
        return self.__unit

    @unit.setter
    def unit(self, v):
        self.logger.info('setting the value is not that simple')
        self.logger.info('we need to change the value also in the'
                         'dict of them corresponding reference'
                         'ID: "{:s}"'.format(self.ref_ID))
        self.__unit = v
        # self.__dict__[self.ref_ID]['value'] = v

    def validate(self, ref_list):
        """validate

        Some documentation here.

        """
        if self.ref_ID not in ref_list:
            print('Reference %s of parameter %s is'
                  'not in database.'%(self.ref_ID, self.name))
            self.logger.fatal('Reference %s of parameter %s is not'
                              'in database.'%(self.ref_ID, self.name))
            return False
        return True

    def dump(self):
        par_dict = {}
        for par_name, par_data in self.__dict__.items():
            trim_name = trim_dict_name(par_name, '_Parameter__')
            if not (trim_name == 'log_level' or trim_name == 'logger' or
                    trim_name == 'ref_ID' or trim_name == 'name'):
                par_dict[trim_name] = par_data
        return par_dict
