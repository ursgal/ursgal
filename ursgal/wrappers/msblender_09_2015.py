#!/usr/bin/python

from __future__ import print_function
from __future__ import division
import os
import os.path
import sys
import csv
import math
import subprocess
from pprint import pprint
import ursgal


class msblender_09_2015( ursgal.UNode ):
    """
    MSblender UNode
    Documentation at http://www.marcottelab.org/index.php/MSblender
    """
    META_INFO = {
        'edit_version'       : 1.00,
        'name'               : 'MSblender',
        'version'            : '09.2015',
        'release_date'       : '2015-9-1',
        'engine_type' : {
            'meta_engine' : True,
        },
        'input_extensions'   : ['.csv'],
        'output_extensions'  : ['.csv'],
        'in_development'     : True,
        'create_own_folder'  : False,
        'include_in_git'     : False,
        'distributable'      : False,
        'utranslation_style' : 'msblender_style_1',
        'engine' : {
            'linux' : {
                '64bit' : {
                    'exe'            : 'msblender',
                    'url'            : '',
                    'zip_md5'        : None,
                    'additional_exe' : [],
                },
            },
            'darwin' : {
                '64bit' : {
                    'exe'            : 'msblender',
                    'url'            : '',
                    'zip_md5'        : None,
                    'additional_exe' : [],
                },
            },
        },
        'citation' : \
            'Kwon T, Choi H, Vogel C, Nesvizhskii AI, Marcotte EM. (2011) '\
            'MSblender: A Probabilistic Approach for Integrating Peptide '\
            'Identifications from Multiple Database Search Engines.',
    }

    def __init__( self, *args, **kwargs ):
        super(msblender_09_2015, self).__init__(*args, **kwargs)

        self.RT_lookup = {}

        return


    def preflight( self ):
        '''
        Formatting the command line via self.params

        Settings file is created in the output folder
        and added to self.created_tmp_files (can be deleted)

        Returns:

            self.params(dict)

        http://www.marcottelab.org/index.php/MSblender#Pre-processing
        '''

        # first, make sure that the msblender input generation script is
        # in the same path as the executable :
        exe_dir = os.path.dirname( self.exe )
        make_msblender_in_py_path = os.path.join(
            exe_dir, "make-msblender_in.py"
        )
        assert os.path.isfile( make_msblender_in_py_path ), '''
            The MSblender python script 'make-msblender_in.py'
            was not found in {}'''.format( exe_dir )
        self.params["make-msblender_in"] = make_msblender_in_py_path

        self.params['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        self.params["input_files"]         = []
        self.params["engine_names"]        = []
        self.params["engine_column_names"] = []
        self.params["evalue_column_names"] = []
        for input_file_dict in self.params["input_file_dicts"]:
            search_engine  = input_file_dict["last_search_engine"]
            score_colname  = input_file_dict["last_search_engine_colname"]
            input_file_path = os.path.join(
                input_file_dict['dir'],
                input_file_dict['file']
            )
            evalue_colname = self.meta_unodes[ search_engine ].DEFAULT_PARAMS['evalue_field']
            self.params["engine_names"].append( search_engine )
            self.params["engine_column_names"].append( score_colname )
            self.params["evalue_column_names"].append( evalue_colname )
            self.params["input_files"].append( input_file_path )


        print('Converting ident CSVs to MSblender "logE hit list" format...')
        msbl_hit_files = []
        for i, ident_csv in enumerate( self.params["input_files"] ):
            print( "Converting file {0} of {1}...".format(
                i+1, len(self.params["input_files"]))
            )
            f = self.convert_ursgal_csv_to_msblender_input( ident_csv )
            msbl_hit_files.append( f )

        print('Generating MSblender config file...')
        self.params["msblender_conf"] = \
            self.make_msblender_config_file( msbl_hit_files )


        command_list_to_generate_input = [
            'python2.7',
            '{make-msblender_in}'.format(**self.params),  # path to make-msblender_in.py
            '{msblender_conf}'.format(**self.params),     # path to msblender_conf file
        ]

        print( 'Generating MSblender input file via command line call:' )
        print( '$ ' + ' '.join( command_list_to_generate_input ) )
        print()
        proc = subprocess.Popen(
            command_list_to_generate_input,
            stdout=subprocess.PIPE,
        )
        for line in proc.stdout:
            print(line.strip().decode('utf'))


        # make-msblender_in.py should have produced an input file with this name:
        msblender_input_file_path = \
            self.params["msblender_conf"] + ".msblender_in"
        assert os.path.isfile( msblender_input_file_path ), '''
            MSblender input file could not be found at that path:
            {}'''.format( msblender_input_file_path)
        self.params["msblender_in"] = msblender_input_file_path

        self.params["command_list"] = [
            self.exe,                                # path to msblender executable
            '{msblender_in}'.format(**self.params),  # path to msblender_in file
        ]


    def postflight( self ):
        # check if msblender output file was sucessfully created or not
        self.params["msblender_out"] = \
            self.params["msblender_in"] + ".msblender_out"
        assert os.path.isfile( self.params["msblender_out"] ), "MSblender output file was not found."
        msg = "MSblender output file successfully created: {msblender_out}"
        print( msg.format( **self.params ) )

        print( "\nFormatting MSblender output file..." )
        output_file = self.convert_msblender_out( self.params["msblender_out"] )
        print( "MSblender Summary CSV created: {output_file_incl_path}".format(**self.params) )


    def make_msblender_config_file( self, msblender_input_files ):
        '''
        MSblender needs a config file of this format:
            MyriMatch:       test.myrimatch.mvh_hit_list_best
            X!Tandem:        test.tandem_k.logE_hit_list_best
            ...
        This function generates that file.
        '''
        config_file_path = self.params['output_file_incl_path'] + ".msblender_conf"

        with open( config_file_path, "w" ) as cfg_file:
            for i, msb_file in enumerate( msblender_input_files ):

                search_engine = self.params["engine_names"][ i ]

                line = "    ".join( [ search_engine, msb_file ] )
                cfg_file.write( line + "\n" )

        self.created_tmp_files.append( config_file_path )  # mark for deletion

        return config_file_path


    def convert_ursgal_csv_to_msblender_input( self, csv_file ):
        '''
        csv_file: search engine output file, converted to csv
            using ursgal

        generates a new csv in msblender "hit_list" format
        (see http://www.marcottelab.org/index.php/MSblender#Pre-processing )
        with the same name as input file, but file extension
        replaced with ".msblender_input"
        '''

        output_header = [
            "#Spectrum_id",
            "Charge",
            "PrecursorMz",
            "MassDiff",
            "Peptide",
            "Protein",
            "MissedCleavages",
            "Score(-log10[E-value])",
        ]

        msblender_decoy_tag = 'xf_'  # msblender interprets a hit as
                        # decoy if spectrum ID starts with this tag,
                        # so we have to mark our decoys with this tag!

        #basename   = os.path.basename( csv_file )
        #fname, ext = os.path.splitext( basename )

        converted_file = csv_file + ".msblender_input"

        with open( csv_file , "r") as in_f:
            rows = (line for line in in_f if not line.startswith("#"))
            reader = csv.DictReader( rows )
            with open( converted_file, "w" ) as out_f:
                writer = csv.DictWriter(
                    out_f, output_header, delimiter='\t'
                )

                writer.writeheader()
                for in_row in reader:

                    # only consider 'the best' PSM for each spectrum
                    if "rank" in in_row:
                        if int(in_row["rank"]) != 1:
                            continue
                    # same effect as 'select-best-PSM.py' from msblender

                    out_row = {}

                    sequence          = in_row["Sequence"]
                    mods              = in_row["Modifications"]
                    spec_title        = in_row["Spectrum Title"]
                    basename          = spec_title.split(".")[0]
                    spec_id_start     = int(spec_title.split(".")[ 1])
                    spec_id_stop      = int(spec_title.split(".")[ 2])
                    input_file_charge = int(spec_title.split(".")[-1])
                    charge            = in_row["Charge"]

                    out_row["Peptide"]      = "#".join( [sequence, mods] )
                    out_row["#Spectrum_id"] = spec_title
                    out_row["Charge"]       = charge

                    out_row["PrecursorMz"] = \
                        in_row["Exp m/z"]

                    out_row["MassDiff"] = \
                        abs(
                            float(in_row["Exp m/z"])
                            - float(in_row["Calc m/z"])
                            )

                    prot_ID = in_row["proteinacc_start_stop_pre_post_;"]
                    if in_row["Is decoy"] == "true" or "decoy" in prot_ID:
                        out_row["Protein"] = msblender_decoy_tag + prot_ID
                    else:
                        out_row["Protein"] = prot_ID

                    RandK = [ aa for aa in sequence[:-1] if aa in ["R","K"] ]
                    out_row["MissedCleavages"] = len( RandK )

                    for e in self.params["evalue_column_names"]:
                        if e in in_row:
                            evalue = float( in_row[ e ] )
                            # no log can be calculated for evalues that are supposedly
                            # zero so they are replaced with evalues of a very small value
                            # (converters by the msblender team use the same fix)
                            if evalue == 0.0:
                                evalue = 1e-15

                    out_row["Score(-log10[E-value])"] = -math.log10( evalue )


                    # noting down some PSM information in a lookup dict, we need
                    # this info later when the final output file is generated
                    for spec_id in set([spec_id_start, spec_id_stop]):
                        # msblender output doesn't have start+stop, so we note down both, just in case
                        PSM  = ( sequence, basename, spec_id, input_file_charge )
                        info = ( in_row["Retention Time (s)"], in_row["proteinacc_start_stop_pre_post_;"] )
                        self.RT_lookup[ PSM ] = info


                    writer.writerow( out_row )

        self.created_tmp_files.append( converted_file )  # mark for deletion

        return converted_file


    def convert_msblender_out( self, msblender_out ):
        '''
        Format the MSblender output csv to match our standards.
        It should look just like the combine_FDR output csv.
        Also adds the estimated FDR for each hit!
        '''
        msblender_converted_out = self.params["output_file_incl_path"]

        # mapping the msblender score column names to the ones that we want in our output csv,
        # i.e. { 'xtandem_score' : 'X\!Tandem:MSblender_score' }
        score_colname_map = {}
        for i, engine in enumerate( self.params["engine_names"] ):
            msbl_score_colname = engine + "_score"
            pretty_engine_name = self.params["engine_column_names"][ i ]
            new_score_colname  = "".join( [
                "MSblender:",
                pretty_engine_name,
                ":score"
            ] )  # i.e. "MSblender:MyriMatch_score"
            score_colname_map[ msbl_score_colname ] = new_score_colname

        out_header = ["Spectrum ID",
                      "Sequence",
                      "Modifications",
                      "MSblender:mvScore",
                      "Charge",
                      "Retention Time (s)",
                      "Engines",
                      "Is decoy",
                      "Estimated FDR",
        ]
        out_header += list( score_colname_map.values() )
        out_header.append( "proteinacc_start_stop_pre_post_;" )

        # these counters will be used for FDR calculation:
        PSM_count   = 0
        decoy_count = 0

        with open( msblender_out, "r" ) as msblout:
            reader = csv.DictReader( msblout, delimiter='\t' )
            with open( msblender_converted_out, "w" ) as out:
                writer = csv.DictWriter( out, out_header )
                writer.writeheader()

                # sorting the csv by score to allow FDR calculation while iterating
                # sorting in reverse since a bigger mvScore is better
                # (it's the "posterior probability of correct identification", see paper)
                sorted_reader = sorted(
                    reader,
                    key = lambda x: float(x["mvScore"]),
                    reverse=True,
                )

                for in_row in sorted_reader:

                    msblender_score = in_row["mvScore"]

                    if float(msblender_score) > self.DEFAULT_PARAMS['FDR_cutoff']:
                        continue

                    if in_row["Decoy"] == "D":
                        is_decoy = "true"
                    elif in_row["Decoy"] == "F":
                        is_decoy = "false"
                    else:
                        raise ValueError('''
                            "Decoy"-column info is missing from MSblender output row!
                            It should be either "D" or "R"!
                            ''')

                    #    desired output format:
                    # Spectrum ID   Sequence  Modifications    Charge  Retention Time (s)
                    # Engines  Is decoy   X\!Tandem:PEP   OMSSA:PEP   proteinacc_start_stop_pre_post_;

                    spec           = in_row["Spectrum"]
                    spec_tokens    = spec.split(".")
                    spec_id        = int( spec_tokens[-3] )
                    charge         = spec_tokens[ -2 ]
                    sequence, mods = spec_tokens[ -1 ].split("#")
                    basename       = spec_tokens[  0 ]

                    out_row = {}

                    out_row["MSblender:mvScore"] = msblender_score
                    out_row["Spectrum ID"]       = spec_id
                    out_row["Charge"]            = charge
                    out_row["Sequence"]          = sequence
                    out_row["Modifications"]     = mods
                    out_row["Is decoy"]          = is_decoy

                    PSM  = ( sequence, basename, spec_id, int(charge) )
                    RT, proteinacc = self.RT_lookup[ PSM ]

                    out_row["Retention Time (s)"]               = RT
                    out_row["proteinacc_start_stop_pre_post_;"] = proteinacc

                    engines_list = []  # list indicating which engines found the PSM
                    for u_score, m_score in score_colname_map.items():
                        out_row[ m_score ] = in_row[ u_score ]
                        if in_row[ u_score ] != "":
                            engines_list.append(
                                m_score.split(":")[1]
                                # MSblender:MyriMatch:score -> MyriMatch
                            )
                    out_row["Engines"] = ";".join( engines_list )

                    # estimating the FDR for each row:
                    PSM_count += 1
                    if is_decoy == 'true':
                        decoy_count += 1
                    # calculate and store the estimated FDR for each identification
                    out_row['Estimated FDR'] = self.calc_FDR ( PSM_count, decoy_count )

                    writer.writerow( out_row )

        self.created_tmp_files.append( msblender_converted_out )  # mark for deletion

        return msblender_converted_out


    def calc_FDR ( self, PSM_count, false_positives ):
        '''
        calculate false discovery rate according to FDR Method 2
        (Käll et al. 2008) as explained by Jones et al. 2009
        '''
        true_positives  = PSM_count - (2 * false_positives)
        if true_positives <= 0:  # prevent FDR above 1. Not sure if this is done?
            return 1.0
        FDR = false_positives / ( false_positives + true_positives)
        return FDR


    def add_estimated_FDR( self, csv_rowlist ):
        '''
        Adding the estimated FDR (based on # of decoys).
        based on Jones et al. 2009: Algorithm 2, step 3
        careful, input file must be sorted by average score (low->high) already!
        '''

        # In certain datasets, decoy hits are not
        # observed at any score threshold for identifications made by all
        # three search engines. To correct for the size of the result set, an
        # artificial decoy hit is added at the end of each data series, such
        # that no identification has a combined FDR/PEP Score = 0.
        artificial_decoy = [ {'Is decoy' : 'true'} ]

        PSM_count   = 0
        decoy_count = 0

        # Traverse identifications from lowest AFS to highest:
        for row in csv_rowlist + artificial_decoy:
            PSM_count += 1

            if row['Is decoy'] == 'true':
                decoy_count += 1

            # calculate and store the estimated FDR (FDRest) for each identification according to FDR Method 2.
            row['Estimated FDR']  = calc_FDR ( PSM_count, decoy_count )
            row['_decoy_percent'] = decoy_count / PSM_count


if __name__ == "__main__":

    m = msblender_09_2015()

    #m.params = {
        #"output_file"          : "./msblender_final_output.csv",
        #"folder"               : ".",
        #"basename"             : "120813OTc1_NQL-AU-0314-LFQ-LCM-SG-04_048_14N",
        #"input_files"    : [     # merged ident csv files:
            #"14N_msgfplus_v9979_merged.csv",
            #"14N_myrimatch_2_1_138_merged.csv",
            #"14N_omssa_2_1_9_merged.csv",
            #"14N_xtandem_sledgehammer_merged.csv",
            #],
        #"score_fields"   : {
            #"xtandem"    : "X\!Tandem:whatever",
            #"omssa"      : "OMSSA:bla",
            #"msgfplus"   : "MS-GF+:whatever",
            #"myrimatch"  : "MyriMatch:doesnmatter",
            #},
        #"FDR_cutoff" : 0.01,
        #}

    m.exe = "./msblender"

    m.preflight()
    m._execute()
    m.postflight()
