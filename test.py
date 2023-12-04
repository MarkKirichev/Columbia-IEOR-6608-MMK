import requests
import gzip
import os

def get_miplib_file(miplib_file_name):
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
            block_size = 1024 # 1 Kibibyte
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
            os.remove(temp_gz_path)

            print(f"File unpacked and saved to {final_mps_path}")
            return final_mps_path
        else:
            raise FileNotFoundError(f"File '{miplib_file_name}' not found in MIPLIB.")


if __name__ == '__main__':
    miplib_file = input()

    get_miplib_file(miplib_file)
