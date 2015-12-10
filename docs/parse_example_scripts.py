#!/usr/bin/env python3.4
# encoding: utf-8

import glob
import os

if __name__ == '__main__':
    print('''
        Formatting example scripts into rst files for the docs
''')
    # input()
    for example_script in glob.glob('../example_scripts/*.py'):
        if os.path.exists(example_script) is False:
            continue
        basename= os.path.basename(example_script)
        print('Reading: {0}'.format(example_script))
        with open('source/code_inc/{0}'.format(basename.replace('.py','.inc')), 'w') as o:
            print('''.. code-block:: python\n''', file=o)
            with open( example_script ) as infile:
                for line in infile:
                    print('\t{0}'.format( line.rstrip()), file=o)


