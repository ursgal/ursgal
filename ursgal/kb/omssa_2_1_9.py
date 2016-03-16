META_INFO = {
     'engine_type'            : {
        'controller'        : False,
        'converter'         : False,
        'validation_engine' : False,
        'search_engine'     : True,
        'meta_engine'       : False
    },
    'engine': {
        'darwin' : {
            '64bit' : {
                'exe'            : 'omssacl',
                'url'            : 'ftp://ftp.ncbi.nih.gov/pub/lewisg/omssa/2.1.9/omssa-2.1.9.macos.tar.gz',
                'zip_md5'        : '9cb92a98c4d96c34cc925b9336cbaec7',
                'additional_exe' : ['makeblastdb'],
            },
        },
        'linux' : {
            '64bit' : {
                'exe'            : 'omssacl',
                'url'            : 'ftp://ftp.ncbi.nih.gov/pub/lewisg/omssa/2.1.9/omssa-2.1.9.linux.tar.gz',
                'zip_md5'        : '921e01df9cd2a99d21e9a336b5b862c1',
                'additional_exe' : ['makeblastdb'],
            },
        },
        'win32' : {
            '64bit' : {
                'exe'            : 'omssacl.exe',
                'url'            : 'ftp://ftp.ncbi.nih.gov/pub/lewisg/omssa/2.1.9/omssa-2.1.9.win32.exe',
                'zip_md5'        : 'b9d9a8aec3cfe77c48ce0f5752aba8f9',
                'additional_exe' : ['makeblastdb'],
            },
            '32bit' : {
                'exe'            : 'omssacl.exe',
                'url'            : 'ftp://ftp.ncbi.nih.gov/pub/lewisg/omssa/2.1.9/omssa-2.1.9.win32.exe',
                'zip_md5'        : 'a05a5cdd45fd8abcfc75b1236f8a2390',
                'additional_exe' : ['makeblastdb'],
            },
        },
    },
    'input_types'               : ['.mgf'],
    'output_extension'          : '.csv',
    'create_own_folder'         : True,
    'citation'                  : 'Geer LY, Markey SP, Kowalak JA, '\
        'Wagner L, Xu M, Maynard DM, Yang X, Shi W, Bryant SH (2004) '\
        'Open Mass Spectrometry Search Algorithm.',

    'include_in_git'            : False,
}

DEFAULT_PARAMS = {
    'validation_score_field'    : 'OMSSA:pvalue',
    'evalue_field'              : 'OMSSA:evalue',
    'validation_minimum_score'  : 1e-30,
    'bigger_scores_better'      : False,  # lower score are better p-value,
    # ---------------------------------------------------------------------
    # the following parameters are not changeable, e.g. default
    # protein/taxon
    'x': '0',  # default, all taxids, we dont want to change this
    'omssa_output_type' : '-oc',
    # ions
    'sct': '0',   # search c terminal ions?, same as sGUI default, 0=yes, 1=no
    'sb1': '1',   # should first forward (b1) product ions be in search (1=no)
    'sp': '0',  # max number of ions in each series being searched (0=all)

    # precursor
    'z1': '0.95',  # default, fraction of peaks below precursor used to determine if spectrum is charge 1
    'zcc': '2',  # how should precursor charges be determined?, use a range
    'tez': '1',  # defautl is 0 (disabled), charge dependency of precursor mass tolerance (0 = none, 1 = linear)
    'pc': '1',  # minimum number of precursors that match a spectrum

    # product
    'zoh': '4',  # maximum product charge to search, default is 2, sGUI:2
    'zt': '3',  # default,minimum precursor charge to start considering multiply charged products

    # charge
    'zc': '1',  # should charge plus one be determined algorithmically? (1=yes)

    # scoring
    'scorr': '0',  # turn off correlation correction to score (1=off, 0=use correlation)
    'scorp': '0.5',  # same as sGUI, probability of consecutive ion (used in correlation correction)
    'he': '1.0',  # the maximum evalue allowed in the hit list, cant find in search GUI

    # spectrum
    'ht': '6',  # number of m/z values corresponding to the most intense peaks that must include one match to the theoretical peptide
    'cl': '0.0',  # low intensity cutoff as a fraction of max peak,
    'cp': '0',  # eliminate charge reduced precursors in spectra (0=no, 1=yes)

    # window
    'h2': '2',  # number of peaks allowed in double charge window
    'h1': '2',  # number of peaks allowed in single charge window (0 = number of ion species)
    'w1': '27',   # default is 27, also in sGUI, single charge window in Da
    'w2': '14',  # double charge window in Da, default

    # mass
    'ta': '1.0',  # default value, cant find in sGUI self.params, automatic mass tolerance adjustment fraction
    'tex': '1446.94',  # threshold in Da above which the mass of neutron should be added in exact   mass search
    'mm': '128',  # the maximum number of mass ladders to generate per database peptide
    'hl':'30',

}

