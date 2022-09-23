#  Copyright (c) 2022 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

import os
import zipfile
import pathlib
import requests


BAMM_VERSION_TO_DOWNLOAD = "2.0.0"


def main():
    """Downloads the release .JAR of the bamm for the selected version and extracts the BAMM files"""
    download_jar(BAMM_VERSION_TO_DOWNLOAD)
    extract_jar(BAMM_VERSION_TO_DOWNLOAD)
    print("current path: ", pathlib.Path().resolve())


def download_jar(version):
    """Downloads the release .JAR of the bamm for the selected version"""

    print(f"Start downloading BAMM Version {version}")
    url = f"https://github.com/OpenManufacturingPlatform/sds-bamm-aspect-meta-model/releases/download/v{version}/sds-aspect-meta-model-{version}.jar "

    request = requests.get(url, allow_redirects=True)

    open(f"sds-aspect-meta-model-{version}.jar", "wb").write(request.content)
    print("JAR-File Downloaded")


def extract_jar(version):
    """Copies all folders in the archive that start with "bamm" into the
    bamm_aspect_meta_model folder. The archive gets deleted afterwards
    """
    print(f"Start extracting files from sds-aspect-meta-model-{version}.jar")
    archive = zipfile.ZipFile(f"sds-aspect-meta-model-{version}.jar")
    for file in archive.namelist():
        if file.startswith("bamm"):
            archive.extract(file, "./sds_aspect_meta_model_python/bamm_aspect_meta_model")
    archive.close()
    print("Done extracting files.")

    print("Deleting BAMM JAR file.")
    os.remove(f"sds-aspect-meta-model-{version}.jar")
