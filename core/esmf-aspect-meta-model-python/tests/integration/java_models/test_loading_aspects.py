"""Collect statistics about loading test Aspect models."""

import csv

from glob import glob
from os import listdir
from os.path import exists, join
from pathlib import Path

from esmf_aspect_meta_model_python.loader.aspect_loader import AspectLoader
from scripts.constants import TestModelConstants
from scripts.download_test_models import download_test_models


def get_resources_folder_path() -> str:
    """Get a path for storing test models."""
    base_path = Path(__file__).parents[3].absolute()
    models_path = join(base_path, TestModelConstants.TEST_MODELS_PATH)

    return models_path


def check_resources_folder(test_models_exists: bool = False):
    """Remove all files to clear test models directory."""
    resources_folder = get_resources_folder_path()

    if not exists(resources_folder) or len(listdir(resources_folder)) == 0 or not test_models_exists:
        download_test_models()


def get_test_files():
    """Get ttl models for testing."""
    resources_folder = get_resources_folder_path()
    samm_folder_name = f"samm_{TestModelConstants.SAMM_VERSION.replace('.', '_')}"
    search_pattern = join(resources_folder, "**", samm_folder_name, "**", "*.ttl")
    test_model_files = glob(search_pattern, recursive=True)

    return test_model_files


def load_test_models():
    """Test for loading Aspect models."""
    test_files = get_test_files()
    if not test_files:
        check_resources_folder()
        test_files = get_test_files()

    result = []
    all_test_files = len(test_files)
    i = 0
    step = 10
    print("Loading test Aspect models...")

    for test_file in test_files:
        i += 1
        if i % step == 0:
            print(f"{i}/{all_test_files}")

        test_file_path = Path(test_file)
        data = {
            "file_name": test_file_path.name,
            "folder_name": join(test_file_path.parents[1].name, test_file_path.parents[0].name),
            "status": "initializing",
            "error": None,
        }

        try:
            loader = AspectLoader()
            model_elements = loader.load_aspect_model(test_file)
            if not model_elements:
                raise Exception("No elements loaded")
        except Exception as error:
            data["error"] = str(error)
            data["status"] = "exception"
        else:
            data["status"] = "success"

        result.append(data)

    print(f"{i}/{all_test_files}")

    return result


def run_test_loading():
    """Run loading of all test Aspect models."""
    report = load_test_models()

    base_path = Path(__file__).parent.absolute()
    with open(join(base_path, "loading_models_test_report.csv"), "w", newline="") as csvfile:
        fieldnames = ["folder_name", "file_name", "status", "error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in report:
            writer.writerow(row)


if __name__ == "__main__":
    run_test_loading()