USEARCH_PARAM_KEY_VALUE_TRANSLATOR = {
    'score_a_ions'           : {True : '0', False : ''},
    'score_b_ions'           : {True : '1', False : ''},
    'score_c_ions'           : {True : '2', False : ''},
    'score_x_ions'           : {True : '3', False : ''},
    'score_y_ions'           : {True : '4', False : ''},
    'score_z_ions'           : {True : '5', False : ''},

    'search_c_terminal_ions' : {True : '1', False : '0'},
    'search_first_b1_ion'    : {True : '0', False : '1'},
    'precursor_isotope_range': {'0':'0','0,1':'1','0,2':'2'}
}

USEARCH_PARAM_VALUE_TRANSLATIONS = {
    #enzymes
    'trypsin'              : '0',
    'argc'                 : '1',
    'cnbr'                 : '2',
    'chymotrypsin'         : '3',
    'formic_acid'          : '4',
    'lysc'                 : '5',
    'lysc_p'               : '6',
    'pepsina'              : '7',
    'trypsin_cnbr'         : '8',
    'trypsin_chymotrypsin' : '9',
    'trypsin_p'            : '10',
    'no_cleavage'          : '11',
    'aspn'                 : '12',
    'gluc'                 : '13',
    'aspn_gluc'            : '14',
    'top_down'             : '15',
    'semi_tryptic'         : '16',
    'nonspecific'          : '17',
    'chymotrypsin_p'       : '18',
    'lysn'                 : '21',
    'thermolysin_p'        : '22',
    'semi_chymotrypsin'    : '23',
    'semi_gluc'            : '24',

    #label
    # '15N'                : '2',
    # '14N'                : '0',
    # OMSSA CSV Header madness
    'Spectrum number'      : 'Spectrum ID',
    ' Filename/id'         : 'Spectrum Title',
    ' Peptide'             : 'Sequence',
    ' E-value'             : 'OMSSA:evalue',
    ' Mass'                : 'Exp m/z',
    ' gi'                  : 'gi',
    ' Accession'           : 'Accession',
    ' Start'               : 'Start',
    ' Stop'                : 'Stop',
    ' Defline'             : 'proteinacc_start_stop_pre_post_;',
    ' Mods'                : 'Modifications',
    ' Charge'              : 'Charge',
    ' Theo Mass'           : 'Calc m/z',
    ' P-value'             : 'OMSSA:pvalue',
    ' NIST score'          : 'NIST score',

}

