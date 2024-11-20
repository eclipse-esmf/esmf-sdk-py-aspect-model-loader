The Aspect Model Loader as part of the Python SDK provided by the [*Eclipse Semantic Modeling Framework*](
https://projects.eclipse.org/projects/dt.esmf).

<!-- TOC -->
* [An Aspect of the Meta Model](#an-aspect-of-the-meta-model)
  * [Set Up SAMM Aspect Meta Model](#set-up-samm-aspect-meta-model)
    * [Install poetry](#install-poetry)
    * [Install project dependencies](#install-project-dependencies)
    * [Download SAMM files](#download-samm-files)
      * [Download SAMM release](#download-samm-release)
      * [Download SAMM branch](#download-samm-branch)
  * [Input data handler usage](#input-data-handler-usage)
  * [Aspect Meta Model Loader usage](#aspect-meta-model-loader-usage)
  * [Samm Units](#samm-units)
  * [SAMM CLI wrapper class](#samm-cli-wrapper-class)
* [Scripts](#scripts)
* [Automation Tasks](#automation-tasks)
  * [tox](#tox)
  * [GitHub actions](#github-actions)
    * [Check New Pull Request](#check-new-pull-request)
    * [Build release](#build-release)
<!-- TOC -->

# An Aspect of the Meta Model

The `esmf-aspect-model-loader` package provides the Python implementation for the SAMM Aspect Meta Model, or SAMM.
Each Meta Model element and each Characteristic class is represented by an interface with a corresponding
implementation.

## Set Up SAMM Aspect Meta Model

Before getting started to use the `esmf-aspect-model-loader` library you need to apply some set up actions:

Required
- [Install poetry](#install-poetry)
- [Install project dependencies](#install-project-dependencies)
- [Download SAMM files](#download-samm-files)

### Install poetry

`Poetry` used as a dependency management for the `esmf-aspect-model-loader`. Follow the next [instruction](https://python-poetry.org/docs/#installation)
 to install it.

To check the poetry version run:
```console
poetry --version
```

### Install project dependencies

Poetry provides convenient functionality for working with dependencies in the project.
To automatically download and install all the necessary libraries, just run one command:
```console
poetry install
```
It is required to run `poetry install` once in the esmf-aspect-model-loader module.

### Download SAMM files

There are two possibilities to download the SAMM files and extract the Turtle sources for the Meta Model: 
SAMM release or SAMM branch

#### Download SAMM release

This script downloads a release JAR-file from GitHub, extracts them for further usage in the Aspect Model Loader:

To run script, execute the next command.
```console
poetry run download-samm-release
```
The version of the SAMM release is specified in the python script.

Link to all Releases: [SAMM Releases](https://github.com/eclipse-esmf/esmf-semantic-aspect-meta-model/releases)

#### Download SAMM branch

The script uses the GitHub API and downloads the files from the `main` GitHub branch. 

If the script is run in a pipeline, it uses a GitHub token to authorize. If the script is run locally, 
the API is called without a token. This may cause problems because unauthorized API calls are limited.

Run the next command to download and start working with the Aspect Model Loader.
```console
poetry run download-samm-branch
```
Link to all branches: [SAMM Releases](https://github.com/eclipse-esmf/esmf-semantic-aspect-meta-model/branches)

## Input data handler usage

The InputHandler is a general-purpose class designed for loading input data into an RDF graph. 
It easily accommodates different input sources such as local files (.ttl) or direct data strings containing 
RDF formatted data.

```python
from esmf_aspect_meta_model_python.resolver.handler import InputHandler

# Instantiating the Handler
# The InputHandler requires a path or data string upon instantiation, which defines the source of RDF data
# local file
model_path = "path/to/local/file/AspectName.ttl"
handler = InputHandler(model_path)
graph, aspect_urn = handler.get_rdf_graph()

# returns a tuple containing the RDF graph and the aspect URN derived from the provided data source
```

```python
from esmf_aspect_meta_model_python.resolver.handler import InputHandler

# Alternatively, if you have RDF data in a string format, you can directly pass it as follows:
rdf_data_string = "your RDF data string here"
handler = InputHandler(rdf_data_string)
graph, aspect_urn = handler.get_rdf_graph()
```

## Aspect Meta Model Loader usage

An Aspect of the Meta Model can be loaded as follows:
```python
from esmf_aspect_meta_model_python import AspectLoader
from esmf_aspect_meta_model_python.resolver.handler import InputHandler

model_path = "absolute/path/to/turtle.ttl"
handler = InputHandler(model_path)
graph, aspect_urn = handler.get_rdf_graph()

loader = AspectLoader()
model_elements = loader.load_aspect_model(graph, aspect_urn)
aspect = model_elements[0]

# or you can provide an Aspect URN

loader = AspectLoader()
aspect_urn = "urn:samm:org.eclipse.esmf.samm:aspect.model:0.0.1#AspectName"
model_elements = loader.load_aspect_model("absolute/path/to/turtle.ttl", aspect_urn)
aspect = model_elements[0]
```

## Samm Units

SAMMUnitsGraph is a class contains functions for accessing units of measurement.
```python 
from esmf_aspect_meta_model_python.samm_meta_model import units

unit_name = "unit:volt"
units.print_description(units.get_info(unit_name))
# preferredName: volt
# commonCode: VLT
# ...
# symbol: V

# Get unit data as dictionary
volt_info = units.get_info("unit:volt")
# {'preferredName': rdflib.term.Literal('volt', lang='en'), 'commonCode': rdflib.term.Literal('VLT'), ... }

units.print_description(volt_info)
# preferredName: volt
# commonCode: VLT
# ...
# symbol: V
```

## SAMM CLI wrapper class

The SAMM CLI is a command line tool provided number of functions for working with Aspect Models.

More detailed information about SAMM CLI functionality can be found in the 
[SAMM CLI documentation](https://eclipse-esmf.github.io/esmf-developer-guide/tooling-guide/samm-cli.html).

Python Aspect Model Loader provide a wrapper class to be able to call SAMM CLI functions from the Python code.
For instance, validation of a model can be done with the following code snippet:

```python
from esmf_aspect_meta_model_python.samm_cli_functions import SammCli

samm_cli = SammCli()
model_path = "Paht_to_the_model/Model.ttl"
samm_cli.validate(model_path)
# Input model is valid
```

List of SAMMCLI functions:
- validate
- to_openapi
- to_schema
- to_json
- to_html
- to_png
- to_svg

# Scripts

The Aspect Model Loader provide scripts for downloading some additional code and data.
Provided scripts:
 - download-samm-release
 - download-samm-branch
 - download-samm-cli
 - download-test-models

All scripts run like a poetry command. The poetry is available from the folder where [pyproject.toml](pyproject.toml) 
is located.

# Automation Tasks
## tox

`tox` is used for the tests automation purpose. There are two environments with different purposes and tests can 
be running with the tox:
- pep8: static code checks (PEP8 style) with MyPy and Black
- py310: unit and integration tests

```console
# run all checks use the next command
poetry run tox

# run only pep8 checks
poetry run tox -e pep8

# run tests
poetry run tox -e py310
```

## GitHub actions

There are two actions on the GitHub repo:
- [Check New Pull Request](../../.github/workflows/push_request_check.yml)
- [Build release](../../.github/workflows/tagged_release.yml)

### Check New Pull Request
This action run after creation or updating a pull request and run all automation tests with tox command.

### Build release
Prepare and publish a new release for the `esmf-aspect-model-loader` to the PyPi: 
[esmf-aspect-model-loader](https://pypi.org/project/esmf-aspect-model-loader/.)

A list of the available releases on the GitHub: 
[Releases](https://github.com/eclipse-esmf/esmf-sdk-py-aspect-model-loader/releases). 
