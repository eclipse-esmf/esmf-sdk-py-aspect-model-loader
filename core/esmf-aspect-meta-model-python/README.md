# Aspect Meta Model

The `esmf-aspect-meta-model-python` package provides the Python implementation for the SAMM Aspect Meta Model, or SAMM.
Each Meta Model element and each Characteristic class is represented by an interface with a corresponding
implementation.

## Usage

An Aspect of the Meta Model can be instantiated as follows using the provided `AspectInstantiator`.

```
aspect_loader = AspectLoader()
aspect = aspect_loader.load_aspect_model("path/to/turtle.ttl");
```

or

```
aspect_loader = AspectLoader()
aspect = aspect_loader.load_aspect_model_from_multiple_files(["list/of/paths/to/turtles.ttl"], "aspect_urn");
```

## Automatic Deployment

A [release GitHub action](https://github.com/eclipse-esmf/esmf-sdk-py-aspect-model-loader/actions/workflows/tagged_release.yml)
has been setup for the
`esmf-aspect-meta-model` component where the module will be build and checked to ensure code quality by running test
files and the [static type checker MyPy](https://github.com/python/mypy) and
the [code formatter 'Black'](https://github.com/psf/black).

## Set Up SAMM Aspect Meta Model für development

In order to download the SAMM sources, it is required to run `poetry install` once in the `esmf-aspect-meta-model-python`
module. There are two possibilities to download the SAMM files and extract the Turtle sources for the Meta Model.

### Possibility 1 (downloading a release)

The `download_samm_release` script may be executed with

```
poetry run download-samm-release
```  

It downloads a release JAR-file from GitHub and extracts the SAMM Files.
The version is specified in the python script.

Link to all Releases: https://github.com/eclipse-esmf/esmf-semantic-aspect-meta-model/releases

### Possibility 2 (downloading from the repository)

It may happen that there is no .JAR file that is up to date with the changes of the SAMM.
This script is an alternative to the `download_samm_release.py` and extracts the files from the repository
directly instead of using the newest release.

The script uses the GitHub API and downloads the files from the `main` branch. If the script is run in a
pipeline, it uses a GitHub token to authorize. If the script is run locally, the API is called without a token.
This may cause problems because unauthorized API calls are limited.

This script can be executed with

```
poetry run download-samm-branch
```

