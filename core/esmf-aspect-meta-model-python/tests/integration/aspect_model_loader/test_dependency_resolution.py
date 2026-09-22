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

import platform

from os import makedirs, remove
from os.path import abspath, dirname, isfile, join

from rdflib.term import URIRef

from esmf_aspect_meta_model_python.resolver.local_file import LocalFileResolver


class TestDependencyResolution:
    """Test dependency resolution for local aspect model files."""

    ROOT_PATH: str = dirname(dirname(abspath(__file__)))
    SOURCE_PATH = join(ROOT_PATH, "resources", "traversal_dependency")
    SECRET_PATH = join(ROOT_PATH, "secrets")

    model_path = ["models", "org.example.test", "1.0.0"]
    secret_path = ["secrets", "1.0.0"]

    @classmethod
    def setup_class(cls):
        """Create the model and dependency files used by the tests."""
        cls.evil_model_dir = join(cls.ROOT_PATH, cls.SOURCE_PATH, *cls.model_path)
        cls.evil_model_name = "Evil.ttl"
        cls._create_file(cls.evil_model_dir, cls.evil_model_name)

        cls.secret_dir = join(cls.ROOT_PATH, cls.SOURCE_PATH, *cls.secret_path)
        cls.secret_model_name = "confidential.ttl"
        cls._create_file(cls.secret_dir, cls.secret_model_name)

    @classmethod
    def _create_file(cls, file_path, file_name):
        """Create a test Turtle file at the specified path."""
        file_full_path = join(file_path, file_name)

        if isfile(file_full_path):
            remove(file_full_path)

        makedirs(file_path, exist_ok=True)

        if file_name == cls.evil_model_name:
            cls._create_evil_model_file(file_full_path)
        elif file_name == cls.secret_model_name:
            cls._create_secret_model_file(file_full_path)
        else:
            raise NotImplementedError(f"Unknown file name: {file_name}")

    @classmethod
    def _create_evil_model_file(cls, file_full_path):
        """Create a model containing an absolute dependency namespace path."""
        with open(file_full_path, "w") as f:
            # absolute path component → os.path.join discards base_path entirely
            f.write(
                "@prefix samm: <urn:samm:org.eclipse.esmf.samm:meta-model:2.2.0#> .\n"
                f'@prefix evil: <urn:samm:{join(cls.ROOT_PATH, cls.SOURCE_PATH, "secrets")}:1.0.0#> .\n'
                "<urn:samm:org.example.test:1.0.0#Evil> a samm:Aspect ;\n"
                "   samm:properties () ; samm:operations () .\n"
            )

    @classmethod
    def _create_secret_model_file(cls, file_full_path):
        """Create a dependency file containing a value that must not be loaded."""
        with open(join(file_full_path), "w") as f:
            f.write(
                "@prefix samm: <urn:samm:org.eclipse.esmf.samm:meta-model:2.2.0#> .\n"
                "@prefix ex: <http://example.com/secret#> .\n"
                'ex:LeakedSecret ex:value "TOP-SECRET-CREDENTIAL-12345" .\n'
            )

    @classmethod
    def teardown_class(cls):
        """Remove the model file created for the tests."""
        remove(join(cls.evil_model_dir, cls.evil_model_name))

    def test_parse_namespace_relative_path_return_path(self):
        """Verify that relative namespace paths are parsed normally."""
        result = LocalFileResolver._parse_namespace("urn:samm:../secrets:1.0.0#")

        assert result == ("../secrets", "1.0.0")

    def test_parse_namespace_absolute_path_return_none(self):
        """Verify that absolute namespace paths are ignored."""
        if platform.system() == "Windows":
            param = "urn:samm:C:\\etc:1.0.0#"
        else:
            param = "urn:samm:/etc:1.0.0#"
        result = LocalFileResolver._parse_namespace(param)

        assert result == (None, None)

    def test_read_secrets(self):
        """Verify that an absolute dependency path cannot load the secret file."""
        local_file_resolver = LocalFileResolver()
        graph = local_file_resolver.read(join(self.evil_model_dir, self.evil_model_name))
        local_file_resolver.prepare_aspect_model(graph)
        result = list(local_file_resolver.graph.triples((URIRef("http://example.com/secret#LeakedSecret"), None, None)))

        assert len(result) == 0
