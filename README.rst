Introduction
############

*Ursgal - Universal Python Module Combining Common Bottom-Up Proteomics Tools for Large-Scale Analysis*

|pypi| |build-status-travis| |doc-status| |Gitter|

.. |pypi| image:: https://badge.fury.io/py/ursgal.svg
    :target: https://badge.fury.io/py/ursgal

.. |build-status-travis| image:: https://travis-ci.org/ursgal/ursgal.svg?branch=master
   :target: https://travis-ci.org/ursgal/ursgal
   :alt: Travis CI status

.. |doc-status| image:: http://readthedocs.org/projects/ursgal/badge/?version=latest
   :target: http://ursgal.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |Gitter| image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :alt: Join the chat at https://gitter.im/ursgal/ursgal
   :target: https://gitter.im/ursgal/ursgal?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

Summary
*******

Ursgal is a Python module that offers a generalized interface to common bottom-up proteomics tools, e.g.

    a) Peptide spectrum matching with up to eight different search engines (some available in multiple versions), including four open modification search engines

    b) Evaluation and post processing of search results with up to two different engines for protein database searches as well as two engines for the post processing of mass difference results from open modification engines

    c) Integration of search results from different search engines

    d) De novo sequencing with up to four different search engines

    e) Miscellaneous tools including the creation of a target decoy database as well as filtering, sanitizing and visualizing of results

Abstract
********

Proteomics data integration has become a broad field with a variety of programs offering innovative algorithms to analyze increasing amounts of data. Unfortunately, this software diversity leads to many problems as soon as the data is analyzed using more than one algorithm for the same task. Although it was shown that the combination of multiple peptide identification algorithms yields more robust results (Nahnsen et al. 2011, Vaudel et al. 2015, Kwon et al. 2011), it is only recently that unified approaches are emerging (Vaudel et al. 2011, Wen et al. 2015); however, workflows that, for example, aim to optimize search parameters or that employ cascaded style searches (Kertesz-Farkas et al. 2015) can only be made accessible if data analysis becomes not only unified but also and most importantly scriptable. Here we introduce Ursgal, a Python interface to many commonly used bottom-up proteomics tools and to additional auxiliary programs. Complex workflows can thus be composed using the Python scripting language using a few lines of code. Ursgal is easily extensible, and we have made several database search engines (X!Tandem (Craig and Beavis 2004), OMSSA (Geer et al. 2004), MS-GF+ (Kim et al. 2010), Myrimatch (Tabb et al. 2008), MS Amanda (Dorfer et al. 2014)), statistical postprocessing algorithms (qvality (Käll et al. 2009), Percolator (Käll et al. 2008)), and one algorithm that combines statistically postprocessed outputs from multiple search engines (“combined FDR” (Jones et al. 2009)) accessible as an interface in Python. Furthermore, we have implemented a new algorithm (“combined PEP”) that combines multiple search engines employing elements of “combined FDR” (Jones et al. 2009), PeptideShaker (Vaudel et al. 2015), and Bayes’ theorem.

*Kremer, L. P. M., Leufken, J., Oyunchimeg, P., Schulze, S. and Fufezan, C.
(2015):* |publicationtitle|_ *, Journal of Proteome research, 15, 788-.
DOI:10.1021/acs.jproteome.5b00860*

.. _publicationtitle: http://dx.doi.org/10.1021/acs.jproteome.5b00860
.. |publicationtitle| replace:: *Ursgal, Universal Python Module Combining Common Bottom-Up Proteomics Tools for Large-Scale Analysis*


Documentation
*************

The complete Documentation can be found at `Read the Docs`_

Besides the `Download and Installation`_ steps,
this includes a `Quick Start Tutorial`_ 
detailed documentation of the `Modules`_ and `Available Engines`_
as well as a broad set of `Example Scripts`_ and many more.


.. _Download and Installation:
    https://ursgal.readthedocs.io/en/latest/intro.html#installation

.. _Quick Start Tutorial:
    https://ursgal.readthedocs.io/en/latest/quick_start.html

.. _Example Scripts:
    https://ursgal.readthedocs.io/en/latest/example_scripts.html

.. _Modules:
    https://ursgal.readthedocs.io/en/latest/index.html#module-structure

.. _Available Engines:
    https://ursgal.readthedocs.io/en/latest/index.html#engines

.. _Read the Docs:
    http://ursgal.readthedocs.org/

.. _installation:

Download and Installation
*************************

Ursgal requires `Python`_ 3.4 or higher.
If you want to run Ursgal on a Windows system, Python 3.6 or higher is
recommended.

There are two recommended ways for installing Ursgal:

    * Installation via pip
    * Installation from the source (GitHub)

.. _Python:
   https://www.python.org/downloads/

.. _install_pip:

