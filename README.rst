Introduction
############

*Ursgal - universal Python module combining common bottom-up proteomics tools for large-scale analysis*

|build-status| |doc-status| |Gitter-join Chat|

.. |build-status| image:: https://travis-ci.org/ursgal/ursgal.svg?branch=master
   :target: https://travis-ci.org/ursgal/ursgal
   :alt: Travis CI status

.. |doc-status| image:: https://readthedocs.org/projects/ursgal/badge/?version=latest
    :target: http://ursgal.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status
    
.. |Gitter-join Chat| image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
    :target: https://gitter.im/ursgal?utm_source=share-link&utm_medium=link&utm_campaign=share-link
    :alt: Gitter

Summary
*******

Ursgal is a Python module that offers a generalized interface to common bottom-up proteomics tools, e.g.

    a) Peptide spectrum matching with up to five different search engines (some available in multiple versions)

    b) Evaluation and post processing of search results with up to two different engines

    c) Integration of search results from different search engines

    d) Creation of a target decoy database

Abstract
********

Proteomics data integration has become a broad field with a variety of programs offering innovative algorithms to analyze increasing amounts of data. Unfortunately, this software diversity leads to many problems as soon as one tries to analyze data using more than one algorithm. Although it was shown that the combination of multiple algorithms yields more robust results, it is only recently that unified approaches are emerging which try to streamline the most prominent search algorithms. However, workflows that for example aim to optimize search parameters or that employ cascaded style searches 3 can only be made accessible if data analysis becomes not only unified but also and most importantly scriptable. Here we introduce Ursgal, an interface between the Python programming language and many commonly used bottom-up proteomics tools as well as several auxiliary programs. Complex common and novel workflows can thus be composed using the Python scripting language using a few lines of code. Ursgal is easily extendable and we have made several database search engines (X!Tandem, OMSSA, MS-GF+, MyriMatch, MSAmanda), post processing algorithms (qvality, Percolator) and two algorithm that combines validated outputs (combined FDR score and combined PEP score) accessible as a Python interface.

*Kremer et al. (2015): Ursgal, universal Python module combining common bottom-up proteomics tools for large-scale analysis, Journal of Proteome research 12/2015, DOI:10.1021/acs.jproteome.5b00860.*


.. _download:

Download
********

Get the latest version via GitHub:
    | https://github.com/ursgal/ursgal

   .zip package:
   | https://github.com/ursgal/ursgal/archive/master.zip

   git clone URL:
   | https://github.com/ursgal/ursgal.git

The complete Documentation can be found at
   | http://ursgal.readthedocs.org/


.. _installation:

Installation
************

Ursgal requires Python 3.4 or higher. 

Download ursgal using Github **or** the zip file:

* Github version: Starting with this the easiest way is to clone the github repo.::

   user@localhost:~$ git clone https://github.com/ursgal/ursgal.git
    

* ZIP version: Download and extract the `ursgalzip`_ file

.. _ursgalzip:
   https://github.com/ursgal/ursgal/archive/master.zip

Install requirements::

    user@localhost:~$ cd ursgal
    user@localhost:~/ursgal$ pip3.4 install -r requirements.txt

Install third party engines::

    user@localhost:~$ python3.4 install_resources.py

Install Ursgal::

    user@localhost:~$ python3.4 setup.py install


.. note::

    Under Linux it may be required to change the permission in the
    python3.4 site-package folder so that all files are executable

(You might need administrator privileges to write in the Python site-package folder.
On Linux or OS X, use ```sudo python setup.py install``` or write into a user folder
by using this command ```python setup.py install --user```. On Windows, you have to
start the command line with administrator privileges.)


Tests
*****

Run nosetests in root folder. You might need to install `nose`_ first::

    user@localhost:~/ursgal$ nosetests

.. _nose:
    https://nose.readthedocs.org/en/latest/


Participate
***********

Fork us at https://github.com/ursgal/ursgal and open up pull requests! Thanks!


Documentation
*************

