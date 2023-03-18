# #########################################################################
# Copyright (c) 2022, UChicago Argonne, LLC. All rights reserved.         #
#                                                                         #
# Copyright 2022. UChicago Argonne, LLC. This software was produced       #
# under U.S. Government contract DE-AC02-06CH11357 for Argonne National   #
# Laboratory (ANL), which is operated by UChicago Argonne, LLC for the    #
# U.S. Department of Energy. The U.S. Government has rights to use,       #
# reproduce, and distribute this software.  NEITHER THE GOVERNMENT NOR    #
# UChicago Argonne, LLC MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR        #
# ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  If software is     #
# modified to produce derivative works, such modified software should     #
# be clearly marked, so as not to confuse it with the version available   #
# from ANL.                                                               #
#                                                                         #
# Additionally, redistribution and use in source and binary forms, with   #
# or without modification, are permitted provided that the following      #
# conditions are met:                                                     #
#                                                                         #
#     * Redistributions of source code must retain the above copyright    #
#       notice, this list of conditions and the following disclaimer.     #
#                                                                         #
#     * Redistributions in binary form must reproduce the above copyright #
#       notice, this list of conditions and the following disclaimer in   #
#       the documentation and/or other materials provided with the        #
#       distribution.                                                     #
#                                                                         #
#     * Neither the name of UChicago Argonne, LLC, Argonne National       #
#       Laboratory, ANL, the U.S. Government, nor the names of its        #
#       contributors may be used to endorse or promote products derived   #
#       from this software without specific prior written permission.     #
#                                                                         #
# THIS SOFTWARE IS PROVIDED BY UChicago Argonne, LLC AND CONTRIBUTORS     #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT       #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS       #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL UChicago     #
# Argonne, LLC OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,        #
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,    #
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;        #
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER        #
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT      #
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN       #
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         #
# POSSIBILITY OF SUCH DAMAGE.                                             #
# #########################################################################

import os
import sys
import h5py
import numpy
import json

from collections import deque

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

def _get_subgroups(hdf_object, key=None):
    """
    Supplementary method for building the tree view of a hdf5 file.
    Return the name of subgroups.
    """
    list_group = []
    if key is None:
        for group in hdf_object.keys():
            list_group.append(group)
        if len(list_group) == 1:
            key = list_group[0]
        else:
            key = ""
    else:
        if key in hdf_object:
            try:
                obj = hdf_object[key]
                if isinstance(obj, h5py.Group):
                    for group in hdf_object[key].keys():
                        list_group.append(group)
            except KeyError:
                pass
    if len(list_group) > 0:
        list_group = sorted(list_group)
    return list_group, key


def _add_branches(tree, hdf_object, key, key1, index, last_index, prefix,
                  connector, level, add_shape):
    """
    Supplementary method for building the tree view of a hdf5 file.
    Add branches to the tree.
    """
    shape = None
    key_comb = key + "/" + key1
    if add_shape is True:
        if key_comb in hdf_object:
            try:
                obj = hdf_object[key_comb]
                if isinstance(obj, h5py.Dataset):
                    shape = str(obj.shape)
            except KeyError:
                shape = str("-> ???External-link???")
    if shape is not None:
        tree.append(f"{prefix}{connector} {key1} {shape}")
    else:
        tree.append(f"{prefix}{connector} {key1}")
    if index != last_index:
        prefix += PIPE_PREFIX
    else:
        prefix += SPACE_PREFIX
    _make_tree_body(tree, hdf_object, prefix=prefix, key=key_comb,
                    level=level, add_shape=add_shape)


def _make_tree_body(tree, hdf_object, prefix="", key=None, level=0,
                    add_shape=True):
    """
    Supplementary method for building the tree view of a hdf5 file.
    Create the tree body.
    """
    entries, key = _get_subgroups(hdf_object, key)
    num_ent = len(entries)
    last_index = num_ent - 1
    level = level + 1
    if num_ent > 0:
        if last_index == 0:
            key = "" if level == 1 else key
            if num_ent > 1:
                connector = PIPE
            else:
                connector = ELBOW if level > 1 else ""
            _add_branches(tree, hdf_object, key, entries[0], 0, 0, prefix,
                          connector, level, add_shape)
        else:
            for index, key1 in enumerate(entries):
                connector = ELBOW if index == last_index else TEE
                if index == 0:
                    tree.append(prefix + PIPE)
                _add_branches(tree, hdf_object, key, key1, index, last_index,
                              prefix, connector, level, add_shape)


def get_hdf_tree(file_path, output=None, add_shape=True, display=True):
    """
    Get the tree view of a hdf/nxs file.

    Parameters
    ----------
    file_path : str
        Path to the file.
    output : str or None
        Path to the output file in a text-format file (.txt, .md,...).
    add_shape : bool
        Including the shape of a dataset to the tree if True.
    display : bool
        Print the tree onto the screen if True.

    Returns
    -------
    list of string
    """
    hdf_object = h5py.File(file_path, 'r')
    tree = deque()
    _make_tree_body(tree, hdf_object, add_shape=add_shape)
    if output is not None:
        make_folder(output)
        output_file = open(output, mode="w", encoding="UTF-8")
        with output_file as stream:
            for entry in tree:
                print(entry, file=stream)
    else:
        if display:
            for entry in tree:
                print(entry)
    return tree