Installation via pip
~~~~~~~~~~~~~~~~~~~~

Execute the following command from your command line::

    user@localhost:~$ pip install ursgal

This installs Python into your Python site-packages. 

To download the executables, which we are allowed to distribute run::

    user@localhost:~$ ursgal-install-resources


You can now use it with all engines that we have built
or that we are allowed to distribute.
For all other third-party engines, a manual download from the respective
homepage is required (see also: `How to install third party engines`_)

.. note::

    Pip is included in Python 3.4 and higher. However, it might not be
    included in in your system's PATH environment variable.
    If this is the case, you can either add the Python scripts directory to your
    PATH env variable or use the path to the pip.exe directly for the
    installation, e.g.: ~/Python34/Scripts/pip.exe install ursgal

.. note::

    On Mac it may be neccesary to use Python3.6, since it comes with its
    own OpenSSL now. This may avoid problems when using pip.

.. _How to install third party engines:
    https://ursgal.readthedocs.io/en/latest/faq.html#q-how-do-i-add-an-engine-that-is-not-installed-via-install-resources-py


Installation from  source
~~~~~~~~~~~~~~~~~~~~~~~~~

1. Download Ursgal using `GitHub`_ **or** the zip file:

* GitHub version: Starting from your command line, the easiest way is to clone the GitHub repo.::

   user@localhost:~$ git clone https://github.com/ursgal/ursgal.git

* ZIP version: Alternatively, download and extract the `ursgal zip file`_

.. _GitHub:
   https://github.com/ursgal/ursgal

.. _ursgal zip file:
   https://github.com/ursgal/ursgal/archive/master.zip

2. Next, navigate into the Ursgal folder and install the requirements::

    user@localhost:~$ cd ursgal
    user@localhost:~/ursgal$ pip install -r requirements.txt

.. note::

    Pip is included in Python 3.4 and higher. However, it might not be
    included in in your system's PATH environment variable.
    If this is the case, you can either add the Python scripts directory to your
    PATH env variable or use the path to the pip.exe directly for the
    installation, e.g.: ~/Python34/Scripts/pip.exe install -r requirements.txt

.. note::

    On Mac it may be neccesary to use Python3.6, since it comes with its
    own OpenSSL now. This may avoid problems when using pip.

3. Finally, use setup.py to download third-party engines (those that we are allowed to distribute) 
and to install Ursgal into the Python site-packages::

    user@localhost:~/ursgal$ python setup.py install

If you want to install the third-party engines without installing Ursgal
into the Python site-packages you can use::

    user@localhost:~/ursgal$ python setup.py install_resources

.. note::

    Since we are not allowed to distribute all third party engines, you might need to
    download and install them on your own. See FAQ (`How to install third party engines`_) and
    the respective engine documentation for more information.

.. note::

    Under Linux, it may be required to change the permission in the
    python site-package folder so that all files are executable

(You might need administrator privileges to write in the Python site-package folder.
On Linux or OS X, use ```sudo python setup.py install``` or write into a user folder
by using this command ```python setup.py install --user```. On Windows, you have to
start the command line with administrator privileges.)



Tests
*****

Run tox in root folder. You might need to install `tox`_ for Python3 first
although it is in the requirements_dev.txt (above) thus pip install -r requirements_dev.txt
should have installed it already. Then just execute::

    user@localhost:~/ursgal$ tox

In case you only want to test one python version (e.g because you only have one installed), run for e.g. python3.5::
    
    user@localhost:~/ursgal$ tox -e py35

For other environments to run, check out the tox.ini file
to test the package.

.. _tox:
    https://tox.readthedocs.io/en/latest/


Update to v0.6.0 Warning
************************

Please note that, due to significant reorganization of UController functions as well as some uparams,
compatibility of v0.6.0 with previous versions is not given in all cases.
Most likely, your previous results will not be recognized, i.e. previously executed runs will be executed again.
Please consider this before updating to v0.6.0, check the Changelog or ask us if you have any doubts.
We are sorry for the inconvenience but changes were necessary for further development.
If you want to continue using (and modifying) v0.5.0 you can use the branch v0.5.0.


Questions and Participation
***************************

If you encounter any problems you can open up issues at GitHub, join the conversation at Gitter, or write an email to ursgal.team@gmail.com. Please also check the `Frequently Asked Questions`_.

For any contributions, fork us at https://github.com/ursgal/ursgal and open up pull requests!
Please also check the `Contribution Guidelines`. Thanks!

.. _Frequently Asked Questions:
    https://ursgal.readthedocs.io/en/latest/faq.html#frequently-asked-questions

.. _Contribution Guidelines:
    https://ursgal.readthedocs.io/en/latest/contribute.html#contribute


Disclaimer
**********