For more detailed documentation of the modules and examples, please refer to
the documentation folder or http://ursgal.readthedocs.org


Disclaimer
**********

Ursgal is beta and thus still contains bugs. Verify your results manually and
as common practice in science, never trust a blackbox :)

Copyrights
***********

Copyright 2014-2015 by authors and contributors

* Lukas P. M. Kremer,
* Purevdulam Oyunchimeg,
* Johannes Leufken,
* Stefan Schulze,
* Christian Fufezan

Contact
*******

    | Dr. Christian Fufezan
    | Institute of Plant Biology and Biotechnology
    | Schlossplatz 8 , R 105
    | University of Muenster
    | Germany
    | eMail: christian@fufezan.net
    | Tel: +049 251 83 24861
    |
    | http://www.uni-muenster.de/Biologie.IBBP.AGFufezan


Citation
********

Ursgal citation

Lukas P. M. Kremer :sup:`1`, Johannes Leufken :sup:`1`, Purevdulam Oyunchimeg :sup:`1`, Stefan Schulze :sup:`1` and Christian Fufezan (2015) Journal of Proteome research, accepted

DOI: 10.1021/acs.jproteome.5b00860

:sup:`1` These authors contributed equally.

.. note::
    Please cite every tool you use in ursgal. During runtime the references of
    the tools you were using are shown.

Full list of tools with proper citations that are integrated into ursgal are:

    * Kwon, T.; Choi, H.; Vogel, C.; Nesvizhskii, A. I.; Marcotte, E. M. MSblender: A probabilistic approach for integrating peptide identifications from multiple database search engines. J. Proteome res. 2011, 10 (7), 2949–2958.
    * Geer, L. Y.; Markey, S. P.; Kowalak, J. A.; Wagner, L.; Xu, M.; Maynard, D. M.; Yang, X.; Shi, W.; Bryant, S. H. Open Mass Spectrometry Search Algorithm. J. Proteome res. 2004, 3 (5), 958–964.
    * Craig, R.; Beavis, R. C. TANDEM: matching proteins with tandem mass spectra. Bioinformatics 2004, 20 (9), 1466–1467.
    * Tabb, D. L.; Fernando, C. G.; Chambers, M. C. MyriMatch:highly accurate tandem mass spectral peptide identificaiton by multivariate hypergeometric analysis. J Proteome Res. 2008, 6 (2), 654–661.
    * Jones, A. R.; Siepen, J. a.; Hubbard, S. J.; Paton, N. W. Improving sensitivity in proteome studies by analysis of false discovery rates for multiple search engines. Proteomics 2009, 9 (5), 1220–1229.
    * Dorfer, V.; Pichler, P.; Stranzl, T.; Stadlmann, J.; Taus, T.; Winkler, S.; Mechtler, K. MS Amanda, a Universal Identification Algorithm Optimised for High Accuracy Tandem Mass Spectra. J. Proteome res. 2014.
    * Käll, L.; Canterbury, J. D.; Weston, J.; Noble, W. S.; MacCoss, M. J. Semi-supervised learning for peptide identification from shotgun proteomics datasets. Nature methods 2007, 4 (11), 923–925.
    * Kim, S.; Mischerikow, N.; Bandeira, N.; Navarro, J. D.; Wich, L.; Mohammed, S.; Heck, A. J. R.; Pevzner, P. a. The Generating Function of CID , ETD , and CID ETD Pairs of Tandem Mass Spectra Applications to Database Search MCP 2010, 2840–2852.
    * Reisinger, F.; Krishna, R.; Ghali, F.; Ríos, D.; Hermjakob, H.; Antonio Vizcaíno, J.; Jones, A. R. JmzIdentML API: A Java interface to the mzIdentML standard for peptide and protein identification data. Proteomics 2012, 12 (6), 790–794.
    * Käll, L.; Storey, J. D.; Noble, W. S. Qvality: Non-parametric estimation of q-values and posterior error probabilities. Bioinformatics 2009, 25 (7), 964–966.
