"""Collect statistics about loading test Aspect models."""

import os
import shutil

from glob import glob
from os import listdir
from os.path import exists, join
from pathlib import Path

from esmf_aspect_meta_model_python import SAMMGraph
from scripts.constants import TestModelConstants
from scripts.download_test_models import download_test_models

# before start tests, download latest aspect test models with the next command
# poetry run download-test-models


def get_resources_folder_path() -> str:
    """Get a path for storing test models."""
    base_path = Path(__file__).parents[4].absolute()
    models_path = join(base_path, TestModelConstants.TEST_MODELS_PATH)

    return models_path


def check_resources_folder():
    """Remove all files to clear test models directory."""
    resources_folder = get_resources_folder_path()

    if not exists(resources_folder) or len(listdir(resources_folder)) == 0:
        download_test_models()


def get_test_files():
    """Get ttl models for testing."""
    resources_folder = get_resources_folder_path()
    search_pattern = join(
        resources_folder,
        TestModelConstants.FOLDER_TO_EXTRACT,
        TestModelConstants.TEST_MODELS_FOLDER,
        "**",
        "*.ttl",
    )
    test_model_files = glob(search_pattern, recursive=True)

    return test_model_files


def get_aspect_test_models():
    """Get files with aspect test models."""
    test_files = get_test_files()
    if not test_files:
        check_resources_folder()
        test_files = get_test_files()

    return test_files


def get_terminal_width():
    columns, _ = shutil.get_terminal_size(fallback=(120, 20))
    return columns


def check_load_aspect_model(test_models):
    total_models = len(test_models)
    report = {"passed": 0, "failed": 0, "errors": []}
    terminal_width = get_terminal_width()
    message = " SAMMGraph.load_aspect_model "
    fill_num = round((terminal_width - len(message)) / 2)
    print("=" * fill_num, message, "=" * (terminal_width - len(message) - fill_num), "\n", sep="")

    for i, model_path in enumerate(test_models):
        model_name = os.path.splitext(os.path.basename(model_path))[0]

        if model_name.lower().startswith("aspect"):
            try:
                samm_graph = SAMMGraph()
                samm_graph.parse(model_path)
                aspect = samm_graph.load_aspect_model()

                assert aspect
                assert samm_graph.aspect
            except Exception as error:
                status = "\033[91mFAILED\033[0m"
                report["failed"] += 1
                report["errors"].append(
                    {
                        "model_name": model_name,
                        "error": error,
                    }
                )
            else:
                status = "\033[92mSUCCESS\033[0m"
                report["passed"] += 1

            output_line = f"{model_name}: {status}"
            percentage = (i + 1) / total_models * 100
            right_data = f"[{percentage:6.2f}% ]"
            total_length = len(output_line) + len(right_data)
            spaces = terminal_width - total_length
            if spaces > 0:
                print(f"{output_line}{' ' * spaces}{right_data}")
            else:
                print(f"{output_line} {right_data}")

    print(f"\nResults:\n\033[92m{report['passed']:7.0f} passed\033[0m\n\033[91m{report['failed']:7.0f} failed\033[0m")
    for record in report["errors"]:
        print(f"{record['model_name']}: FAILED", {record["error"]})

    assert report["failed"] == 0, "Some models failed to load aspect model"


def check_load_model_elements(test_models):
    total_models = len(test_models)
    report = {"passed": 0, "failed": 0, "errors": []}
    terminal_width = get_terminal_width()
    message = " SAMMGraph.load_model_elements "
    fill_num = round((terminal_width - len(message)) / 2)
    print("=" * fill_num, message, "=" * (terminal_width - len(message) - fill_num), "\n", sep="")

    for i, model_path in enumerate(test_models):
        model_name = os.path.splitext(os.path.basename(model_path))[0]

        try:
            samm_graph = SAMMGraph()
            samm_graph.parse(model_path)
            elements = samm_graph.load_model_elements()

            assert elements
            assert samm_graph.model_elements
            if model_name.lower().startswith("aspect"):
                assert samm_graph.aspect
        except Exception as error:
            status = "\033[91mFAILED\033[0m"
            report["failed"] += 1
            report["errors"].append(
                {
                    "model_name": model_name,
                    "error": error,
                }
            )
        else:
            status = "\033[92mSUCCESS\033[0m"
            report["passed"] += 1

        output_line = f"{model_name}: {status}"
        percentage = (i + 1) / total_models * 100
        right_data = f"[{percentage:6.2f}% ]"
        total_length = len(output_line) + len(right_data)
        spaces = terminal_width - total_length
        if spaces > 0:
            print(f"{output_line}{' ' * spaces}{right_data}")
        else:
            print(f"{output_line} {right_data}")

    print(f"\nResults:\n\033[92m{report['passed']:7.0f} passed\033[0m\n\033[91m{report['failed']:7.0f} failed\033[0m")
    for record in report["errors"]:
        print(f"{record['model_name']}: FAILED", {record["error"]})

    assert report["failed"] == 0, "Some models failed to load model elements"


def test_load_aspect_model():
    test_models = get_aspect_test_models()
    assert test_models

    print("\nSubtests for checking aspect loading")
    check_load_aspect_model(test_models)


def test_load_model_elements():
    test_models = get_aspect_test_models()
    assert test_models

    print("\nSubtests for checking model element loading")
    check_load_model_elements(test_models)
