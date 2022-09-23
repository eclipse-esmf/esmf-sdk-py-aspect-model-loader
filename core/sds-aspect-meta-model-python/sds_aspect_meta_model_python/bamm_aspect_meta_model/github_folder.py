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

import json
from typing import List, Optional
from os import path
import requests
from sds_aspect_meta_model_python.bamm_aspect_meta_model.github_file import GitFile


class GitFolder(GitFile):
    def __init__(self, name: str, git_path: str, sha: str, size: int, url: str, local_path: str):
        super().__init__(name, git_path, sha, size, url)
        self.folders: List[GitFolder] = []
        self.files: List[GitFile] = []
        self.local_path = local_path

    @staticmethod
    def get_folder_from_json(json_folder, parent_local_path: str, headers: Optional[dict]) -> "GitFolder":
        git_folder = GitFolder(
            json_folder["name"],
            json_folder["path"],
            json_folder["sha"],
            json_folder["size"],
            json_folder["url"],
            path.join(parent_local_path, json_folder["name"]),
        )

        decoding_url_response(git_folder, git_folder.url, headers)

        return git_folder


def decoding_url_response(parent_folder: GitFolder, url: str, headers: Optional[dict]) -> GitFolder:
    print(f"requesting: {url}")
    response = requests.get(url, headers=headers, allow_redirects=True)
    if not response.ok:
        print(response.content)
        raise requests.RequestException

    json_result = json.loads(response.content)

    for json_object in json_result:
        object_type = json_object["type"]
        if object_type == "dir":
            parent_folder.folders.append(GitFolder.get_folder_from_json(json_object, parent_folder.local_path, headers))
        if object_type == "file":
            parent_folder.files.append(GitFile.from_json(json_object))
    return parent_folder