Ursgal is beta and thus still contains bugs. Verify your results manually and
as common practice in science, never trust a blackbox :)

Copyrights
***********

Copyright 2014-2020 by authors and contributors in alphabetical order

* Christian Fufezan
* Aime B. Igiraneza
* Manuel Koesters
* Lukas P. M. Kremer
* Johannes Leufken
* Purevdulam Oyunchimeg
* Stefan Schulze
* Lukas Vaut
* David Yang
* Fengchao Yu

Contact
*******

    | Dr. Christian Fufezan
    | Institute of Pharmacy and Molecular Biotechnology
    | Heidelberg University
    | Germany
    | eMail: christian@fufezan.net

Citation
********

In an academic world, citations are the only credit that one can hope for ;)
Therefore, please do not forget to cite us if you use Ursagl:

Kremer, L. P. M., Leufken, J., Oyunchimeg, P., Schulze, S., and Fufezan, C. (2016) `Ursgal, Universal Python Module Combining Common Bottom-Up Proteomics Tools for Large-Scale Analysis`_ Journal of Proteome research 15, 788–794, DOI:10.1021/acs.jproteome.5b00860

.. _Ursgal, Universal Python Module Combining Common Bottom-Up Proteomics Tools for Large-Scale Analysis: http://dx.doi.org/10.1021/acs.jproteome.5b00860

.. note::

    Please also cite every tool you use in Ursgal. During runtime the references of
    the tools you are using are shown.

