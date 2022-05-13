====
meta
====

**meta** is a python library providing support for the meta data reading from a file. Currently **meta** support only hdf but other format meta-data extraction can be added using the same model.

At the Advanced Photon Source Imaging Group beamlines (2-BM, 7-BM and 32-ID) **meta** supports:

- `meta cli <https://github.com/xray-imaging/meta-cli>`_
- `tomolog cli <https://tomologcli.readthedocs.io/en/latest/>`_
- `tile <https://tile.readthedocs.io/en/latest/>`_

Installation
============

::

    $ git clone https://github.com/xray-imaging/meta.git
    $ cd meta
    $ python setup.py install

in a prepared virtualenv or as root for system-wide installation.

.. warning:: 
	If your python installation is in a location different from #!/usr/bin/env python please edit the first line of the bin/meta file to match yours.


Dependencies
============

- h5py
- numpy
- collections
