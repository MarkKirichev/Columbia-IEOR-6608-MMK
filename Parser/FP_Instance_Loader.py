#! /usr/bin/python
# Copyright (c) 2023 Mark Kirichev

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

LOADERS = {
    "json": load_json_instance
}

def get_extension(file_name: str):
    return file_name.split(".")[-1] if "." in file_name else None

def list_parsers():
    return LOADERS.keys()

def load_instance(file_name):
    ext = get_extension(file_name)
    print(file_name)
    load = LOADERS[ext]
    return load(file_name)
