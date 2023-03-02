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
from os import path, makedirs
import pathlib
from typing import Optional
import requests

from esmf_aspect_meta_model_python.samm_aspect_meta_model.github_folder import (
    GitFolder,
    decoding_url_response,
)


def main():
    url = "https://api.github.com/repos/eclipse-esmf/esmf-semantic-aspect-meta-model/contents/src/main/resources/bamm"
    #TODO url = "https://api.github.com/repos/eclipse-esmf/esmf-semantic-aspect-meta-model/contents/src/main/resources/samm"

    # in the pipeline machine an environment variable is set for the Github Token.
    # If the variable does not exists don't use authorization.
    github_token = os.getenv("GithubSdsBotToken")
    if github_token is None:
        headers = None
    else:
        headers = {"Authorization": f"token {github_token}"}

    samm_folder = GitFolder(
        "bamm",
        #TODO "samm",
        "",
        "",
        0,
        "",
        path.join("esmf_aspect_meta_model_python", "samm_aspect_meta_model", "bamm"),
        #TODO path.join("esmf_aspect_meta_model_python", "samm_aspect_meta_model", "samm"),
    )
    samm_folder = decoding_url_response(samm_folder, url, headers)
    download_samm_files(samm_folder, headers)


def download_samm_files(samm_folder: GitFolder, headers: Optional[dict]) -> None:
    download_files(samm_folder, headers)


def download_files(parent_folder: GitFolder, headers: Optional[dict]) -> None:
    current_path = pathlib.Path().resolve()
    for file in parent_folder.files:
        print(f"file: {file.name}")
        response = requests.get(file.url, headers=headers)
        file_path = path.join(current_path, parent_folder.local_path)
        if not path.exists(file_path):
            makedirs(file_path)
        open(path.join(file_path, file.name), "wb").write(response.content)
    for folder in parent_folder.folders:
        print(f"folder: {folder.name}")
        download_files(folder, headers)


if __name__ == "__main__":
    main()