USED_USEARCH_PARAMS = set([
    'database',
    'modifications',
    'num_match_spec',
    'precursor_min_charge',
    'precursor_max_charge',
    'maximum_missed_cleavages',
    'precursor_mass_tolerance_minus',
    'precursor_mass_tolerance_plus',
    'frag_mass_tolerance',
    'frag_mass_tolerance_unit',
    'enzyme',
    'score_a_ions',
    'score_b_ions',
    'score_c_ions',
    'score_x_ions',
    'score_y_ions',
    'score_z_ions',
    'mininimal_required_observed_peaks',
    'precursor_isotope_range',
    'label',
    'validation_score_field',
    'evalue_field',
    'validation_minimum_score',
    'bigger_scores_better',
    'x',
    'omssa_output_type',
    'sct',
    'sb1',
    'sp',
    'z1',
    'zcc',
    'tez',
    'pc',
    'zoh',
    'zt',
    'zc',
    'scorr',
    'scorp',
    'he',
    'ht',
    'cl',
    'cp',
    'h2',
    'h1',
    'w1',
    'w2',
    'ta',
    'tex',
    'mm',
    'hl',
    'semi_enzyme',
    'base_mz'
])


    #  Trypsin: 0
    # Arg-C: 1
    # CNBr: 2
    # Chymotrypsin (FYWL): 3
    # Formic Acid: 4
    # Lys-C: 5
    # Lys-C, no P rule: 6
    # Pepsin A: 7
    # Trypsin+CNBr: 8
    # Trypsin+Chymotrypsin (FYWLKR): 9
    #  Trypsin, no P rule:10
    #  Whole protein:11
    #  Asp-N:12
    #  Glu-C:13
    #  Asp-N+Glu-C:14
    #  Top-Down:15
    #  Semi-Tryptic:16
    #  No Enzyme:17
    #  Chymotrypsin, no P rule (FYWL):18
    #  Asp-N (DE):19
    #  Glu-C (DE):20
    #  Lys-N (K):21
    #  Thermolysin, no P rule:22
    #  Semi-Chymotrypsin (FYWL):23
    #  Semi-Glu-C:24

# USAGE
# omssacl [-h] [-help] [-xmlhelp] [-pm param] [-d blastdb] [-umm] [-f infile]
# [-fx xmlinfile] [-fb dtainfile] [-fp pklinfile] [-fm pklinfile]
# [-foms omsinfile] [-fomx omxinfile] [-fbz2 bz2infile] [-fxml omxinfile]
# [-o textasnoutfile] [-ob binaryasnoutfile] [-ox xmloutfile]
# [-obz2 bz2outfile] [-op pepxmloutfile] [-oc csvfile] [-w] [-to pretol]
# [-te protol] [-tom promass] [-tem premass] [-tez prozdep] [-ti isotopes]
# [-teppm] [-ta autotol] [-tex exact] [-i ions] [-cl cutlo] [-ch cuthi]
# [-ci cutinc] [-cp precursorcull] [-v cleave] [-x taxid] [-w1 window1]
# [-w2 window2] [-h1 hit1] [-h2 hit2] [-hl hitlist] [-hc hitcount]
# [-ht tophitnum] [-hm minhit] [-hs minspectra] [-he evalcut] [-mf fixedmod]
# [-mv variablemod] [-mnm] [-mm maxmod] [-e enzyme] [-zh maxcharge]
# [-zl mincharge] [-zoh maxprodcharge] [-zt chargethresh] [-z1 plusone]
# [-zc calcplusone] [-zcc calccharge] [-zn negions] [-pc pseudocount]
# [-sb1 searchb1] [-sct searchcterm] [-sp productnum] [-scorr corrscore]
# [-scorp corrprob] [-no minno] [-nox maxno] [-is subsetthresh]
# [-ir replacethresh] [-ii iterativethresh] [-p prolineruleions] [-il] [-el]
# [-ml] [-mx modinputfile] [-mux usermodinputfile] [-nt numthreads] [-ni]
# [-ns] [-os] [-nrs] [-logfile File_Name] [-conffile File_Name] [-version]
# [-version-full] [-dryrun]

