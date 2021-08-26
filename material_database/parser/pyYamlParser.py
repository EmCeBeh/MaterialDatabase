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
# Copyright (C) 2020 Felix Steinbach, Daniel Schick

"""A :mod:`PyYamlParser` module """

__all__ = ["PyYamlParser"]

__docformat__ = "restructuredtext"

# import numpy as np
import yaml
from os import path
import logging
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
import re


class PyYamlParser():
    """PyYamlParser

    PyYamlParser parsing data

    """

    def __init__(self, base_path, log_level=logging.WARNING):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level=log_level)
        if path.exists(base_path):
            self.base_path = base_path
            self.logger.info('Base path of PyYamlParser set to: {:s}'.format(base_path))
        else:
            self.logger.error('Path {:s} does not exist!'.format(base_path))

    def load(self, material):
        """load a yaml file

        load a yaml from the given path and return a dictionary.

        """
        full_file_name = path.join(path.abspath(self.base_path),
                                   material + '.yaml')
        # read yaml file
        with open(full_file_name, 'r') as file:
            material_data = yaml.unsafe_load(file)

        # add filename as ID to dict
        material_data['ID'] = material

        self.logger.info('converted yaml file "{:s}" to Python dictionary'.format(
            full_file_name))
        bibtex = material_data['meta']['references']

        # convert bibtex into list of dicts
        # these two lines also allow for other types than the standard:

        # 'article',
        # 'book',
        # 'booklet',
        # 'conference',
        # 'inbook',
        # 'incollection',
        # 'inproceedings',
        # 'manual',
        # 'mastersthesis',
        # 'misc',
        # 'phdthesis',
        # 'proceedings',
        # 'techreport',
        # 'unpublished'

        parser = bibtexparser.bparser.BibTexParser(common_strings=False)
        parser.ignore_nonstandard_types = False
        # parser.homogenise_fields = False

        bib_list = bibtexparser.loads(bibtex, parser).entries

        # create dicts with bibtex ID as key
        bib_dict = {}
        for bibtex_entry in bib_list:
            bib_dict[bibtex_entry['ID']] = bibtex_entry
            del bib_dict[bibtex_entry['ID']]['ID']
        self.logger.info('found {:d} bibtex entries and converted them to'
                         'Python dictionaries'.format(len(bib_dict)))
        # replace bibtex string with dict
        material_data['meta']['references'] = bib_dict

        # This part fixes pyYaml's issue in reading complex numbers as strings.
        # Manually step through the array and turn strings into complex numbers
        for prop_key, prop_value in material_data['data'].items():
            for cite_key, cite_value in prop_value.items():
                if type(cite_value['value']) == str:
                    self.logger.info(cite_value['value'])
                    complex_corrected = complex(cite_value['value'].replace("i", "j").replace(" ",  ""))
                    material_data['data'][prop_key][cite_key]['value'] = complex_corrected
                elif type(cite_value['value']) == list and type(cite_value['value'][0]) == str:
                    complex_corrected = [complex(v.replace("i",  "j").replace(" ", "")) for v in cite_value['value']]
                    material_data['data'][prop_key][cite_key]['value'] = complex_corrected
                else:
                    pass
        return material_data

    def dump(self, material_data):
        """dump dictionary to yaml file

        converts a dictionary into a yaml file
        which is returned by this function

        """

        # divide the dict into three dict. BibDict contains the references,
        # metaDict contains the meta dates and dataDict contains the data.
        bib_dict = material_data["meta"]["references"]
        meta_dict = dict(material_data["meta"])
        data_dict = material_data['data']

        del meta_dict["references"]

        yaml_meta = "meta:\n"
        meta_str = (yaml.dump(meta_dict,
                              allow_unicode=True,
                              sort_keys=False)).rstrip(" ")
        split_meta = meta_str.split("\n")
        for str_inx, sub_str in enumerate(split_meta):
            yaml_meta += '  ' + sub_str + '\n'
        yaml_meta = yaml_meta[:-2]

        bib_list = []
        for dic_name, dic_data in bib_dict.items():
            dic_data['ID'] = dic_name
            bib_list.append(dic_data)
        bib_Obj = BibDatabase()
        bib_Obj.entries = bib_list
        bib_str = bibtexparser.dumps(bib_Obj)
        split_bib = bib_str.split("\n")
        indexes = [i for i, x in enumerate(split_bib) if re.search(r'^@[A-Za-z0-9]+{',x)]

        yaml_bib = " references: \n"
        for str_inx, sub_str in enumerate(split_bib):
            if str_inx in indexes:
                if str_inx == indexes[0]:
                    yaml_bib += "   '" + sub_str + '\n'
                else:
                    yaml_bib += '    ' + sub_str + '\n'
            else:
                yaml_bib += '        ' + sub_str + '\n'
        yaml_bib = yaml_bib[:-2]
        yaml_bib += "'\n"

        # add a data header
        yaml_data = "data:\n"

        '''
        Loop through the parameter names and reference names and add each key
        to the yaml data string.
        The data string has two spaces in front and the
        reference name four spaces.
        The type of value determines which flow_style is used to convert the
        value dict into a yaml string.
        Values that are dict are converted as flow_style = None and
        scalar values as flow_style = False
        '''

        for par_name in data_dict.keys():

            yaml_data += '  ' + par_name+':\n'
            par = data_dict[par_name]
            for ref_name in par.keys():
                yaml_data += '    ' + ref_name + ':\n'
                value = par[ref_name]['value']

                if(value is None or value == 'null'):
                    tmp_yaml = yaml.dump(par[ref_name],
                                         default_flow_style=None,
                                         sort_keys=False)
                else:
                    tmp_yaml = yaml.dump(par[ref_name],
                                         default_flow_style=False,
                                         allow_unicode=True,
                                         sort_keys=False)

                # Six spaces are added in front of each value line.
                split_tmp = tmp_yaml.split('\n')
                for str_inx, sub_str in enumerate(split_tmp):
                    yaml_data += '      ' + sub_str + '\n'
                    # split_tmp[0] = '      ' + split_tmp[0]
                # yaml_par = '\n'.join(split_tmp)
                # yaml_data += yaml_par

            yaml_data = yaml_data.rstrip(' ')

        # Concat the meta, references and data yaml string and return it
        yamlFile = yaml_meta + yaml_bib + '\n' + yaml_data

        full_file_name = path.join(path.abspath(self.base_path),
                                   meta_dict['name'].replace(' ', '_') + '.yaml')
        # read yaml file
        f = open(full_file_name, "w")
        f.write(yamlFile)
        f.close()
        # with open(full_file_name, 'r') as file:
        #    material_data = yaml.load(file, Loader=yaml.FullLoader)

        return yamlFile
