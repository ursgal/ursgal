#!/usr/bin/env python
import ursgal
import os
import shutil


class kojak_1_5_3( ursgal.UNode ):
    """
    Kojak UNode
    Parameter options at http://www.kojak-ms.org/param/index.html

    Reference:
    Hoopmann MR, Zelter A, Johnson RS, Riffle M, Maccoss MJ, Davis TN, Moritz RL (2015) Kojak: Efficient analysis of chemically cross-linked protein complexes. J Proteome Res 14: 2190-198

    Note:

        Kojak has to be installed manually at the moment! Use folder name:
        'kojak_1_5_3' in the resources folder.

    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'Kojak',
        'version'                     : '1.5.3',
        'release_date'                : '2015-5-1',
        'engine_type' : {
            'cross_link_search_engine' : True,
        },
        'input_extensions'            : ['.mzML', '.mzXML'],
        'output_extensions' : ['.kojak.txt', '.pep.xml', '.perc.inter.txt', \
            '.perc.intra.txt', '.perc.loop.txt', '.perc.single.txt'],
        'create_own_folder'           : True,
        'distributable'               : False,
        'in_development'              : False,
        'include_in_git'              : None,
        'utranslation_style'          : 'kojak_style_1',
        'engine' : {
            'linux' : {
                '64bit' : {
                    'exe'            : 'kojak',
                    'url'            : '',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                },
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'kojak',
                    'url'            : '',
                    'zip_md5'        : '',
                    'additional_exe' : [],
                }
            },
        },
        'citation' : \
            'Hoopmann MR, Zelter A, Johnson RS, Riffle M, Maccoss MJ, Davis '\
            'TN, Moritz RL (2015) Kojak: Efficient analysis of chemically '\
            'cross-linked protein complexes. J Proteome Res 14: 2190-198',
    }


    def __init__(self, *args, **kwargs):
        super(kojak_1_5_3, self).__init__(*args, **kwargs)
        pass

    def preflight( self ):
        '''
        Formatting the command line via self.params

        '''
        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )
        input_file = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        if input_file.lower().endswith('.mzml') or \
            input_file.lower().endswith('.mzml.gz'):
            self.params['translations']['mzml_input_file'] = input_file
        elif input_file.lower().endswith('.mgf'):
            self.params['translations']['mzml_input_file'] = \
                self.meta_unodes['ucontroller'].get_mzml_that_corresponds_to_mgf( input_file )
            self.print_info(
                'Kojak cannot read .mgf files.'
                'the corresponding mzML file {0} will be used instead.'.format(
                    os.path.abspath(self.params['translations']['mzml_input_file'])
                ),
                caller = "INFO"
            )
        else:
            raise Exception('Kojak input spectrum file must be in mzML or MGF format!')


        # remap modifications to adapt to kojak format
        self.params['translations']['kojak_fix_modifications'] = ''
        self.params['translations']['kojak_opt_modifications'] = ''
        for mod_type, mod_list in self.params['mods'].items():
            mod_dict_key = 'kojak_{0}_modifications'.format(mod_type)
            # if len(mod_list) > 0:
            #     self.p[]
            if mod_type == 'fix':
                param_name = 'fixed_modification'
            else:
                param_name = 'modification'
            for mod_dict in mod_list:
                self.params['translations'][mod_dict_key] += '{0} = {1} {2}\n'.format(
                    param_name,
                    mod_dict['aa'],
                    mod_dict['mass']
                )
        self.params['translations']['formatted_cross_link'] = ''
        self.params['translations']['formatted_mono_link'] = ''
        if len(self.params['translations']['cross_link_definition']) > 0:
            for cross_link in self.params['translations']['cross_link_definition']:
                self.params['translations']['formatted_cross_link'] += 'cross_link = {0}\n'.format(cross_link)

        if len(self.params['translations']['mono_link_definition']) > 0:
            for mono_link in self.params['translations']['mono_link_definition']:
                if mono_link not in [None, '']:
                    self.params['translations']['formatted_mono_link'] += 'mono_link = {0}\n'.format(mono_link)

        for ion in ['a', 'b', 'c', 'x', 'y', 'z']:
            if ion in self.params['translations']['score_ion_list']:
                self.params['translations']['ion_series_{0}'.format(ion.upper())] = 1
            else:
                self.params['translations']['ion_series_{0}'.format(ion.upper())] = 0

        # building command_list !

        templates = self.format_templates( )
        config_file_path = os.path.join(
            self.params['output_dir_path'],
            'Kojak.conf'
        )
        with open( config_file_path, 'w') as out:
            print(
                templates['Kojak.conf'],
                file = out
            )
            self.print_info('wrote input file {0}'.format( config_file_path ))
        self.params['command_list'] =[
            self.exe,
            '{0}'.format(config_file_path)
        ]

        return self.params

    def postflight( self ):
        '''
        Move the result files to the Kojak folder, since the output files can
        not be specified manually.
        '''
        # kojak_extensions = [
        #     '.kojak.txt',
        #     '.pep.xml',
        #     '.perc.inter.txt',
        #     '.perc.intra.txt',
        #     '.perc.loop.txt',
        #     '.perc.single.txt',
        # ]
        for extension in self.META_INFO['all_extensions']:
            org_path = os.path.join(
                self.params['input_dir_path'],
                '{0}{1}'.format(
                    self.params['file_root'],
                    extension
                )
            )
            new_path = os.path.join(
                self.params['output_dir_path'],
                '{0}_kojak_{1}{2}'.format(
                    self.params['file_root'],
                    self.META_INFO['version'].replace('.', '_'),
                    extension
                )
            )
            if os.path.exists(org_path):
                shutil.move(
                    org_path,
                    new_path
                )

        pass

    def format_templates( self ):
        '''
        Returns formatted input files as a dict.

        The standard parametern file is used and adjustes.

        Returns:
            dict: keys are the names of the parametern template file

        '''
        templates = {
            'Kojak.conf' : '''\
# Kojak version 1.5.3 parameter file
# Please see online documentation at:
# http://www.kojak-ms.org/param

# All parameters are separated from their values by an equals sign ('=')
# Anything after a '#' will be ignored for the remainder of the line.


#
# Computational resources
#
threads     =   {cpus} #Increase to use more cores/nodes


#
# Data input files: include full path if not in current working directory
#
database            =   {database}
export_percolator   =   {kojak_export_percolator}
export_pepXML       =   {kojak_export_pepxml}
MS_data_file        =   {mzml_input_file}
percolator_version  =   {kojak_percolator_version}
# output_file       =   {output_file_incl_path}


#
# Parameters used to described the data being input to Kojak
#
enrichment      =   {kojak_enrichment}       #Values between 0 and 1 to describe 18O APE.
                            #For example, 0.25 equals 25 APE.
instrument      =   {instrument}       #Values are: 0=Orbitrap, 1=FTICR (such as Thermo LTQ-FT)
MS1_centroid    =   {ms1_is_centroided}       #0=no, 1=yes
MS2_centroid    =   {ms2_is_centroided}        #0=no, 1=yes
MS1_resolution  =   {ms1_resolution}    #Resolution at 400 m/z, value ignored if data are
                            #already centroided
MS2_resolution  =   {ms2_resolution}    #Resolution at 400 m/z, value ignored if data are
                            #already centroided


#
# Cross-link and mono-link masses allowed. May have more than one of each parameter.
#
# Format for cross_link is [amino acids] [amino acids] [mass mod] [identifier]
# Format for mono_link is [amino acids] [mass mod]
# One or more amino acids (uppercase only!!) can be specified for each linkage moiety
# Use lowercase 'n' or 'c' to indicate protein N-terminus or C-terminus
#
# cross_link  =   nK  nK  138.0680742 BS3
# mono_link   =   nK  156.0786
# cross_link = C G -18.010565 Thioester_loss_of_water
{formatted_cross_link}
{formatted_mono_link}


#
# Fixed modifications. Add as many as necessary.
#
#fixed_modification  =   C   57.02146
{kojak_fix_modifications}


#
# Differential modifications. Add as many as necessary. Uppercase only!
# n = protein N-terminus, c = protein C-terminus
#
# If more than one modification is possible for an amino acid,
# list all modifications on separate lines
#
#modification            =       M       15.9949
{kojak_opt_modifications}

diff_mods_on_xl         =       {kojak_diff_mods_on_xl}
max_mods_per_peptide    =       {max_num_mods}
mono_links_on_xl        =       {kojak_mono_links_on_xl}


#
# Digestion enzyme rules.
#
# See http://www.kojak-ms.org/param/enzyme.html
#
enzyme  =       {enzyme}


#
# Scoring algorithm parameters
#
# fragment_bin_offset and fragment_bin_size influence algorithm precision and memory usage.
# They should be set appropriately for the data analyzed.
# For ion trap ms/ms:  1.0005 size, 0.4 offset
# For high res ms/ms:    0.03 size, 0.0 offset
#

fragment_bin_offset     =   {kojak_fragment_bin_offset}     #between 0.0 and 1.0
fragment_bin_size       =   {kojak_fragment_bin_size}   #in Thomsons
ion_series_A            =   {score_a_ions}
ion_series_B            =   {score_b_ions}
ion_series_C            =   {score_c_ions}
ion_series_X            =   {score_x_ions}
ion_series_Y            =   {score_y_ions}
ion_series_Z            =   {score_z_ions}

#
# Additional parameters used in Kojak analysis
#
decoy_filter            =   {decoy_tag}   #identifier for all decoys in the database.
                                    #Default value is "random" (without quotes)
isotope_error           =   {precursor_isotope_range}       #account for errors in precursor peak identification.
                                    #Searches this number of isotope peak offsets.
                                    #Values are 0,1,or 2.
max_miscleavages        =   {max_missed_cleavages}       #number of missed trypsin cleavages allowed
max_peptide_mass        =   {precursor_max_mass}  #largest allowed peptide mass in Daltons
min_peptide_mass        =   {precursor_min_mass}   #lowest allowed peptide mass in Daltons
max_spectrum_peaks      =   {max_accounted_observed_peaks}       #top N peaks to use during analysis. 0 uses all peaks.
ppm_tolerance_pre       =   {precursor_mass_tolerance_plus}    #mass tolerance on precursor when searching
prefer_precursor_pred   =   {kojak_prefer_precursor_pred}       #prefer precursor mono mass predicted by
                                    #instrument software.
                                    #  0 = ignore previous predictions
                                    #  1 = use only previous predictions
                                    #  2 = supplement predictions with additional analysis
spectrum_processing     =   {kojak_spectrum_processing}       #0=no, 1=yes
top_count               =   {kojak_top_count}     #number of top scoring single peptides to combine
                                    #in relaxed analysis
truncate_prot_names     =   {kojak_truncate_prot_names}       #Max protein name character to export, 0=off
turbo_button            =   {kojak_turbo_button}       #Generally speeds up analysis. Special cases cause reverse
                                    #effect, thus this is allowed to be disabled. 0=off
        '''.format(
            **self.params['translations']
            )
        }
        return templates
