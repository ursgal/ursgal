#!/usr/bin/env python
import ursgal
import os


class xtandem_vengeance(ursgal.UNode):
    """
    X!Tandem UNode
    Parameter options at http://www.thegpm.org/TANDEM/api/

    Reference:
    Craig R, Beavis RC. (2004) TANDEM: matching proteins with tandem mass spectra.
    """
    META_INFO = {
        'edit_version'                : 1.00,
        'name'                        : 'X!Tandem',
        'version'                     : 'Vengeance',
        'release_date'                : '2015-12-15',
        'engine_type' : {
            'protein_database_search_engine' : True,
        },
        'input_extensions'            : ['.mgf', '.gaml', '.dta', '.pkl', '.mzData', '.mzXML'],
        'output_extensions'           : ['.xml'],
        'create_own_folder'           : True,
        'in_development'              : False,
        'include_in_git'              : False,
        'distributable'               : True,
        'utranslation_style'          : 'xtandem_style_1',
        'engine' : {
            'darwin' : {
                '64bit' : {
                    'exe'            : 'tandem',
                    'url'            : '',
                    'zip_md5'        : 'b6898f00921f6fbd6b826aa734e4fc44',
                    'additional_exe' : [],
                },
            },
            'linux' : {
                '64bit' : {
                    'exe'            : 'tandem.exe',
                    'url'            : '',
                    'zip_md5'        : 'fb4f06cf5061a0807732530eb9fdd006',
                    'additional_exe' : [],
                },
            },
            'win32' : {
                '64bit' : {
                    'exe'            : 'tandem.exe',
                    'url'            : '',
                    'zip_md5'        : '05fe1e0b4db8ec6d4a7867c563d16597',
                    'additional_exe' : [],
                },
            },
        },
        'citation' :
            'Craig R, Beavis RC. (2004) TANDEM: matching proteins with tandem '
            'mass spectra.',
    }

    def __init__(self, *args, **kwargs):
        super(xtandem_vengeance, self).__init__(*args, **kwargs)
        pass

    def preflight(self):
        '''
        Formatting the command line via self.params

        Input files from format_templates are created in the output folder
        and added to self.created_tmp_files (can be deleted)

        Returns:
            dict: self.params
        '''
        # import pprint
        # pprint.pprint(self.params)
        # exit(1)

        self.params['translations']['mgf_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )

        xml_required = [
            'default_input.xml',
            'taxonomy.xml',
            '15N-masses.xml',
            'input.xml'
        ]
        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        for file_name in xml_required:
            file_info_key = file_name.replace('.xml', '')
            xml_file_path = self.params['translations']['output_file_incl_path'].strip(
                '.xml') + file_name
            self.params['translations'][file_info_key] = xml_file_path
            self.created_tmp_files.append(xml_file_path)
        #
        # building command_list !
        #
        self.params['command_list'] = [
            self.exe,
            '{input}'.format(**self.params['translations']),
        ]

        if self.params['translations']['label'] == '15N':
            self.params['translations'][
                '15N_default_input_addon'] = '<note label="protein, modified residue mass file" type="input">{15N-masses}</note>'.format(**self.params['translations'])
            # translations['protein, modified residue mass file']['label'] = \
            #     '<note label="protein, modified residue mass file" type="input">{15N-masses}</note>'.format(**self.params['translations'])
        else:
            self.params['translations'][
                '15N_default_input_addon'] = '<note label="protein, modified residue mass file" type="input">no</note>'
            # translations['protein, modified residue mass file']['label'] = \
            #     '<note label="protein, modified residue mass file" type="input">no</note>'

        # modifications
        potential_mods = []
        refine_potential_mods = []
        fixed_mods = []
        self.params['translations']['Prot-N-term'] = 0.0
        self.params['translations']['Prot-C-term'] = 0.0
        for mod in self.params['mods']['fix']:
            if mod['pos'] == 'N-term':
                mod['aa'] = '['
            elif mod['pos'] == 'C-term':
                mod['aa'] = ']'

            fixed_mods.append(
                '{0}@{1}'.format(mod['mass'], mod['aa'])
            )

        self.params['translations']['acetyl_N_term'] = 'no'
        self.params['translations']['pyro_glu'] = 'no'
        pyro_glu = 0
        potentially_modified_aa = set()
        for mod in self.params['mods']['opt']:
            if mod['aa'] == '*' and mod['name'] == 'Acetyl' and mod['pos'] == 'Prot-N-term' :
                self.params['translations']['acetyl_N_term'] = 'yes'
                continue
            if mod['aa'] == '*' and mod['name'] == 'Gln->pyro-Glu' and mod['pos'] == 'Pep-N-term' :
                pyro_glu += 1
                continue
            if mod['aa'] == '*' and mod['name'] == 'Glu->pyro-Glu' and mod['pos'] == 'Pep-N-term' :
                pyro_glu += 1
                continue
            for term in ['Prot-N-term', 'Prot-C-term']:
                if mod['pos'] == term:
                    if mod['aa'] == '*':
                        if self.params['translations'][term] != 0.0:
                            print(
                                '''
[ WARNING ] X!Tandem does not allow two mods on the same position {1}
[ WARNING ] Continue without modification {0} '''.format(mod, term, **mod)
                            )
                            continue
                        else:
                            self.params['translations'][term] = mod['mass']
                    else:
                        print(
                            '''
[ WARNING ] X!Tandem does not support specific amino acids for terminal modifications
[ WARNING ] Continue without modification {0} '''.format(mod, term, **mod)
                        )
                        continue
            if mod['aa'] in potentially_modified_aa:
                print(
                    '''
[ WARNING ] X!Tandem does not allow two potential mods on the same aminoacid!
[ WARNING ] Continue without modification {0} '''.format(mod, **mod)
                )
                continue
            else:
                forbidden_cterm = ''
                max_num_per_mod_name_specific = ''
                if mod['name'] in self.params['translations']['forbidden_cterm_mods']:
                    forbidden_cterm = ']'
                if mod['name'] in self.params['translations']['max_num_per_mod_name_specific'].keys():
                    max_num_per_mod_name_specific = self.params['translations'][
                        'max_num_per_mod_name_specific'][mod['name']]

                if mod['pos'] == 'N-term':
                    mod['aa'] = '['
                elif mod['pos'] == 'C-term':
                    mod['aa'] = ']'

                potential_mods.append(
                    '{0}@{1}{2}{3}'.format(
                        mod['mass'],
                        max_num_per_mod_name_specific,
                        forbidden_cterm,
                        mod['aa'],
                    )
                )
                potentially_modified_aa.add(mod['aa'])

        if pyro_glu == 2:
            self.params['translations']['pyro_glu'] = 'yes'
        if pyro_glu == 1:
            print('''
[ WARNING ] X!Tandem looks for Gln->pyro-Glu and Glu->pyro-Glu
[ WARNING ] at the same time, please include both or none
[ WARNING ] Continue without modification {0} '''.format(mod, **mod)
                  )
        self.params['translations']['fixed_modifications'] = ','.join(
            fixed_mods
        )
        self.params['translations']['potential_modifications'] = ','.join(
            potential_mods
        )
        self.params['translations']['refine_potential_modifications'] = ','.join(
            refine_potential_mods
        )

        for ion in ['a', 'b', 'c', 'x', 'y', 'z']:
            if ion in self.params['translations']['score_ion_list']:
                self.params['translations'][
                    'score_{0}_ions'.format(ion)] = 'yes'
            else:
                self.params['translations'][
                    'score_{0}_ions'.format(ion)] = 'no'

        templates = self.format_templates()
        for file_name, content in templates.items():
            if file_name == '15N-masses.xml' and self.params['translations']['label'] == '14N':
                continue
            xml_file_path = self.params['translations']['output_file_incl_path'].strip(
                '.xml') + file_name
            with open(xml_file_path, 'w') as out:
                print(content, file=out)
                self.print_info(
                    'Wrote input file {0}'.format(file_name),
                    caller='preflight'
                )

                self.created_tmp_files.append(xml_file_path)
        return self.params

    def postflight(self):
        # convert_xtandemXML_to_identcsv( self.params )
        pass

    def format_templates(self):
        '''Returns formatted X!Tandem input files

        The formating is taken from self.params

        Returns:
            dict: keys are the names of the three templates (15N-masses.xml, taxonomy.xml, input.xml)

        '''
        templates = {
            '15N-masses.xml' :
'''<?xml version="1.0"?>
    <bioml title="peptide residue molecular mass values for an all 15N organisms">
        <aa type="A" mass="72.034148698" />
        <aa type="B" mass="116.036998" />
        <aa type="C" mass="104.006219398" />
        <aa type="D" mass="116.023977958" />
        <aa type="E" mass="130.039628028" />
        <aa type="F" mass="148.065448838" />
        <aa type="G" mass="58.018498628" />
        <aa type="H" mass="140.050016555" />
        <aa type="I" mass="114.081098908" />
        <aa type="J" mass="0.0" />
        <aa type="K" mass="130.089032837" />
        <aa type="L" mass="114.081098908" />
        <aa type="M" mass="132.037519538" />
        <aa type="N" mass="116.036997257" />
        <aa type="O" mass="0.0" />
        <aa type="P" mass="98.049798768" />
        <aa type="Q" mass="130.052647327" />
        <aa type="R" mass="160.089250624" />
        <aa type="S" mass="88.029063328" />
        <aa type="T" mass="102.044713398" />
        <aa type="V" mass="100.065448838" />
        <aa type="W" mass="188.073382767" />
        <aa type="X" mass="112.057034" />
        <aa type="Y" mass="164.060363468" />
        <aa type="Z" mass="130.052648" />
        <molecule type="NH3" mass="18.02358311" />
        <molecule type="H2O" mass="18.01056470" />
    </bioml>
''',
            # -------------------------
            # -------------------------
            'taxonomy.xml' :
'''<?xml version='1.0' encoding='iso-8859-1'?>
    <bioml label="x! taxon-to-file matching list">
        <taxon label="{database_taxonomy}">
            <file URL="{database}" format="peptide" />
        </taxon>
    </bioml>
'''.format(**self.params['translations']),
            # -------------------------
            # -------------------------
            'input.xml' :
'''<?xml version='1.0' encoding='iso-8859-1'?>
    <bioml>
        <note label="list path, default parameters" type="input">{default_input}</note>
        <note label="list path, taxonomy information" type="input">{taxonomy}</note>
        <note label="spectrum, path" type="input">{mgf_input_file}</note>
        <note label="output, path" type="input">{output_file_incl_path}</note>
    </bioml>'''.format( **self.params['translations'] ),

            'default_input.xml' : 
'''<?xml version='1.0' encoding='iso-8859-1'?>
    <bioml label="ursgal">
    <note type="heading">

        Spectrum general

    </note>
    <note type="input" label="spectrum, parent monoisotopic mass error plus">{precursor_mass_tolerance_plus}</note>
    <note type="input" label="spectrum, parent monoisotopic mass error minus">{precursor_mass_tolerance_minus}</note>
    <note type="input" label="spectrum, parent monoisotopic mass error units">{precursor_mass_tolerance_unit}</note>
    <note type="input" label="spectrum, parent monoisotopic mass isotope error">{precursor_isotope_range}</note>
    <note type="input" label="spectrum, minimum parent m+h">{precursor_min_mass}</note>

    <note type="input" label="spectrum, fragment mass type">{frag_mass_type}</note>
    <note type="input" label="spectrum, fragment monoisotopic mass error">{frag_mass_tolerance}</note>
    <note type="input" label="spectrum, fragment monoisotopic mass error units">{frag_mass_tolerance_unit}</note>
    <note type="input" label="spectrum, fragment mass error">{frag_mass_tolerance}</note>
    <note type="input" label="spectrum, fragment mass error units">{frag_mass_tolerance_unit}</note>
    <note type="heading">

        Spectrum conditioning

    </note>
    <note type="input" label="spectrum, dynamic range">{spec_dynamic_range}</note>
    <note type="input" label="spectrum, total peaks">{max_accounted_observed_peaks}</note>
    <note type="input" label="spectrum, use neutral loss window">{neutral_loss_enabled}</note>
    <note type="input" label="spectrum, neutral loss window">{neutral_loss_window}</note>
    <note type="input" label="spectrum, neutral loss mass">{neutral_loss_mass}</note>
    <note type="input" label="spectrum, minimum fragment mz">{frag_min_mz}</note>
    <note type="input" label="spectrum, minimum peaks">{min_required_observed_peaks}</note>
    <note type="input" label="spectrum, threads">{cpus}</note>
    <note type="input" label="spectrum, sequence batch size" >{batch_size}</note>
    <note type="heading">

        Residue modification

    </note>
    <note type="input" label="residue, modification mass">{fixed_modifications}</note>
    <note type="input" label="residue, potential modification mass">{potential_modifications}</note>
    <note type="heading">

        Protein general

    </note>
    <note type="input" label="protein, taxon">{database_taxonomy}</note>
    <note type="input" label="protein, cleavage site">{enzyme}</note>
    <note type="input" label="protein, cleavage C-terminal mass change">{cleavage_cterm_mass_change}</note>
    <note type="input" label="protein, cleavage N-terminal mass change">{cleavage_nterm_mass_change}</note>
    <note type="input" label="protein, cleavage semi">{semi_enzyme}</note>
    <note type="input" label="protein, N-terminal residue modification mass">{Prot-N-term}</note>
    <note type="input" label="protein, C-terminal residue modification mass">{Prot-C-term}</note>
    <note type="input" label="protein, ptm complexity">{max_mod_alternatives}</note>
    <note type="input" label="protein, quick acetyl" >{acetyl_N_term}</note>
    <note type="input" label="protein, quick pyrolidone" >{pyro_glu}</note>
    <note type="input" label="protein, saps" >{search_for_saps}</note>
    <note type="input" label="protein, stP bias" >{xtandem_stp_bias}</note>
    {15N_default_input_addon}
    <note type="heading">

        Scoring

    </note>
    <note type="input" label="scoring, a ions">{score_a_ions}</note>
    <note type="input" label="scoring, b ions">{score_b_ions}</note>
    <note type="input" label="scoring, c ions" >{score_c_ions}</note>
    <note type="input" label="scoring, minimum ion count">{min_required_matched_peaks}</note>
    <note type="input" label="scoring, maximum missed cleavage sites">{max_missed_cleavages}</note>
    <note type="input" label="scoring, cyclic permutations" >{compensate_small_fasta}</note>
    <note type="input" label="scoring, include reverse" >{engine_internal_decoy_generation}</note>
    <note type="input" label="scoring, x ions" >{score_x_ions}</note>
    <note type="input" label="scoring, y ions" >{score_y_ions}</note>
    <note type="input" label="scoring, z ions" >{score_z_ions}</note>
    <note type="heading">

        Model refinement parameters

    </note>
    <note type="input" label="refine">{use_refinement}</note>
    <note type="input" label="refine, spectrum synthesis">no</note>
    <note type="input" label="refine, maximum valid expectation value">0.1</note>
    <note type="input" label="refine, potential N-terminus modifications"></note>
    <note type="input" label="refine, unanticipated cleavage">no</note>
    <note type="input" label="refine, potential modification mass">{refine_potential_modifications}</note>
    <note type="input" label="refine, use potential modifications for full refinement">no</note>
    <note type="input" label="refine, point mutations">no</note>
    <note type="heading">

        Output

    </note>
    <note type="input" label="output, path hashing">no</note>
    <note type="input" label="output, xsl path">tandem-style.xsl</note>
    <note type="input" label="output, parameters">yes</note>
    <note type="input" label="output, performance">yes</note>
    <note type="input" label="output, spectra">yes</note>
    <note type="input" label="output, histograms">yes</note>
    <note type="input" label="output, proteins">yes</note>
    <note type="input" label="output, sequences">yes</note>
    <note type="input" label="output, results">all</note>
    <note type="input" label="output, maximum valid expectation value">{max_output_e_value}</note>
    <note type="input" label="output, histogram column width">30</note>
    <note type="input" label="output, mzid">{output_file_type}</note>
    </bioml>'''.format(**self.params['translations'])
        }
        return templates
