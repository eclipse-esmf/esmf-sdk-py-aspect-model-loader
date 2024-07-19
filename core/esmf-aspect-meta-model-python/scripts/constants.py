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

from os.path import join
from string import Template


SAMM_VERSION = "2.1.0"
JAVA_CLI_VERSION = "2.7.0"


class SAMMCliConstants:
    BASE_PATH = Template("https://github.com/eclipse-esmf/esmf-sdk/releases/download/v$version_number/$file_name")
    JAVA_CLI_VERSION = JAVA_CLI_VERSION
    LINUX_FILE_NAME = Template("samm-cli-$version_number-linux-x86_64.tar.gz")
    SAMM_VERSION = SAMM_VERSION
    WIN_FILE_NAME = Template("samm-cli-$version_number-windows-x86_64.zip")


class TestModelConstants:
    FOLDER_TO_EXTRACT = "valid"
    JAVA_CLI_VERSION = JAVA_CLI_VERSION
    MAVEN_URL = Template(
        "https://repo1.maven.org/maven2/org/eclipse/esmf/esmf-test-aspect-models/$version_number/"
        "esmf-test-aspect-models-$version_number.jar"
    )
    SAMM_VERSION = SAMM_VERSION
    TEST_MODELS_PATH = join("tests", "integration", "java_models", "resources")
