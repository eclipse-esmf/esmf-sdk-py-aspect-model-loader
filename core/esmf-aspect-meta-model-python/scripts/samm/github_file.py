#  Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0


class GitFile:
    def __init__(self, name: str, path: str, sha: str, size: int, url: str):
        self.name = name
        self.path = path
        self.sha = sha
        self.size = size
        self.url = url

    @staticmethod
    def from_json(json_dct):
        return GitFile(
            json_dct["name"],
            json_dct["path"],
            json_dct["sha"],
            json_dct["size"],
            json_dct["download_url"],
        )
