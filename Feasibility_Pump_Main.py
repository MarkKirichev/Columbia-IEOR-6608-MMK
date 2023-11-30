#! /usr/bin/python

# Copyright (c) 2023 Mark Kirichev

from argparse import ArgumentParser
from BinaryFP.FP_Binary_Main import feasibility_pump
from Parser.FP_Instance_Loader import load_instance, list_parsers
from Gurobi_MIPs_Solver import model_to_json


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
    # args = arg_parser()
    # if args.list:
    #     for i in list_parsers():
    #         print(i)
    # else:
    #    solve_instance(args.instance, args.log)

    print("Please, indicate the what file should be used an input to the FP: \n \t 1) MIPLIB file \n \t 2) Personal file")
    type_of_file = input()

    if not (type_of_file == "1" or type_of_file == "2"):
        raise ValueError("Please, use a valid indication!")

    if type_of_file == "1":
        print("Please, indicate the name of the .mps file that we should include as an input.\n")
        print("Example files are '10teams', 'air04', 'fast0507', 'vmp2', etc.")
        miplib_file_name = input()
        mps_file = get_miplib_file(miplib_file_name)
        mps_file_full = mps_file + '.mps'

        if mps_file == "No such file":
            raise NameError("There's no such MIPLIB .mps file. Please, check the spelling and try again.")
        else:
            print(f"Starting the Feasibility Pump with input: {mps_file_full}")
            json_file_name = model_to_json(file_path=f'DatabaseMIPs/{mps_file_full}',
                                           output_file_path=f'DatabaseMIPs/{mps_file}.json')
            solve_instance(json_file_name, "")

    if type_of_file == "2":
        print("Please, indicate the name and location of the .json file that we should include as an input.\n")
        test_file_name = input()
        # Check if the file exists ... TODO
        print(f"Starting the Feasibility Pump with input: {test_file_name}")
        solve_instance(test_file_name, "")

if __name__ == "__main__":
    main()
