#! /usr/bin/python

# Copyright (c) 2019 Mark Kirichev

from collections import namedtuple
from .FP_JSON_Parser import load_json_instance

Instance = namedtuple(
    typename="Instance",
    field_names=[
        "obj",
        "constr_mat",
        "constr_vec"
    ]
)

LOADERS = { "json": load_json_instance }

def get_extension(file_name: str):
    index = file_name.find(".")
    if not index == -1:
        return file_name[index + 1 :]
    else:
        return None

def list_parsers():
    return LOADERS.keys()

def load_instance(file_name):
    ext = get_extension(file_name)
    load = LOADERS[ext]
    return load(file_name)