Full list of tools with proper citations that are integrated into Ursgal are:

    * Craig, R.; Beavis, R. C. TANDEM: matching proteins with tandem mass spectra. Bioinformatics 2004, 20 (9), 1466–1467.
    * Dorfer, V.; Pichler, P.; Stranzl, T.; Stadlmann, J.; Taus, T.; Winkler, S.; Mechtler, K. MS Amanda, a Universal Identification Algorithm Optimised for High Accuracy Tandem Mass Spectra. J. Proteome Res. 2014.
    * Frank, A. M.; Savitski, M. M.; Nielsen, M. L.; Zubarev, R. A. and Pevzner, P. A. De Novo Peptide Sequencing and Identification with Precision Mass Spectrometry. J. Proteome Res. 2007 6:114-123.',
    * Geer, L. Y.; Markey, S. P.; Kowalak, J. A.; Wagner, L.; Xu, M.; Maynard, D. M.; Yang, X.; Shi, W.; Bryant, S. H. Open Mass Spectrometry Search Algorithm. J. Proteome res. 2004, 3 (5), 958–964.
    * Hoopmann, M. R.; Zelter, A.; Johnson, R. S.; Riffle, M.; Maccoss, M. J.; Davis, T. N.; Moritz, R. L. Kojak: Efficient analysis of chemically cross-linked protein complexes. J Proteome Res 2015, 14, 2190-198
    * Jones, A. R.; Siepen, J. a.; Hubbard, S. J.; Paton, N. W. Improving sensitivity in proteome studies by analysis of false discovery rates for multiple search engines. Proteomics 2009, 9 (5), 1220–1229.
    * Kim, S.; Mischerikow, N.; Bandeira, N.; Navarro, J. D.; Wich, L.; Mohammed, S.; Heck, A. J. R.; Pevzner, P. A. The generating function of CID, ETD, and CID/ETD pairs of tandem mass spectra: applications to database search. MCP 2010, 2840–2852.
    * Käll, L.; Canterbury, J. D.; Weston, J.; Noble, W. S.; MacCoss, M. J. Semi-supervised learning for peptide identification from shotgun proteomics datasets. Nature methods 2007, 4 (11), 923–925.
    * Käll, L.; Storey, J. D.; Noble, W. S. Qvality: Non-parametric estimation of q-values and posterior error probabilities. Bioinformatics 2009, 25 (7), 964–966.
    * Kong, A. T., Leprevost, F. V, Avtonomov, D. M., Mellacheruvu, D., and Nesvizhskii, A. I. MSFragger: ultrafast and comprehensive peptide identification in mass spectrometry–based proteomics. Nature methods 2017, 14, 513–520
    * Leufken J, Niehues A, Sarin LP, Wessel F, Hippler M, Leidel SA, Fufezan C. pyQms enables universal and accurate quantification of mass spectrometry data. Mol Cell Proteomics 2017, 16, 1736-1745
    * Ma, B. Novor: real-time peptide de novo sequencing software. J Am Soc Mass Spectrom. 2015 Nov;26(11):1885-94
    * Na S, Bandeira N, Paek E. Fast multi-blind modification search through tandem mass spectrometry. Mol Cell Proteomics 2012, 11
    * Reisinger, F.; Krishna, R.; Ghali, F.; Ríos, D.; Hermjakob, H.; Antonio Vizcaíno, J.; Jones, A. R. JmzIdentML API: A Java interface to the mzIdentML standard for peptide and protein identification data. Proteomics 2012, 12 (6), 790–794.
    * Tabb, D. L.; Fernando, C. G.; Chambers, M. C. MyriMatch: highly accurate tandem mass spectral peptide identification by multivariate hypergeometric analysis. J Proteome Res. 2008, 6 (2), 654–661.
    * Yu, F., Li, N., Yu, W. PIPI: PTM-Invariant Peptide Identification Using Coding Method. J Prot Res 2016, 15
    * Barsnes, H., Vaudel, M., Colaert, N., Helsens, K., Sickmann, A., Berven, F. S., and Martens, L. (2011) compomics-utilities: an open-source Java library for computational proteomics. BMC Bioinformatics 12, 70
    * Leufken, J., Niehues, A., Sarin, L. P., Wessel, F., Hippler, M., Leidel, S. A., and Fufezan, C. (2017) pyQms enables universal and accurate quantification of mass spectrometry data. Mol. Cell. Proteomics 16, 1736–1745
    * Jaeger, D., Barth, J., Niehues, A., and Fufezan, C. (2014) pyGCluster, a novel hierarchical clustering approach. Bioinformatics 30, 896–898
    * Bald, T., Barth, J., Niehues, A., Specht, M., Hippler, M., and Fufezan, C. (2012) pymzML--Python module for high-throughput bioinformatics on mass spectrometry data. Bioinformatics 28, 1052–1053
    * Kösters, M., Leufken, J., Schulze, S., Sugimoto, K., Klein, J., Zahedi, R. P., Hippler, M., Leidel, S. A., and Fufezan, C. (2018) pymzML v2.0: introducing a highly compressed and seekable gzip format. Bioinformatics 34, 2513-2514
    * Liu, M.Q.; Zeng, W.F.; Fang, P.; Cao, W.Q.; Liu, C.; Yan, G.Q.; Zhang, Y.; Peng, C.; Wu, J.Q.;
    * Zhang, X.J.; Tu, H.J.; Chi, H.; Sun, R.X.; Cao, Y.; Dong, M.Q.; Jiang, B.Y.; Huang, J.M.; Shen, H.L.; Wong ,C.C.L.; He, S.M.; Yang, P.Y. (2017) pGlyco 2.0 enables precision N-glycoproteomics with comprehensive quality control and one-step mass spectrometry for intact glycopeptide identification. Nat Commun 8(1)
    * Yuan, Z.F.; Liu, C.; Wang, H.P.; Sun, R.X.; Fu, Y.; Zhang, J.F.; Wang, L.H.; Chi, H.; Li, Y.; Xiu, L.Y.; Wang, W.P.; He, S.M. (2012) pParse: a method for accurate determination of monoisotopic peaks in high-resolution mass spectra. Proteomics 12(2)
    * Hulstaert, N.; Sachsenberg, T.; Walzer, M.; Barsnes, H.; Martens, L. and Perez-Riverol, Y. (2019) ThermoRawFileParser: modular, scalable and cross-platform RAW file conversion. bioRxiv https://doi.org/10.1101/622852
    * Tran, N.H.; Zhang, X.; Xin, L.; Shan, B.; Li, M. (2017) De novo peptide sequencing by deep learning. PNAS 114 (31) 
    * Devabhaktuni, A.; Lin, S.; Zhang, L.; Swaminathan, K.; Gonzalez, CG.; Olsson, N.; Pearlman, SM.; Rawson, K.; Elias, JE. (2019) TagGraph reveals vast protein modification landscapes from large tandem mass spectrometry datasets. Nat Biotechnol. 37(4)
    * Yang, H; Chi, H; Zhou, W; Zeng, WF; He, K; Liu, C; Sun, RX; He, SM. (2017) Open-pNovo: De Novo Peptide Sequencing with Thousands of Protein Modifications. J Proteome Res. 16(2)
    * Polasky, DA; Yu, F; Teo, GC; Nesvizhskii, AI (2020) Fast and comprehensive N- and O-glycoproteomics analysis with MSFragger-Glyco. Nat Methods 17 (11)
    * Geiszler, DJ; Kong, AT; Avtonomov, DM; Yu, F; Leprevost, FV; Nesvizhskii, AI (2020) PTM-Shepherd: analysis and summarization of post-translational and chemical modifications from open search results. bioRxiv doi: https://doi.org/10.1101/2020.07.08.192583
    * An, Z; Zhai, L; Ying, W; Qian, X; Gong, F; Tan, M; Fu, Y. (2019) PTMiner: Localization and Quality Control of Protein Modifications Detected in an Open Search and Its Application to Comprehensive Post-translational Modification Characterization in Human Proteome.  Mol Cell Proteomics 18 (2)
