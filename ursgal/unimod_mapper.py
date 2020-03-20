#!/usr/bin/env python
# encoding: utf-8
"""

    Ursgal MappOrs


    :copyright: (c) 2014 by C. Fufezan, S. Schulze
    :licence: BSD, see LISCENSE for more details

"""
from __future__ import absolute_import
import sys
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as xmldom
import ursgal


class UnimodMapper( object ):
    '''
    UnimodMapper class that creates lookup to the unimod.xml and
    userdefined_unimod.xml found located in ursgal/kb/ext and
    offers several helper methods described below :

    '''
    def __init__( self ):
        self.data_list = self._parseXML()
        self.mapper    = self._initialize_mapper()

    def _parseXML(self, xmlFile = None):
        if xmlFile is None:
            unimodXML = os.path.normpath(
                os.path.join(
                    os.path.dirname(__file__),
                    'resources',
                    'platform_independent',
                    'arc_independent',
                    'ext',
                    'unimod.xml'
                ))
            if unimodXML is None:
                print("No unimod.xml file found.")
                sys.exit(1)
            userdefined_unimodXML = os.path.normpath(
                os.path.join(
                    os.path.dirname(__file__),
                    'resources',
                    'platform_independent',
                    'arc_independent',
                    'ext',
                    'userdefined_unimod.xml'
                ))
            xmlFiles = [unimodXML, userdefined_unimodXML] 
        else:
            xmlFiles = [xmlFile]
        data_list = []
        for xmlFile in xmlFiles:
            if os.path.exists( xmlFile ):
                unimodXML = ET.iterparse(
                    open( xmlFile, 'r', encoding='utf-8'),
                    events = (b'start', b'end')
                )
                collect_element = False
                for event, element in unimodXML:
                    if event == b'start':
                        if element.tag.endswith('}mod'):
                            tmp = {
                                'unimodID' : element.attrib['record_id'],
                                'unimodname' : element.attrib['title'],
                                'element' : {}
                            }
                        elif element.tag.endswith('}delta'):
                            collect_element = True
                            tmp[ 'mono_mass' ] = float(
                                element.attrib[ 'mono_mass' ]
                            )
                        elif element.tag.endswith('}element'):
                            if collect_element is True:
                                number = int(element.attrib['number'])
                                if number != 0:
                                    tmp['element'][ element.attrib['symbol'] ] = \
                                        number
                        else:
                            pass
                    else:
                        # end element
                        if element.tag.endswith('}delta'):
                            collect_element = False
                        elif element.tag.endswith('}mod'):
                            data_list.append(tmp)
                        else:
                            pass

            else:
                continue
        return data_list

    def _initialize_mapper(self):
        '''set up the mapper, generates the index dict'''
        mapper = {}
        for index, unimod_data_dict in enumerate(self.data_list):
            for key, value in unimod_data_dict.items():
                if key == 'element':

                    MAJORS = ['C', 'H']
                    hill_notation = ''
                    for major in MAJORS:
                        if major in unimod_data_dict[key].keys():
                            hill_notation += '{0}({1})'.format(
                                major,
                                unimod_data_dict[key][major]
                            )
                    for symbol, number in sorted(unimod_data_dict[key].items()):
                        if symbol in MAJORS:
                            continue
                        hill_notation += '{0}({1})'.format(
                            symbol,
                            number
                        )
                    if hill_notation not in mapper.keys():
                        mapper[ hill_notation ] = []
                    mapper[ hill_notation ].append( index )
                elif key == 'mono_mass':
                    if value not in mapper.keys():
                        mapper[ value ] = []
                    mapper[ value ].append( index )
                else:
                    if value not in mapper.keys():
                        mapper[ value ] = index
        return mapper

    # name 2 ....
    def name2mass(self, unimod_name):
        '''
        Converts unimod name to unimod mono isotopic mass

        Args:
            unimod_name (str):

        Returns:
            float: Unimod mono isotopic mass
        '''
        return self._map_key_2_index_2_value(unimod_name, 'mono_mass')

    def name2composition(self, unimod_name):
        '''
        Converts unimod name to unimod composition

        Args:
            unimod_name (str):

        Returns:
            dict: Unimod elemental composition
        '''
        return self._map_key_2_index_2_value(unimod_name, 'element')

    def name2id(self, unimod_name):
        '''
        Converts unimod name to unimodID

        Args:
            unimod_name (str):

        Returns:
            int: Unimod id
        '''
        return self._map_key_2_index_2_value(unimod_name, 'unimodID')

    # unimodid 2 ....
    def id2mass(self, unimod_id):
        '''
        Converts unimodID to unimod mass

        Args:
            unimod_id (int):

        Returns:
            float: Unimod mono isotopic mass
        '''
        return self._map_key_2_index_2_value(unimod_id, 'mono_mass')

    def id2composition(self, unimod_id):
        '''
        Converts unimod id to unimod composition

        Args:
            unimod_id (int):

        Returns:
            dict: Unimod elemental composition
        '''
        return self._map_key_2_index_2_value(unimod_id, 'element')

    def id2name(self, unimod_id):
        '''
        Converts unimodID to unimod name

        Args:
            unimod_id (int):

        Returns:
            str: Unimod name
        '''
        return self._map_key_2_index_2_value(unimod_id, 'unimodname')

    # mass is ambigous therefore a list is returned
    def mass2name_list(self, mass):
        '''
        Converts unimod mass to unimod name list,
            since a given mass can map to mutiple entries in the XML.

        Args:
            mass (float):

        Returns:
            list: Unimod names
        '''
        list_2_return = []
        index_list = self.mapper.get( mass, None)
        if index_list is not None:
            for index in index_list:
                list_2_return.append( self._data_list_2_value(index, 'unimodname'))
        return list_2_return

    def mass2id_list(self, mass):
        '''
        Converts unimod mass to unimod name list,
            since a given mass can map to mutiple entries in the XML.

        Args:
            mass (float):

        Returns:
            list: Unimod IDs
        '''
        list_2_return = []
        index_list = self.mapper.get( mass, None)
        if index_list is not None:
            for index in index_list:
                list_2_return.append(self._data_list_2_value(index, 'unimodID'))
        return list_2_return

    def mass2composition_list(self, mass):
        '''
        Converts unimod mass to unimod element composition list,
            since a given mass can map to mutiple entries in the XML.

        Args:
            mass (float):

        Returns:
            list: Unimod elemental compositions
        '''

        list_2_return = []
        index_list = self.mapper.get( mass, None)
        if index_list is not None:
            for index in index_list:
                list_2_return.append( self._data_list_2_value(index, 'element') )
        return list_2_return

    def composition2name_list(self, composition):
        '''
        Converts unimod composition to unimod name list,
            since a given composition can map to mutiple entries in the XML.

        Args:
            composition (dict):

        Returns:
            list: Unimod names
        '''
        list_2_return = []
        index_list = self.mapper.get( composition, None)
        if index_list is not None:
            for index in index_list:
                list_2_return.append( self._data_list_2_value(index, 'unimodname'))
        return list_2_return

    def composition2id_list(self, composition):
        '''
        Converts unimod composition to unimod name list,
            since a given composition can map to mutiple entries in the XML.

        Args:
            composition (dict):

        Returns:
            list: Unimod IDs
        '''
        list_2_return = []
        index_list = self.mapper.get( composition, None)
        if index_list is not None:
            for index in index_list:
                list_2_return.append(
                    self._data_list_2_value(index, 'unimodID')
                )
        return list_2_return

    def composition2mass(self, composition):
        '''
        Converts unimod composition to unimod monoisotopic mass,

        Args:
            composition (float):

        Returns:
            float: monoisotopic mass
        '''
        mass_2_return = None
        list_2_return = []
        index_list = self.mapper.get( composition, None)
        if index_list != None:
            for index in index_list:
                list_2_return.append( self._data_list_2_value(index, 'mono_mass') )
            assert len(set(list_2_return)) == 1, '''
            Unimod chemical composition {0}
            maps on different monoisotopic masses. This should not happen.
            '''.format( composition )
            mass_2_return = list_2_return[0]
        return mass_2_return

    def appMass2id_list(self, mass, decimal_places = 2):
        '''
        Creates a list of unimod ids for a given approximate mass

        Args:
            mass (float):

        Keyword Arguments:
            decimal_places (int): Precision with which the masses in the
                Unimod is compared to the input, i.e.
                round( mass, decimal_places )

        Returns:
            list: Unimod IDs

        Examples::
            >>> import ursgal
            >>> U = ursgal.UnimodMapper()
            >>> U.appMass2id_list(18, decimal_places=0)
            ['127', '329', '608', '1079', '1167']

        '''
        return_list = self._appMass2whatever(
            mass,
            decimal_places= decimal_places,
            entry_key='unimodID'
        )
        return return_list

    def appMass2element_list(self, mass, decimal_places = 2):
        '''
        Creates a list of element composition dicts for a given approximate mass

        Args:
            mass (float):

        Keyword Arguments:
            decimal_places (int): Precision with which the masses in the
                Unimod is compared to the input, i.e. round( mass, decimal_places )

        Returns:
            list: Dicts of elements

        Examples::
            >>> import ursgal
            >>> U = ursgal.UnimodMapper()
            >>> U.appMass2element_list(18, decimal_places=0)
            [{'F': 1, 'H': -1}, {'13C': 1, 'H': -1, '2H': 3},
                {'H': -2, 'C': -1, 'S': 1}, {'H': 2, 'C': 4, 'O': -2},
                {'H': -2, 'C': -1, 'O': 2}]


        '''
        return_list = self._appMass2whatever(
            mass,
            decimal_places= decimal_places,
            entry_key='element'
        )
        return return_list

    def appMass2name_list(self, mass, decimal_places = 2):
        '''
        Creates a list of unimod names for a given approximate mass

        Args:
            mass (float)

        Keyword Arguments:
            decimal_places (int): Precision with which the masses in the
                Unimod is compared to the input, i.e. round( mass, decimal_places )

        Returns:
            list: Unimod names

        Examples::
            >>> import ursgal
            >>> U = ursgal.UnimodMapper()
            >>> U.appMass2name_list(18, decimal_places=0)
            ['Fluoro', 'Methyl:2H(3)13C(1)', 'Xle->Met', 'Glu->Phe', 'Pro->Asp']
        '''
        return_list = self._appMass2whatever(
            mass,
            decimal_places= decimal_places,
            entry_key='unimodname'
        )
        return return_list

    def _appMass2whatever(self, mass, decimal_places=2, entry_key=None):
        return_list = []
        for entry in self.data_list:
            umass = entry['mono_mass']
            rounded_umass = round( float(umass), decimal_places )
            if abs(rounded_umass - mass) <= sys.float_info.epsilon:
                return_list.append( entry[ entry_key ] )
        return return_list

    def _map_key_2_index_2_value(self, map_key, return_key):
        ''''''
        if type(map_key) is int:
            map_key = str(map_key)
        index = self.mapper.get( map_key.strip(), None)
        if index is None:
            ursgal.UNode.print_info(
                'Cannot return {0} via map {1}'.format( \
                    return_key,
                    map_key,
                ),
                caller='WARNING'
            )
            return_value = None
        else:
            return_value = self._data_list_2_value(index, return_key)
        return return_value

    def _data_list_2_value(self, index, return_key):
        ''''''
        return self.data_list[ index ][ return_key ]

    def writeXML(self, modification_dict, xmlFile = None):
        '''
        Writes a unimod-style userdefined_unimod.xml file in 
        ursal/resources/platform_independent/arc_independent/ext

        Args:
            modification_dict (dict): dictionary containing at least
            'mass' (mass of the modification),
            'name' (name of the modificaton),
            'composition' (chmical composition of the modification as a Hill notation)
        '''
        if xmlFile == None:
            xmlFile = os.path.normpath(
                os.path.join(
                    os.path.dirname(__file__),
                    'resources',
                    'platform_independent',
                    'arc_independent',
                    'ext',
                    'userdefined_unimod.xml'
                ))
        unimod = ET.Element('{usermod}unimod')
        modifications = ET.SubElement(unimod, '{usermod}modifications')
        mod_dicts = [modification_dict]
        if os.path.exists(xmlFile):
            data_list = self._parseXML(xmlFile)
            for data_dict in data_list:
                mod_dict = {
                    'mass'  : data_dict['mono_mass'],
                    'name'  : data_dict['unimodname'],
                    'composition' : data_dict['element'],
                    'id'    : data_dict['unimodID'],
                }
                mod_dicts.insert(-1,mod_dict)

        for modification_dict in mod_dicts:
            if modification_dict.get('id', None) == None:
                modification_dict['id'] = 'u{0}'.format(len(mod_dicts))
            mod = ET.SubElement(modifications, '{usermod}mod', title = modification_dict['name'], record_id = modification_dict['id'])
            delta = ET.SubElement(mod, '{usermod}delta', mono_mass = str(modification_dict['mass']) )

            for symbol, number in modification_dict['composition'].items():
                element = ET.SubElement(delta, '{usermod}element', symbol=symbol, number=str(number) )

        tree = ET.ElementTree(unimod)
        tree.write(xmlFile, encoding = 'utf-8')
        xml = xmldom.parse(xmlFile)
        pretty_xml_as_string = xml.toprettyxml()
        outfile = open(xmlFile, 'w')
        print(pretty_xml_as_string, file = outfile)
        outfile.close()
        self._reparseXML()
        return

    def _reparseXML(self):
        self.data_list = self._parseXML()
        self.mapper    = self._initialize_mapper()

if __name__ == '__main__':
    print('Yes!')
