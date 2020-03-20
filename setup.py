#!/usr/bin/env python3

from setuptools import setup
import setuptools
from setuptools.command.install_lib import install_lib
import setuptools.command.build_py
import distutils.cmd
import os
import sys


executable_list = [
    'makeblastdb',
    'tandem',
    'tandem.exe',
    'qvality',
    'percolator',
    'percolator_2_08',
    'omssacl',
    'myrimatch_2_1_138',
    'myrimatch.exe',
    'MSAmanda.exe',
    'PepNovo_bin',
    'novor.bat',
    'novor.sh',
    'PepNovo.exe',
]

if sys.platform in ['win32']:
    class my_install_lib(setuptools.command.install_lib.install_lib):
        pass
else:
    class my_install_lib(setuptools.command.install_lib.install_lib):

        def run(self):
            setuptools.command.install_lib.install_lib.run(self)
            for fn in self.get_outputs():
                if os.path.basename(fn) in executable_list:
                    # copied from setuptools source - make the binaries
                    # executable
                    mode = ((os.stat(fn).st_mode) | 0o555) & 0o7777
                    print("changing mode of %s to %o", fn, mode)
                    os.chmod(fn, mode)


class BuildPyWithResources(setuptools.command.build_py.build_py):
    """Includes install_resources.py before the setuptools build"""

    def run(self):
        self.run_command('install_resources')
        setuptools.command.build_py.build_py.run(self)


class InstallResourcesCommand(distutils.cmd.Command):
    """Download resources from webpage and install into ursgal/resources"""
    description = 'Download and install third party engines'
    user_options = []

    def initialize_options(self):
        return
    def finalize_options(self):
        return

    def run(self):
        '''
        Download all resources from our webpage to ursgal/resources.

        '''
        working_directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
        )
        if os.path.exists(os.path.join(working_directory, 'ursgal')) is False:
            print('Could not find ursgal directory')
            sys.exit(1)
        import ursgal
        uc = ursgal.UController()
        downloaded_zips = uc.download_resources(resources=None)
        if len(downloaded_zips) == 0:
            print('[ INFO ] No engines were downloaded, all should be available')
        else:
            print(
                '[ INFO ] Downloaded and installed {0} engine(s)'.format(
                    len(downloaded_zips)
                )
            )
            for engine, zip_file in downloaded_zips:
                print(
                    '[ INFO ] Engine: {0} has been installed from {1}'.format(
                        engine,
                        zip_file
                    )
                )

# We store our version number in a simple text file:
version_path = os.path.join(
    os.path.dirname(__file__),
    'ursgal', 'version.txt'
)
with open(version_path, 'r') as version_file:
    ursgal_version = version_file.read().strip()

with open('requirements.txt') as req:
    requirements = req.readlines()

setup(
    name='ursgal',
    version=ursgal_version,
    packages=['ursgal'],
    package_dir={'ursgal': 'ursgal'},
    description='ursgal',
    package_data={
        'ursgal' : [
            'version.txt',
            'wrappers/*.py',
            'resources/*/*/*',
            'resources/*/*/*/*',
            'resources/*/*/*/*/*',
        ]
    },
    build_requires=[
        'numpy',
    ],
    install_requires=requirements,
    long_description='Universal Python module combining common bottom-up proteomics tools for large-scale analysis',
    author='Lukas P. M. Kremer, Purevdulam Oyunchimeg, Johannes Barth, Stefan Schulze and Christian Fufezan',
    author_email='christian@fufezan.net',
    url='http://ursgal.github.com',
    license='Lesser GNU General Public License (LGPL)',
    platforms='any that supports python 3.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    cmdclass={
        'install_lib': my_install_lib,
        'build_py': BuildPyWithResources,
        'install_resources': InstallResourcesCommand,
    }
)
