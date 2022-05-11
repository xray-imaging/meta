import os
import sys
import h5py

from collections import deque

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

def read_hdf(fname, add_shape=True):
    """
    Get the tree view of a hdf/nxs file.

    Parameters
    ----------
    file_path : str
        Path to the file.
    add_shape : bool
        Including the shape of a dataset to the tree if True.

    Returns
    -------
    list of string
    """

    tree = deque()
    meta = {}

    with h5py.File(fname, 'r') as hdf_object:
        _extract_hdf(tree, meta, hdf_object, add_shape=add_shape)
    # for entry in tree:
    #     print(entry)
    return tree, meta

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

def _add_branches(tree, meta, hdf_object, key, key1, index, last_index, prefix,
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
                    if obj.shape[0]==1:
                        value = obj[()][0]
                        attr = obj.attrs.get('units')
                        if attr != None:
                            attr = attr.decode('UTF-8')
                            # print(">>>>>> %s: %s %s" % (obj.name, value, attr))
                        if  (value.dtype.kind == 'S'):
                            value = value.decode(encoding="utf-8")
                            # print(">>>>>> %s: %s" % (obj.name, value))
                        meta.update( {obj.name : [value, attr] } )
            except KeyError:
                shape = str("-> ???External-link???")
            except IndexError:
                shape = "None"
    if shape is not None:
        tree.append(f"{prefix}{connector} {key1} {shape}")
    else:
        tree.append(f"{prefix}{connector} {key1}")
    if index != last_index:
        prefix += PIPE_PREFIX
    else:
        prefix += SPACE_PREFIX
    _extract_hdf(tree, meta, hdf_object, prefix=prefix, key=key_comb,
                    level=level, add_shape=add_shape)

def _extract_hdf(tree, meta, hdf_object, prefix="", key=None, level=0,
                    add_shape=True):
    """
    Supplementary method for extracting from a generic hdf file the meta data 
    tree view and the 1D meta data values/units.
    Create the tree body and a meta dictionary 
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
            _add_branches(tree, meta, hdf_object, key, entries[0], 0, 0, prefix,
                          connector, level, add_shape)
        else:
            for index, key1 in enumerate(entries):
                connector = ELBOW if index == last_index else TEE
                if index == 0:
                    tree.append(prefix + PIPE)
                _add_branches(tree, meta, hdf_object, key, key1, index, last_index,
                              prefix, connector, level, add_shape)

