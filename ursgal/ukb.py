#!/usr/bin/env python3

CAM_MOD            = 57.0214637206
DIFFERENCE_14N_15N = 0.997035
PROTON             = 1.00727646677

NITROGENS = {
    'A' : 1,
    'C' : 1,
    'D' : 1,
    'E' : 1,
    'F' : 1,
    'G' : 1,
    'H' : 3,
    'I' : 1,
    'K' : 2,
    'L' : 1,
    'M' : 1,
    'N' : 2,
    'P' : 1,
    'Q' : 2,
    'R' : 4,
    'S' : 1,
    'T' : 1,
    'V' : 1,
    'W' : 2,
    'Y' : 1,
}

# mass of all amino acid difference between 15N and 14N
DICT_15N_DIFF = {
    'A' : 0.997035,
    'C' : 0.997035,
    'D' : 0.997035,
    'E' : 0.997035,
    'F' : 0.997035,
    'G' : 0.997035,
    'H' : 2.991105,
    'I' : 0.997035,
    'K' : 1.99407,
    'L' : 0.997035,
    'M' : 0.997035,
    'N' : 1.99407,
    'P' : 0.997035,
    'Q' : 1.99407,
    'R' : 3.98814,
    'S' : 0.997035,
    'T' : 0.997035,
    'V' : 0.997035,
    'W' : 1.99407,
    'Y' : 0.997035
}

