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

"""A :mod:`Material` module """

__all__ = ["Material"]

__docformat__ = "restructuredtext"

import logging
from .parameter import Parameter
from .reference import Reference
from ..helpers import name_to_identifer


class Material():
    """Material

    Material holding information of pyhsical parameters

    Args:
        data_dict: dictionary holding all information of the material

    Attributes:
        ID (int): unique integer ID
        name (str): name of the material
        description (str): description of properties of the material
        last_updated (str): date of the last update (YYYY-MM-DD)
        parameters (dict): dictionary holding paramter objects
        references (dics): dictionary holding references

    """

    def __init__(self, material_data={}, log_level=logging.WARNING):
        self.logger = logging.getLogger(__name__)
        self.log_level = log_level
        self.logger.setLevel(level=self.log_level)

        self.ID = -1
        self.name = ''
        self.description = ''
        self.comment = ''
        self.last_updated = ''
        if material_data:
            self.build_from_dict(material_data)

    def build_from_dict(self, material_data):
        """build_from_dict

        Some documentation here.

        """
        self.ID = material_data['ID']
        self.name = material_data['meta']['name']
        self.description = material_data['meta']['description']
        self.comment = material_data['meta']['comment']
        self.last_updated = material_data['meta']['last_updated']

        # add references
        for ref_ID, ref_data in material_data['meta']['references'].items():
            ID = name_to_identifer(ref_ID)
            self.__dict__[ID] = Reference(ID, ref_data, log_level=self.log_level)
            self.logger.info('added reference with key {:s}'.format(ID))

        for par_name, par_data in material_data['data'].items():
            name = name_to_identifer(par_name)
            tmp_par_dict = {}
            for sub_par_name, sub_par_data in par_data.items():
                sub_name = name_to_identifer(sub_par_name)
                tmp_par_dict[sub_name] = Parameter(name, sub_name, sub_par_data, log_level=self.log_level)
            self.__dict__[name] = tmp_par_dict
            self.logger.info('added parameter with name {:s}'.format(name))

    def dump(self):
        """dump_to_dict

        Some documentation here.

        """
        if self.validate():
            mat_dict = {}
            par_list = self.list_parameters()
            ref_list = self.list_references()
            par_dict = {}
            for par in par_list:
                par_obj = getattr(self, par)
                tmp_par_dict = {}
                for par_name, par_data in par_obj.items():
                    tmp_par_dict[par_name] = par_data.dump()
                par_dict[par] = tmp_par_dict
            mat_dict['data'] = par_dict
            
            meta_dict = {}
            ref_dict = {}
            for ref in ref_list:
                ref_obj = getattr(self, ref)
                ref_dict[ref] = ref_obj.dump()
            meta_dict['references'] = ref_dict
            meta_dict['name'] = self.name
            meta_dict['last_updated'] = self.last_updated
            meta_dict['description'] = self.description
            meta_dict['comment'] = self.comment
            mat_dict['meta'] = meta_dict
            mat_dict['ID'] = self.name

            return mat_dict
        return None

    def validate(self):
        """validate

            Checks weather a new parameter is given
            for an existing reference

        """
        par_list = self.list_parameters()
        ref_list = self.list_references()
        for par in par_list:
            par_dict = getattr(self, par)
            for par_name, par_data in par_dict.items():
                if not par_data.validate(ref_list):
                    return False
        return True

    def add_parameter(self, parameter):
        """add_parameter

        Some documentation here.

        """
        ref_list = self.list_references()

        if parameter.validate(ref_list):
            try:
                tmp_par_dict = self.__dict__[parameter.name]
            except:
                tmp_par_dict = {}
            tmp_par_dict[parameter.ref_ID] = parameter
            self.__dict__[parameter.name] = tmp_par_dict

            self.logger.info('Added parameter %s with reference %s correctly'
                             'to database.'%(parameter.name, parameter.ref_ID))

    def add_reference(self, reference):
        """add_reference

        Some documentation here.

        """
        self.__dict__[reference.ref_ID] = reference
        print('Added reference %s correctly to database.'%(reference.ref_ID))
        self.logger.info('Added reference %s correctly'
                         'to database.'%(reference.ref_ID))

    def list_parameters(self):
        """list_parameters

        Some documentation here.

        """
        par_list = []
        for par_name in self.__dict__:
            if type(self.__dict__[par_name])==dict:
                par_list.append(par_name)
        return par_list

    def list_references(self):
        """list_references

        Some documentation here.

        """
        ref_list = []
        for ref_name in self.__dict__:
            if type(self.__dict__[ref_name]) == Reference:
                ref_list.append(ref_name)
        return ref_list
