====
meta
====

**meta** is a python library providing support to the meta data reading from a file. Currently **meta** support only hdf but other formats can be added using the same model.

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
