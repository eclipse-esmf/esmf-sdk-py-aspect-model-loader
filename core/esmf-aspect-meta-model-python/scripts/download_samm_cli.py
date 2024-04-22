"""Download SAMM CLI.

Windows: https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.6.1/samm-cli-2.6.1-windows-x86_64.zip
  Linux: https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.6.1/samm-cli-2.6.1-linux-x86_64.tar.gz
    JAR: https://github.com/eclipse-esmf/esmf-sdk/releases/download/v2.6.1/samm-cli-2.6.1.jar
"""

import os
from pathlib import Path
import platform
import requests
import sys
import zipfile

from string import Template

BASE_PATH = Template("https://github.com/eclipse-esmf/esmf-sdk/releases/download/v$version_number/$file_name")
LINUX_FILE_NAME = Template("samm-cli-$version_number-linux-x86_64.tar.gz")
SAMM_CLI_VERSION = "2.6.1"
WIN_FILE_NAME = Template("samm-cli-$version_number-windows-x86_64.zip")


def get_samm_cli_file_name():
    """Get a SAMM CLI file name for the current platform."""

    if platform.system() == "Windows":
        file_name = WIN_FILE_NAME.substitute(version_number=SAMM_CLI_VERSION)
    elif platform.system() == "Linux":
        file_name = LINUX_FILE_NAME.substitute(version_number=SAMM_CLI_VERSION)
    else:
        raise NotImplementedError(
            f"Please download a SAMM CLI manually for your operation system from '{BASE_PATH}'"
        )

    return file_name


def download_archive_file(url, archive_file):
    """Download an archive file."""
    with open(archive_file, "wb") as f:
        print("Downloading %s" % archive_file)
        response = requests.get(url, allow_redirects=True, stream=True)
        content_len = response.headers.get('content-length')

        if content_len is None:
            f.write(response.content)
        else:
            total_len = int(content_len)
            data_len = 0
            chunk = 4096
            progress_bar_len = 50

            for content_data in response.iter_content(chunk_size=chunk):
                data_len += len(content_data)

                f.write(content_data)

                curr_progress = int(50 * data_len / total_len)
                sys.stdout.write(f"\r[{'*' * curr_progress}{' ' * (progress_bar_len - curr_progress)}]")
                sys.stdout.flush()


def download_samm_cli():
    try:
        samm_cli_file_name = get_samm_cli_file_name()
    except NotImplementedError as error:
        print(error)
    else:
        print(f"Start downloading SAMM CLI {samm_cli_file_name}")
        url = BASE_PATH.substitute(version_number=SAMM_CLI_VERSION, file_name=samm_cli_file_name)
        dir_path = Path(__file__).resolve().parents[1]
        archive_file = os.path.join(dir_path, samm_cli_file_name)

        download_archive_file(url, archive_file)
        print("\nSAMM CLI archive file downloaded")

        print("Start extracting files")
        archive = zipfile.ZipFile(archive_file)
        for file in archive.namelist():
            archive.extract(file, "samm-cli")
        archive.close()
        print("Done extracting files.")

        print("Deleting SAMM CLI archive file.")
        os.remove(archive_file)


if __name__ == "__main__":
    download_samm_cli()