# Dictionary containing all accepted file extensions in Ursgal
FILE_EXTENSIONS = {
    '.dat' : {
        'short_name': 'DAT',
        'long_name': 'DAT (Mascot)',
        'same_extension': [],
        'description': \
            'Mascot specific identification output format.'
            'Mixture of csv, xml and configuration style file.'
    },
    '.csv' : {
            'short_name'     : 'CSV',
            'long_name'      : 'CSV (Comma Delimited)',
            'same_extension' : [],
            'description'    : \
                'The comma-separated values (CSV) file format is a '\
                'tabular data format that has fields separated by the '\
                'comma character and quoted by the double quote '\
                'character.\n'\
            '(DataTypes.net; https://datatypes.net)',
    },
    '.cfg' : {
            'short_name'     : 'CFG',
            'long_name'      : 'CFG (pGlyco)',
            'same_extension' : [],
            'description'    : \
                'pGlyco specific parameter file format.',
    },
    '.den' : {
        'short_name'     : 'DEN',
        'long_name'      : 'DEN (XMVB Density Data)',
        'same_extension' : [],
        'description'    : \
            'DEN file is a XMVB Density Data. Xiamen Valence Bond '\
            '(XMVB) is a quantum chemistry program for performing '\
            'electronic structure calculations based on the '\
            'non-orthogonal Valence Bond methods.\n'\
            '(DataTypes.net; https://datatypes.net)',
    },
    '.dta' : {
        'short_name'     : 'DTA',
        'long_name'      : 'DTA (Stata Data)',
        'same_extension' : [],
        'description'    : \
            'DTA file is a Stata Data File. Stata is a '\
            'general-purpose statistical software package created in '\
            '1985 by StataCorp. It is used by many businesses and '\
            'academic institutions around the world.\n'\
            '(DataTypes.net; https://datatypes.net)',
    },
    '.dta.txt' : {
        'short_name'     : 'DTA_Text',
        'long_name'      : 'DTA_Text (Text Fromat of DTA)',
        'same_extension' : [],
        'description'    : \
            'Text format of DTA format.',
    },
    '.fasta' : {
        'short_name'     : 'FASTA',
        'long_name'      : 'FASTA (Sequence Alignment)',
        'same_extension' : ['.fa', '.mpfa', '.fna', '.fsa', '.fas'],
        'description'    : \
            'FASTA file is a FASTA Sequence. In bioinformatics, FASTA '\
            'format is a text-based format for representing either '\
            'nucleotide sequences or peptide sequences, in which '\
            'nucleotides or amino acids are represented using '\
            'single-letter codes.\n'\
            '(DataTypes.net; https://datatypes.net)',
    },
    '.gaml' : {
        'short_name'     : 'GAML',
        'long_name'      : 'GAML (GAML spectra)',
        'same_extension' : [],
        'description'    : \
            'GAML spectra',
    },
    '.idx.gz' : {
        'short_name'     : 'igzip',
        'long_name'      : 'igzipped mzML (MS data)',
        'same_extension' : [],
        'description'    : \
            'Compressed mzML, indexed gzip according to pymzML2.0',
    },
    '.kojak.txt' : {
        'short_name'     : 'Kojak',
        'long_name'      : 'Kojak (Kojak result)',
        'same_extension' : [],
        'description'    : \
            'Kojak result',
    },
    '.mgf' : {
        'short_name'     : 'MGF',
        'long_name'      : 'MGF (Mascot Generic Format)',
        'same_extension' : [],
        'description'    : \
            'The Mascot generic format for a data file submitted to Mascot',
    },
    '.ms2' : {
        'short_name'     : 'MS2',
        'long_name'      : 'MS2 (MS data)',
        'same_extension' : [],
        'description'    : \
            'Mass spectrometry data format',
    },
    '.mzData' : {
        'short_name'     : 'mzData',
        'long_name'      : 'mzData (MS data)',
        'same_extension' : [],
        'description'    : \
            'This format was deprecated, and was replaced by mzML',
    },
    '.mzid' : {
        'short_name'     : 'mzid',
        'long_name'      : 'mzid (MS data)',
        'same_extension' : [],
        'description'    : \
            'Mass spectrometry data format',
    },
    '.mzid.gz' : {
        'short_name'     : 'mzid.gz',
        'long_name'      : 'mzid.gz (Compressed mzid)',
        'same_extension' : [],
        'description'    : \
            'Compressed mzid',
    },
    '.mzML' : {
        'short_name'     : 'mzML',
        'long_name'      : 'mzML (MS data)',
        'same_extension' : [],
        'description'    : \
            'Mass spectrometry data format',
    },
    '.mzML.gz' : {
        'short_name'     : 'mzML',
        'long_name'      : 'mzML (MS data)',
        'same_extension' : [],
        'description'    : \
            'Compressed mzML',
    },
    '.mzXML' : {
        'short_name'     : 'mzXML',
        'long_name'      : 'mzXML (MS data)',
        'same_extension' : [],
        'description'    : \
            'This format was replaced by mzML',
    },
    '.pep.xml' : {
        'short_name'     : 'pep.xml',
        'long_name'      : 'pep.xml (Kojak result)',
        'same_extension' : [],
        'description'    : \
            'Kojak result',
    },
    '.perc.inter.txt' : {
        'short_name'     : 'perc.inter.txt',
        'long_name'      : 'perc.inter.txt (Kojak result)',
        'same_extension' : [],
        'description'    : \
            'Kojak result',
    },
    '.perc.intra.txt' : {
        'short_name'     : 'perc.intra.txt',
        'long_name'      : 'perc.intra.txt (Kojak result)',
        'same_extension' : [],
        'description'    : \
            'Kojak result',
    },
    '.perc.loop.txt' : {
        'short_name'     : 'perc.loop.txt',
        'long_name'      : 'perc.loop.txt (Kojak result)',
        'same_extension' : [],
        'description'    : \
            'Kojak result',
    },
    '.perc.single.txt' : {
        'short_name'     : 'perc.single.txt',
        'long_name'      : 'perc.single.txt (Kojak result)',
        'same_extension' : [],
        'description'    : \
            'Kojak result',
    },
    '.pkl' : {
        'short_name'     : 'PKL',
        'long_name'      : 'PKL (pickle)',
        'same_extension' : [],
        'description'    : \
            'PKL file is a file created by the Python pickle module',
    },
    '.raw' : {
        'short_name'     : 'RAW',
        'long_name'      : 'RAW (ThermoFisher RAW format)',
        'same_extension' : [],
        'description'    : \
            'ThermoFisher RAW format',
    },
    '.ssl' : {
        'short_name'     : 'SSL',
        'long_name'      : 'SSL (Spectrum Sequence List)',
        'same_extension' : [],
        'description'    : \
            'Generic tab-delimited text file format supported by BiblioSpec',
    },
    '.svg' : {
        'short_name'     : 'SVG',
        'long_name'      : 'SVG (Scalable Vector Graphic)',
        'same_extension' : [],
        'description'    : \
            'SVG file is a Scalable Vector Graphic. SVG is a language '\
            'for describing two-dimensional graphics and graphical '\
            'applications in XML.\n'\
            '(DataTypes.net; https://datatypes.net)',
    },
    '.tsv' : {
        'short_name'     : 'TSV',
        'long_name'      : 'TSV (Tab-Separated Values document)',
        'same_extension' : [],
        'description'    : \
            'TSV is a Tab-Separated Values document. It is very '\
            'simple textual data format which allows tabular data to '\
            'be exhanged between applications that use different '\
            'internal data formats.\n'\
            '(DataTypes.net; https://datatypes.net)',
    },
    '.txt' : {
        'short_name'     : 'Text',
        'long_name'      : 'Text (General text format)',
        'same_extension' : ['.text'],
        'description'    : \
            'TXT file is a plain text. Plain text is textual '\
            'material, usually in a disk file, that is (largely) '\
            'unformatted.\n'\
            '(DataTypes.net; https://datatypes.net)',
    },
    '.xml' : {
        'short_name'     : 'XML',
        'long_name'      : 'XML (Extensible Markup Language document)',
        'same_extension' : [],
        'description'    : \
            'XML file is an Extensible Markup Language document. XML '\
            'is a simple, very flexible text format derived from SGML '\
            '(ISO 8879). Originally designed to meet the challenges '\
            'of large-scale electronic publishing, XML is also '\
            'playing an increasingly important role in the exchange '\
            'of a wide variety of data on the Web and elsewhere.\n'\
            '(DataTypes.net; https://datatypes.net)',
    },
    '.xml.gz' : {
        'short_name'     : 'XML.gz',
        'long_name'      : 'XML.gz (Compressed mzid)',
        'same_extension' : [],
        'description'    : \
            'Compressed xml',
    }
}

ENGINE_TYPES = {
    'converter'                     : 'convert',
    'controller'                    : None,
    'cross_link_search_engine'      : 'search_mgf',
    'de_novo_search_engine'         : 'search_mgf',
    'fetcher'                       : 'fetch_file',
    'misc_engine'                   : 'execute_misc_engine',
    'meta_engine'                   : 'combine_search_results',
    'protein_database_search_engine': 'search_mgf',
    'quantification_engine'         : 'quantify',
    'spectral_library_search_engine': 'search_mgf',
    '_test'                         : 'execute_misc_engine',
    'validation_engine'             : 'validate',
    'visualizer'                    : 'visualize',
}

UCONTROLLER_FUNCTIONS = {}
for engine_type, ucontoller_function in ENGINE_TYPES.items():
    if ucontoller_function is None:
        continue
    if ucontoller_function not in UCONTROLLER_FUNCTIONS.keys():
        UCONTROLLER_FUNCTIONS[ucontoller_function] = []
    UCONTROLLER_FUNCTIONS[ucontoller_function].append(engine_type)