# # OPTIONAL ARGUMENTS
#  -h
#    Print USAGE and DESCRIPTION;  ignore other arguments
#  -help
#    Print USAGE, DESCRIPTION and ARGUMENTS description;  ignore other arguments
#  -xmlhelp
#    Print USAGE, DESCRIPTION and ARGUMENTS description in XML format;  ignore
#    other arguments
#  -pm <String>
#    search parameter input in xml format (overrides command line)
#    Default = `'
#  -d <String>
#    Blast sequence library to search. Do not include .p* filename suffixes.
#    Default = `nr'
#  -umm
#    use memory mapped sequence libraries
#  -f <String>
#    single dta file to search
#    Default = `'
#  -fx <String>
#    multiple xml-encapsulated dta files to search
#    Default = `'
#  -fb <String>
#    multiple dta files separated by blank lines to search
#    Default = `'
#  -fp <String>
#    pkl formatted file
#    Default = `'
#  -fm <String>
#    mgf formatted file
#    Default = `'
#  -foms <String>
#    omssa oms file
#    Default = `'
#  -fomx <String>
#    omssa omx file
#    Default = `'
#  -fbz2 <String>
#    omssa omx file compressed by bzip2
#    Default = `'
#  -fxml <String>
#    omssa xml search request file
#    Default = `'
#  -o <String>
#    filename for text asn.1 formatted search results
#    Default = `'
#  -ob <String>
#    filename for binary asn.1 formatted search results
#    Default = `'
#  -ox <String>
#    filename for xml formatted search results
#    Default = `'
#  -obz2 <String>
#    filename for bzip2 compressed xml formatted search results
#    Default = `'
#  -op <String>
#    filename for pepXML formatted search results
#    Default = `'
#  -oc <String>
#    filename for csv formatted search summary
#    Default = `'
#  -w
#    include spectra and search params in search results
#  -to <Real>
#    product ion m/z tolerance in Da
#    Default = `0.8'
#  -te <Real>
#    precursor ion m/z tolerance in Da (or ppm if -teppm flag set)
#    Default = `2.0'
#  -tom <Integer>
#    product ion search type (0 = mono, 1 = avg, 2 = N15, 3 = exact)
#    Default = `0'
#  -tem <Integer>
#    precursor ion search type (0 = mono, 1 = avg, 2 = N15, 3 = exact, 4 =
#    multiisotope)
#    Default = `0'
#  -tez <Integer>
#    charge dependency of precursor mass tolerance (0 = none, 1 = linear)
#    Default = `0'
#  -ti <Integer>
#    when doing multiisotope search, number of isotopic peaks to search.  0 =
#    monoisotopic peak only
#    Default = `0'
#  -teppm
#    search precursor masses in units of ppm
#  -ta <Real>
#    automatic mass tolerance adjustment fraction
#    Default = `1.0'
#  -tex <Real>
#    threshold in Da above which the mass of neutron should be added in exact
#    mass search
#    Default = `1446.94'
#  -i <String>
#    id numbers of ions to search (comma delimited, no spaces)
#    Default = `1,4'
#  -cl <Real>
#    low intensity cutoff as a fraction of max peak
#    Default = `0.0'
#  -ch <Real>
#    high intensity cutoff as a fraction of max peak
#    Default = `0.2'
#  -ci <Real>
#    intensity cutoff increment as a fraction of max peak
#    Default = `0.0005'
#  -cp <Integer>
#    eliminate charge reduced precursors in spectra (0=no, 1=yes)
#    Default = `0'
#  -v <Integer>
#    number of missed cleavages allowed
#    Default = `1'
#  -x <String>
#    comma delimited list of taxids to search (0 = all)
#    Default = `0'
#  -w1 <Integer>
#    single charge window in Da
#    Default = `27'
#  -w2 <Integer>
#    double charge window in Da
#    Default = `14'
#  -h1 <Integer>
#    number of peaks allowed in single charge window (0 = number of ion species)
#    Default = `2'
#  -h2 <Integer>
#    number of peaks allowed in double charge window (0 = number of ion species)
#    Default = `2'
#  -hl <Integer>
#    maximum number of hits retained per precursor charge state per spectrum
#    during the search
#    Default = `30'
#  -hc <Integer>
#    maximum number of hits reported per spectrum (0 = all)
#    Default = `0'
#  -ht <Integer>
#    number of m/z values corresponding to the most intense peaks that must
#    include one match to the theoretical peptide
#    Default = `6'
#  -hm <Integer>
#    the minimum number of m/z matches a sequence library peptide must have for
#    the hit to the peptide to be recorded
#    Default = `2'
#  -hs <Integer>
#    the minimum number of m/z values a spectrum must have to be searched
#    Default = `4'
#  -he <Real>
#    the maximum evalue allowed in the hit list
#    Default = `1'
#  -mf <String>
#    comma delimited (no spaces) list of id numbers for fixed modifications
#    Default = `'
#  -mv <String>
#    comma delimited (no spaces) list of id numbers for variable modifications
#    Default = `'
#  -mnm
#    n-term methionine should not be cleaved
#  -mm <Integer>
#    the maximum number of mass ladders to generate per database peptide
#    Default = `128'
#  -e <Integer>
#    id number of enzyme to use
#    Default = `0'
#  -zh <Integer>
#    maximum precursor charge to search when not 1+
#    Default = `3'
#  -zl <Integer>
#    minimum precursor charge to search when not 1+
#    Default = `1'
#  -zoh <Integer>
#    maximum product charge to search
#    Default = `2'
#  -zt <Integer>
#    minimum precursor charge to start considering multiply charged products
#    Default = `3'
#  -z1 <Real>
#    fraction of peaks below precursor used to determine if spectrum is charge 1
#    Default = `0.95'
#  -zc <Integer>
#    should charge plus one be determined algorithmically? (1=yes)
#    Default = `1'
#  -zcc <Integer>
#    how should precursor charges be determined? (1=believe the input file,
#    2=use a range)
#    Default = `2'
#  -zn <Integer>
#    search using negative or positive ions (1=positive, -1=negative)
#    Default = `1'
#  -pc <Integer>
#    minimum number of precursors that match a spectrum
#    Default = `1'
#  -sb1 <Integer>
#    should first forward (b1) product ions be in search (1=no)
#    Default = `1'
#  -sct <Integer>
#    should c terminus ions be searched (1=no)
#    Default = `0'
#  -sp <Integer>
#    max number of ions in each series being searched (0=all)
#    Default = `100'
#  -scorr <Integer>
#    turn off correlation correction to score (1=off, 0=use correlation)
#    Default = `0'
#  -scorp <Real>
#    probability of consecutive ion (used in correlation correction)
#    Default = `0.5'
#  -no <Integer>
#    minimum size of peptides for no-enzyme and semi-tryptic searches
#    Default = `4'
#  -nox <Integer>
#    maximum size of peptides for no-enzyme and semi-tryptic searches (0=none)
#    Default = `40'
#  -is <Real>
#    evalue threshold to include a sequence in the iterative search, 0 = all
#    Default = `0.0'
#  -ir <Real>
#    evalue threshold to replace a hit, 0 = only if better
#    Default = `0.0'
#  -ii <Real>
#    evalue threshold to iteratively search a spectrum again, 0 = always
#    Default = `0.01'
#  -p <String>
#    id numbers of ion series to apply no product ions at proline rule at (comma
#    delimited, no spaces)
#    Default = `'
#  -il
#    print a list of ions and their corresponding id number
#  -el
#    print a list of enzymes and their corresponding id number
#  -ml
#    print a list of modifications and their corresponding id number
#  -mx <String>
#    file containing modification data
#    Default = `mods.xml'
#  -mux <String>
#    file containing user modification data
#    Default = `usermods.xml'
#  -nt <Integer>
#    number of search threads to use, 0=autodetect
#    Default = `0'
#  -ni
#    don't print informational messages
#  -ns
#    depreciated flag
#  -os
#    use omssa 1.0 scoring
#  -nrs
#    turn off rank score
#  -logfile <File_Out>
#    File to which the program log should be redirected
#  -conffile <File_In>
#    Program's configuration (registry) data file
#  -version
#    Print version number;  ignore other arguments
#  -version-full
#    Print extended version data;  ignore other arguments
#  -dryrun
#    Dry run the application: do nothing, only test all preconditions
