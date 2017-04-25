Introduction
############

*Ursgal - Universal Python Module Combining Common Bottom-Up Proteomics Tools for Large-Scale Analysis*

|build-status-travis| |build-status-appveyor| |doc-status| |Gitter|

.. |build-status-travis| image:: https://travis-ci.org/ursgal/ursgal.svg?branch=master
   :target: https://travis-ci.org/ursgal/ursgal
   :alt: Travis CI status

.. |build-status-appveyor| image:: https://ci.appveyor.com/api/projects/status/aygfxqlf5lccm7sx/branch/master?svg=true
   :target: https://ci.appveyor.com/project/JB-MS/ursgal
   :alt: AppVeyor CI status

.. |doc-status| image:: http://readthedocs.org/projects/ursgal/badge/?version=latest
   :target: http://ursgal.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |Gitter| image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :alt: Join the chat at https://gitter.im/ursgal/ursgal
   :target: https://gitter.im/ursgal/ursgal?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

Summary
*******

Ursgal is a Python module that offers a generalized interface to common bottom-up proteomics tools, e.g.

    a) Peptide spectrum matching with up to five different search engines (some available in multiple versions)

    b) Evaluation and post processing of search results with up to two different engines

    c) Integration of search results from different search engines

    d) Creation of a target decoy database

Abstract
********

Proteomics data integration has become a broad field with a variety of programs offering innovative algorithms to analyze increasing amounts of data. Unfortunately, this software diversity leads to many problems as soon as the data is analyzed using more than one algorithm for the same task. Although it was shown that the combination of multiple peptide identification algorithms yields more robust results (Nahnsen et al. 2011, Vaudel et al. 2015, Kwon et al. 2011), it is only recently that unified approaches are emerging (Vaudel et al. 2011, Wen et al. 2015); however, workflows that, for example, aim to optimize search parameters or that employ cascaded style searches (Kertesz-Farkas et al. 2015) can only be made accessible if data analysis becomes not only unified but also and most importantly scriptable. Here we introduce Ursgal, a Python interface to many commonly used bottom-up proteomics tools and to additional auxiliary programs. Complex workflows can thus be composed using the Python scripting language using a few lines of code. Ursgal is easily extensible, and we have made several database search engines (X!Tandem (Craig and Beavis 2004), OMSSA (Geer et al. 2004), MS-GF+ (Kim et al. 2010), Myrimatch (Tabb et al. 2008), MS Amanda (Dorfer et al. 2014)), statistical postprocessing algorithms (qvality (Käll et al. 2009), Percolator (Käll et al. 2008)), and one algorithm that combines statistically postprocessed outputs from multiple search engines (“combined FDR” (Jones et al. 2009)) accessible as an interface in Python. Furthermore, we have implemented a new algorithm (“combined PEP”) that combines multiple search engines employing elements of “combined FDR” (Jones et al. 2009), PeptideShaker (Vaudel et al. 2015), and Bayes’ theorem.

*Kremer, L. P. M., Leufken, J., Oyunchimeg, P., Schulze, S. and Fufezan, C.
(2015):* |publicationtitle|_ *, Journal of Proteome research, 15, 788-.
DOI:10.1021/acs.jproteome.5b00860*

.. _publicationtitle: http://dx.doi.org/10.1021/acs.jproteome.5b00860
.. |publicationtitle| replace:: *Ursgal, Universal Python Module Combining Common Bottom-Up Proteomics Tools for Large-Scale Analysis*
.. _download:

Download
********

Get the latest version via GitHub:
    | https://github.com/ursgal/ursgal

as .zip package:
   | https://github.com/ursgal/ursgal/archive/master.zip

or via git clone URL:
   | https://github.com/ursgal/ursgal.git

The complete Documentation can be found at
   | http://ursgal.readthedocs.org/


.. _installation:

Installation
************

Ursgal requires `Python`_ 3.4 or higher.

Download Ursgal using `GitHub`_ **or** the zip file:

* GitHub version: Starting with this the easiest way is to clone the GitHub repo.::

   user@localhost:~$ git clone https://github.com/ursgal/ursgal.git


* ZIP version: Alternatively, download and extract the `ursgal zip file`_

.. _Python:
   https://www.python.org/downloads/

.. _GitHub:
   https://github.com/ursgal/ursgal

.. _ursgal zip file:
   https://github.com/ursgal/ursgal/archive/master.zip

Install requirements::

    user@localhost:~$ cd ursgal
    user@localhost:~/ursgal$ pip3.4 install -r requirements.txt

.. note::

    Pip is included in Python 3.4 and higher. However, it might not be
    included in in your system's PATH environment variable.
    If this is the case, you can either add the Python scripts directory to your
    PATH env variable or use the path to the pip.exe directly for the
    installation, e.g.: ~/Python34/Scripts/pip.exe install -r requirements.txt

