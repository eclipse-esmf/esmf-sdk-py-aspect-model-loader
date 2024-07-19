#  Copyright (c) 2024 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

import shutil

from os import listdir, mkdir, remove
from os.path import exists, join
from pathlib import Path
from zipfile import ZipFile

import requests

from scripts.constants import TestModelConstants as Const


def get_resources_folder_path() -> str:
    """Get a path for storing test models."""
    base_path = Path(__file__).parents[1].absolute()
    models_path = join(base_path, Const.TEST_MODELS_PATH)

    return models_path


def clear_folder(resources_folder):
    """Remove all files to clear test models directory."""
    if exists(resources_folder) and len(listdir(resources_folder)) != 0:
        shutil.rmtree(resources_folder)

    mkdir(resources_folder)


def download_jar_file(jar_file_path: str):
    """Download JAR with test models."""
    url = Const.MAVEN_URL.substitute(version_number=Const.JAVA_CLI_VERSION)
    response = requests.get(url, allow_redirects=True)

    with open(jar_file_path, "wb") as f:
        f.write(response.content)


def extract_test_models(resources_folder: str, jar_file_path: str):
    """Unzip and extract test models."""
    archive = ZipFile(jar_file_path)
    for file_name in archive.namelist():
        if file_name.startswith(Const.FOLDER_TO_EXTRACT):
            archive.extract(file_name, resources_folder)

    archive.close()


def download_test_models(version: str = Const.JAVA_CLI_VERSION):
    """Downloads and extract the esmf-test-aspect-models."""
    print("Start a script to download the JAVA test Aspect Models")
    resources_folder = get_resources_folder_path()
    jar_file_name = f"esmf-test-aspect-models-{version}.jar"
    jar_file_path = join(resources_folder, jar_file_name)

    print(f"Remove previous version of test models from the folder {resources_folder}")
    clear_folder(resources_folder)

    print(f"Start downloading esmf-test-aspect-models version {version}")
    download_jar_file(jar_file_path)
    print("JAR-File Downloaded")

    print(f"Start extracting files from {jar_file_name} to the folder {resources_folder}")
    extract_test_models(resources_folder, jar_file_path)
    print("Done extracting files")

    print("Deleting esmf-test-aspect-models JAR file")
    remove(jar_file_path)


if __name__ == "__main__":
    download_test_models()
