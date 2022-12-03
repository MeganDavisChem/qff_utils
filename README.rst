=========
qff_utils
=========


#.. image:: https://img.shields.io/pypi/v/qff_utils.svg
#        :target: https://pypi.python.org/pypi/qff_utils

#.. image:: https://img.shields.io/travis/MeganDavisChem/qff_utils.svg
#        :target: https://travis-ci.com/MeganDavisChem/qff_utils

.. image:: https://readthedocs.org/projects/qff-utils/badge/?version=latest
        :target: https://qff-utils.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




Various python utilities to make working with QFFs easier.
This will probably only be relevant to our research group, but it's
a good opportunity for me to practice project management :).

This repo is currently under construction, but should be usable.
I think you need Python >3.9, probably the simplest way to install everything you need is
to install anaconda and activate the proper environment on shell login.


* Free software: MIT license
* Documentation: https://qff-utils.readthedocs.io.


Features
--------

* XQPGen: Generate points for an XS QFF
* spec2latex: Convert summarize output to LaTeX table (deprecated, needs to be updated for rsummarize)
* qff-helper: Automates processing steps from energy.dat file to spectro2.out. Redundant functionality w/ pbQFF,
  so mostly only useful if you really like python
* misc: WIP utilities and oddball scripts

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