Install third party engines::

    user@localhost:~/ursgal$ python3.4 install_resources.py


Install Ursgal::

    user@localhost:~/ursgal$ python3.4 setup.py install


.. note::

    Under Linux, it may be required to change the permission in the
    python3.4 site-package folder so that all files are executable

(You might need administrator privileges to write in the Python site-package folder.
On Linux or OS X, use ```sudo python setup.py install``` or write into a user folder
by using this command ```python setup.py install --user```. On Windows, you have to
start the command line with administrator privileges.)


Tests
*****

Run nosetests in root folder. You might need to install `nose`_ for Python3 first
although it is in the requirements.txt (above) thus pip3.4 install -r requirements
should have installed it already. Then just execute::

    user@localhost:~/ursgal$ nosetests3

to test the package.

.. _nose:
    https://nose.readthedocs.org/en/latest/



Participate
***********

Fork us at https://github.com/ursgal/ursgal and open up pull requests! Thanks!

If you encounter any problems you can open up issues at GitHub, join the conversation at Gitter, or write an email to ursgal.team@gmail.com


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

Copyright 2014-2015 by authors and contributors in alphabetical order

* Christian Fufezan,
* Lukas P. M. Kremer
* Johannes Leufken
* Purevdulam Oyunchimeg
* Stefan Schulze
* Kazuhiko Sugimoto
* Lukas Vaut

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

Lukas P. M. Kremer, Johannes Leufken, Purevdulam Oyunchimeg, Stefan Schulze, and Christian Fufezan (2015): `Ursgal, Universal Python Module Combining Common Bottom-Up Proteomics Tools for Large-Scale Analysis`_, Journal of Proteome research, DOI:10.1021/acs.jproteome.5b00860

.. _Ursgal, Universal Python Module Combining Common Bottom-Up Proteomics Tools for Large-Scale Analysis: http://dx.doi.org/10.1021/acs.jproteome.5b00860

.. note::
    Please cite every tool you use in Ursgal. During runtime the references of
    the tools you were using are shown.

Full list of tools with proper citations that are integrated into Ursgal are:

    * Craig, R.; Beavis, R. C. TANDEM: matching proteins with tandem mass spectra. Bioinformatics 2004, 20 (9), 1466–1467.
    * Dorfer, V.; Pichler, P.; Stranzl, T.; Stadlmann, J.; Taus, T.; Winkler, S.; Mechtler, K. MS Amanda, a Universal Identification Algorithm Optimised for High Accuracy Tandem Mass Spectra. J. Proteome res. 2014.
    * Frank, A. M.; Savitski, M. M.; Nielsen, M. L.; Zubarev, R. A. and Pevzner, P. A. De Novo Peptide Sequencing and Identification with Precision Mass Spectrometry. J. Proteome Res. 2007 6:114-123.',
    * Geer, L. Y.; Markey, S. P.; Kowalak, J. A.; Wagner, L.; Xu, M.; Maynard, D. M.; Yang, X.; Shi, W.; Bryant, S. H. Open Mass Spectrometry Search Algorithm. J. Proteome res. 2004, 3 (5), 958–964.
    * Jones, A. R.; Siepen, J. a.; Hubbard, S. J.; Paton, N. W. Improving sensitivity in proteome studies by analysis of false discovery rates for multiple search engines. Proteomics 2009, 9 (5), 1220–1229.
    * Kim, S.; Mischerikow, N.; Bandeira, N.; Navarro, J. D.; Wich, L.; Mohammed, S.; Heck, A. J. R.; Pevzner, P. A. The generating function of CID, ETD, and CID/ETD pairs of tandem mass spectra: applications to database search. MCP 2010, 2840–2852.
    * Käll, L.; Canterbury, J. D.; Weston, J.; Noble, W. S.; MacCoss, M. J. Semi-supervised learning for peptide identification from shotgun proteomics datasets. Nature methods 2007, 4 (11), 923–925.
    * Käll, L.; Storey, J. D.; Noble, W. S. Qvality: Non-parametric estimation of q-values and posterior error probabilities. Bioinformatics 2009, 25 (7), 964–966.
    * Ma, B. Novor: real-time peptide de novo sequencing software. J Am Soc Mass Spectrom. 2015 Nov;26(11):1885-94
    * Reisinger, F.; Krishna, R.; Ghali, F.; Ríos, D.; Hermjakob, H.; Antonio Vizcaíno, J.; Jones, A. R. JmzIdentML API: A Java interface to the mzIdentML standard for peptide and protein identification data. Proteomics 2012, 12 (6), 790–794.
    * Tabb, D. L.; Fernando, C. G.; Chambers, M. C. MyriMatch: highly accurate tandem mass spectral peptide identification by multivariate hypergeometric analysis. J Proteome Res. 2008, 6 (2), 654–661.
