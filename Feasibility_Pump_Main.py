#! /usr/bin/python

# Copyright (c) 2023 Mark Kirichev

from argparse import ArgumentParser
from BinaryFP.FP_Binary_Main import feasibility_pump
from Parser.FP_Instance_Loader import load_instance, list_parsers


def arg_parser():
    parser = ArgumentParser(description='Find a feasible solution to a Binary Programming problem')

    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument(
        "-i",
        "--instance",
        help="specify the instance to solve"
    )

    input_group.add_argument(
        '-l',
        '--list',
        help='list known file formats',
        default=False,
        action='store_true'
    )

    parser.add_argument(
        '--log',
        default=False,
        action='store_true',
        help='enable informational logging'
    )

    return parser.parse_args()


def solve_instance(file_name, log):
    c, A, b = load_instance(file_name)

    sol, stat = feasibility_pump(c, A, b, log)
    if stat:
        print("Solution Found:")
        print(sol)
    else:
        print("Unable to find a feasible solution")


def main():
    args = arg_parser()
    if args.list:
        for i in list_parsers():
            print(i)
    else:
        solve_instance(args.instance, args.log)


if __name__ == "__main__":
    main()