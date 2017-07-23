Contribution guidelines
#######################

Beta stage. If you find typos, please fix them :)

*Ursgal - Universal Python Module Combining Common Bottom-Up Proteomics Tools for Large-Scale Analysis*


Summary
*******

In general, contribution to Ursgal is very welcome! Feel free to fork and/or clone
Ursgal. If you want to improve code or contribute new nodes/tools/algorithms
please read these guidelines first. If something is unclear please contact one
of the authors for help or let us know via e.g. an issue.


Commit messages
***************

First of all, please be concise and as descriptive (explicit is better than 
implicit :) ) as possible. It is always
helpful to point out, which parts of Ursgal were changed/fixed (e.g.
documentation or example scripts etc. ). In the same time, please avoid
unneccesarily long messages.


Parameters
**********

The central idea of Ursgal are the unified parameters. The central parameter is 
tranlated, so that every engine can use it. This means, if you implement a new
engine, you have to go through the (more or less) tedious process to check, if
parameter X of the new engine Y is already listed in uparams.py. We require
to be very thorough in this process. Having the same parameter multiple times
must be avoided! There may be difficult cases, to decide if the parameter is
actually the same, but by using the translation system in Ursgal, some
adjusments can be made. Please refer to the documentation for further
instructions and considerations on the parameters.


Code standards and conventions
******************************

Since this a collaborative project, you will encounter different coding styles.
Despite the fact that we know that diversity is beautiful, we need to keep some
common line on how to code (This list may be further extended). Please refer
also to the PEP8 style guide, which we use generally 
https://www.python.org/dev/peps/pep-0008/). Additionally this list will give
you some things to think about:

  | Re-think naming of variables at least twice
  | Re-check deleting of own debug code before Pull-requests



Test philosophy
***************

Test your code! Seriously, test you code! If you add new functionality or nodes
at the same time provide (a) test function(s). We have already a set of tests
and different files, which can be used for the test. Avoid adding new test files
if possible to keep the repo small.


Sphinx guide
************

We use Sphinx to automatically build and format the documentation. Please keep
this style in your docstrings


Other rules and cosiderations
*****************************

None so far.

Merge/pull requests
*******************

Please use the pull request to push your code to the master repository. It will
be automatically tested by Travis and AppVeyor if the module is still working in
unix and Windows environments. Pull requests will be discussed by the main dev
team and merged into Ursgal.


Issues
****** 

If you have an issue or problem, please first search all open issues and pull
request to avoid duplication of efforts. If you have a fix for the problem you
may directly open a pull requets. On the other hand, if you plan to or
are already working on implementing new stuff, you may also open an issue and
(pre-) announce your contribution. Please tag then the issue with
'enhancement'. In general the core team of Ursgal will also take care of crucial
bugs in the main code. Since Ursgal is open source, we cannot maintain every
and assure its compatibility and functionality (please be reminded here to test
your code, seriously, test your code)


Citation
********

If you use Ursagl, do not forget to cite us

*Kremer, L. P. M., Leufken, J., Oyunchimeg, P., Schulze, S. and Fufezan, C.
(2015):* |publicationtitle|_ *, Journal of Proteome research, 15, 788-.
DOI:10.1021/acs.jproteome.5b00860*

.. _publicationtitle: http://dx.doi.org/10.1021/acs.jproteome.5b00860
.. |publicationtitle| replace:: *Ursgal, Universal Python Module Combining Common Bottom-Up Proteomics Tools for Large-Scale Analysis*



.. note::

    Pip is included in Python 3.4 and higher. However, it might not be
    included in your system's PATH environment variable.
    If this is the case, you can either add the Python scripts directory to your
    PATH env variable or use the path to the pip.exe directly for the
    installation, e.g.: ~/Python34/Scripts/pip.exe install -r requirements.txt



Copyrights
***********

Copyright 2014-2015 by authors and contributors in alphabetical order

* Christian Fufezan
* Manuel Koesters
* Lukas P. M. Kremer
* Johannes Leufken
* Purevdulam Oyunchimeg
* Stefan Schulze
* Kazuhiko Sugimoto
* Lukas Vaut




