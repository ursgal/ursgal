#!/usr/bin/env python
import ursgal
import os
from collections import defaultdict as ddict
import csv
import sys

class pparse_2_0(ursgal.UNode):
    """
    Unode for pParse included in pGlyco 2.2.0
    For further information visit
    http://pfind.ict.ac.cn/software/pParse/#Downloads

    Note:
        Please download pParse manually as part of pGlyco 2.2.0
        https://github.com/pFindStudio/pGlyco2

    Reference:
    Yuan ZF, Liu C, Wang HP, Sun RX, Fu Y, Zhang JF, Wang LH,
    Chi H, Li Y, Xiu LY, Wang WP, He SM (2012)
    pParse: a method for accurate determination of monoisotopic peaks 
    in high-resolution mass spectra. Proteomics 12(2)
    """

    META_INFO = {
        'edit_version': 1.00,
        'name': 'pAarse',
        'version': '2.0',
        'release_date': '2018-11-02',
        'utranslation_style': 'pparse_style_1',
        'input_extensions': ['.raw'],
        'output_extensions': ['.mgf'],
        'output_suffix' : None,
        'create_own_folder': False,
        'in_development': False,
        'include_in_git': False,
        'distributable': False,
        'engine_type': {
            'converter': True,
        },
        'engine': {
            'win32' : {
                '64bit' : {
                    'exe'            : 'pParse.exe',
                    'url'            : '',
                    'zip_md5'        : None,
                    'additional_exe' : [],
                },
            },
        },
        'citation':
        'Yuan ZF, Liu C, Wang HP, Sun RX, Fu Y, Zhang JF, Wang LH,'
            'Chi H, Li Y, Xiu LY, Wang WP, He SM (2012)'
            'pParse: a method for accurate determination of monoisotopic peaks '
            'in high-resolution mass spectra. Proteomics 12(2)'
    }

    def __init__(self, *args, **kwargs):
        super(pparse_2_0, self).__init__(*args, **kwargs)
        pass

    def preflight(self):
        '''
        Formatting the command line via self.params

        Returns:
            dict: self.params

        Command line options:
            -D datapath               default (D:\data\)
            -L logfilepath            default (the same with datapath)
            -O outputpath             default (the same with datapath)
            -W isolation_width        default (2)
            -F input_format           default (raw) optional (wiff)
            -C co-elute               default (1)
            -S cut_similiar_mono      default (1)
            -I ipv_file               default (.\IPV.txt)
            -M mars_model             default (4)
            -T trainingset            default (.\TrainingSet.txt)
            -m output_mgf             default (1)
            -p output_pf              default (1)
            -d delete_msn             default (0)
            -a check_activationcenter default (1)
            -g debug_mode             default (0)
            -r rewrite_files          default (0)
            -t mars_threshold         default (-0.34)
            -u export_unchecked_mono  default (0)
            -y output_all_mars_y      default (0)
            -Y output_mars_y          default (0)
            -s output_trainingdata    default (0)
            -R recalibrate_window     default (7)
            -v outputsvmlight         default (0)
            -z m/z                    default (5)
            -i Intensity              default (1)
        '''
        self.params['translations']['raw_input_file'] = os.path.join(
            self.params['input_dir_path'],
            self.params['input_file']
        )
        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        # self.created_tmp_files.append(self.param_file_name)

        self.params['command_list'] = [
            self.exe,
            '-D',
            self.params['translations']['raw_input_file'],
            # '-O',
            # self.params['translations']['output_file_incl_path']
        ]

        for flag, value in self.params['translations']['pparse_options'].items():
            self.params['command_list'].extend(
                [flag, value]
            )

        return self.params


    def postflight(self):
        '''
        Rename output file, since that naming the output file is not properly working in pParse
        '''
        os.rename(
            self.params['translations']['raw_input_file'].replace('.raw', '_HCDFT.mgf'), 
            self.params['translations']['output_file_incl_path']
        )
        return self.params['translations']['output_file_incl_path']