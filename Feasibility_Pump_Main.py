#! /usr/bin/python
# Copyright (c) 2023 Mark Kirichev

import requests
import gzip
import sys
import os

from argparse import ArgumentParser
from BinaryFP.FP_Binary_Main import feasibility_pump
from Parser.FP_Instance_Loader import load_instance, list_parsers
from Gurobi_MIPs_Solver import model_to_json


def arg_parser():
    parser = ArgumentParser(description='Find a feasible solution to a Binary Programming problem!')

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
        help='logging will be displayed'
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


def get_miplib_file(miplib_file_name, remove_tar_gz=True):
    # Base URL for MIPLIB files
    base_url = "https://miplib.zib.de/WebData/instances/"

    # Construct the URL for the .mps file
    file_url = f"{base_url}{miplib_file_name}.mps.gz"

    # Directory to store the .mps file
    directory = "DatabaseMIPs"

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Temporary path for the downloaded .gz file
    temp_gz_path = f"{directory}/{miplib_file_name}.mps.gz"

    # Final path for the unpacked .mps file
    final_mps_path = f"{directory}/{miplib_file_name}.mps"

    # Attempt to download the .mps.gz file
    with requests.get(file_url, stream=True) as r:
        if r.status_code == 200:
            total_size = int(r.headers.get('content-length', 0))
            block_size = 1024 # 1 KB
            progress_bar = ""

            print(f"Downloading {miplib_file_name}.mps.gz")
            with open(temp_gz_path, 'wb') as file:
                for data in r.iter_content(block_size):
                    file.write(data)
                    progress_bar += "="
                    print(f"\rProgress: [{'=' * (len(progress_bar)//10)}{' ' * ((total_size//block_size//10) - len(progress_bar)//10)}] {len(progress_bar)*block_size/total_size*100:.2f}%", end="")
            print("\nDownload complete.")

            # Unpack the .gz file and save the .mps file
            with gzip.open(temp_gz_path, 'rb') as gz_file:
                with open(final_mps_path, 'wb') as mps_file:
                    mps_file.write(gz_file.read())

            # Optionally, remove the downloaded .gz file after unpacking
            if remove_tar_gz:
                os.remove(temp_gz_path)

            print(f"File unpacked and saved to {final_mps_path}")
            return final_mps_path
        else:
            raise FileNotFoundError(f"File '{miplib_file_name}' not found in MIPLIB.")


def main(args_parse=True):
    if args_parse:
        args = arg_parser()
        if args.list:
            for i in list_parsers():
                print(i)
        else:
           solve_instance(args.instance, args.log)
        return

    # if no arguments are passed, prompt for the file or for the file to be downloaded from MIPLIB and then processed
    print("Please, indicate the what file should be used an input to the FP: \n \t 1) MIPLIB file \n \t 2) Personal file")
    type_of_file = input()

    if not (type_of_file == "1" or type_of_file == "2"):
        raise ValueError("Please, use a valid indication!")

    if type_of_file == "1":
        print("Please, indicate the name of the .mps file that we should include as an input.\n")
        print("Example files are '10teams', 'air04', 'fast0507', 'vmp2', etc.")
        miplib_file_name = input()
        mps_file = get_miplib_file(miplib_file_name)

        if mps_file == "No such file":
            raise NameError("There's no such MIPLIB .mps file. Please, check the spelling and try again.")
        else:
            print(f"Starting the Feasibility Pump with input: {mps_file}")
            json_file_name = model_to_json(file_path=f'{mps_file}',
                                           output_file_path=f'{mps_file[:-4]}')
            solve_instance(json_file_name, "")

    if type_of_file == "2":
        print("Please, indicate the name and location of the .json file that we should include as an input.\n")
        test_file_location = input()

        try:
            with open(test_file_location, 'r') as mip_file:
                json_file_name = model_to_json(file_path=f'{test_file_location}',
                                               output_file_path=f'{mip_file}.json')
                print(f"Starting the Feasibility Pump with input: {mip_file}")
                print(json_file_name)
                solve_instance(json_file_name, "")

        except FileNotFoundError:
            print("No such file exists!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        instance = sys.argv[1]
        print(f"Instance passed: {instance}")
        main(args_parse=True)
    else:
        # If no instance is passed, prompt for user input
        main(args_parse=False)

    print("Binary Feasbility Pump terminated!")
