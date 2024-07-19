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
import pathlib
import zipfile

import requests

SAMM_VERSION_TO_DOWNLOAD = "2.1.0"


def main():
    """Downloads the release .jar of the samm for the selected version and extracts the SAMM files"""
    download_jar(SAMM_VERSION_TO_DOWNLOAD)
    extract_jar(SAMM_VERSION_TO_DOWNLOAD)
    print("current path: ", pathlib.Path().resolve())


def download_jar(version):
    """Downloads the release .jar of the samm for the selected version"""

    print(f"Start downloading SAMM Version {version}")
    url = (
        f"https://repo1.maven.org/maven2/org/eclipse/esmf/esmf-semantic-aspect-meta-model/{version}/"
        f"esmf-semantic-aspect-meta-model-{version}.jar"
    )

    request = requests.get(url, allow_redirects=True)

    open(f"esmf-aspect-meta-model-{version}.jar", "wb").write(request.content)
    print("JAR-File Downloaded")


def extract_jar(version):
    """Copies all folders in the archive that start with "samm" into the
    samm_aspect_meta_model folder. The archive gets deleted afterwards
    """
    print(f"Start extracting files from esmf-aspect-meta-model-{version}.jar")
    archive = zipfile.ZipFile(f"esmf-aspect-meta-model-{version}.jar")
    for file in archive.namelist():
        if file.startswith("samm"):
            archive.extract(file, "./esmf_aspect_meta_model_python/samm_aspect_meta_model")
    archive.close()
    print("Done extracting files.")

    print("Deleting SAMM JAR file.")
    os.remove(f"esmf-aspect-meta-model-{version}.jar")
