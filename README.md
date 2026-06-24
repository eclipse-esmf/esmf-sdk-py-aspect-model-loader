# ESMF SDK Python Aspect Model Loader

## Table of Contents

- [Introduction](#introduction)
- [Getting help](#getting-help)
- [Getting Started](#getting-started)
- [SDK Structure](#sdk-structure)
- [Python Core Components](#python-core-components)
    - [esmf-aspect-meta-model-python](#esmf-aspect-meta-model-python)
- [Version Handling](#version-handling)
    - [SAMM Versioning](#samm-versioning)
- [About](#about)
    - [Building](#building)
    - [Contributors](#contributors)
    - [Contribution Guidelines](#contribution-guidelines)
    - [3rd Party Licenses](#3rd-party-licenses)
    - [Documentation](#documentation)
    - [License](#license)

## Introduction

The ESMF SDK Python Aspect Model Loader contains artifacts and resources for all parties that intent to use, extend or
integrate with the Semantic Aspect Meta Model, e.g., Solution Developers, Domain Experts or OEMs.

At its core are components which help to work with the Semantic Aspect Meta Model (SAMM).

This repository contains a detailed developer documentation written in AsciiDoc. The source files (AsciiDoc) are 
[python-sdk-guide](documentation/python-sdk-guide) and are built using [Antora](https://antora.org/) 
which generates the documentation as HTML files.

## Getting help

Are you having trouble with ESMF SDK Python Aspect Model Loader? We want to help!

* Check the [developer documentation](https://eclipse-esmf.github.io)
* Check the SAMM [specification](https://eclipse-esmf.github.io/samm-specification/snapshot/index.html)
* Having issues with the ESMF SDK Python Aspect Model Loader? Open a [GitHub issue](https://github.com/eclipse-esmf/esmf-sdk-py-aspect-model-loader/issues).

## Getting Started

This document provides an overall overview of the SDK and the concepts applied throughout it. Detailed documentation and
concepts for each component can be found in the respective subfolders or sub-repositories.

## SDK Structure

To ease navigation through the SDK and its components, the following structure is employed:

```
esmf-sdk-py-aspect-model-loader
 │
 ├─── core                                      # e.g. meta model implementation etc.
 │     ├─── esmf-aspect-meta-model-python
 │     ├─── ...
```

## Python Core Components

The Python core components are those to be consumed by developers that aim to build applications or tools dealing with
SAMM.

### esmf-aspect-meta-model-python

Contains the Python implementation of the SAMM.

An aspect meta model can be primarily used dynamically instantiate an Aspect Model. This is done by tooling and
applications that don't have any a-prior knowledge except for the aspect model file/URN and also don't or can't use
generated source code artifacts. Any form of source code generator will use the meta model this way.

## Version Handling

The aspect meta model loader work with the SAMM versions specified in the [download_samm_release.py](core/esmf-aspect-meta-model-python/scripts/samm/download_samm_release.py). 
This version will be used for deployment.

As SAMM evolves over time, the Aspect Meta Model Loader should also adapt and evolve accordingly.
Due to this fact it is important to understand the versioning concept that is applied to the SAMM,
APIs and SDK components that are derived from them.

In case of a prerelease a PEP 440 suffix is added to the version (e.g. `2.3.0rc1`) and the package is
published to PyPI as a pre-release. Install a specific (pre-)release with
`pip install esmf-aspect-model-loader==<version>` or `uv add esmf-aspect-model-loader==<version>`.
Released artifacts are also attached to the corresponding [GitHub release](https://github.com/eclipse-esmf/esmf-sdk-py-aspect-model-loader/releases).

### SAMM Versioning

For the SAMM, semantic versioning (`major.minor.micro`) is applied with the following rules:

* A breaking change increases the `major` part
* Backwards compatible new features increase the `minor` part
* Changes to existing features or bug fixes increase the `micro` part

A new SAMM version always comprises new releases of the aspect meta model loader that depend on the SAMM, 
and new releases of aspect meta model loader may be crafted that are built on the existing SAMM version.

## About

### Building

The Python SDK is built using [uv](https://docs.astral.sh/uv/). Each SDK component is a uv project. In
order to e.g. build a package or run the tests for a package navigate to the packages root directory.

*install dependencies*

`uv sync`

*build package*

`uv build`

*run all checks: tests and code style*

`uv run tox`

*run tests*

`uv run tox -e py310`

*run code style*

`uv run tox -e pep8`

### Contributors

... and you? Feel free to add yourself to the [`authors` list in `pyproject.toml`](core/esmf-aspect-meta-model-python/pyproject.toml) when issuing your PR!

### Contribution Guidelines

We highly appreciate any [contributions](CONTRIBUTING.md)! Feel free to issue a PR at any time.

### 3rd Party Licenses

The following 3rd party libraries are used within the SDK. Further dependencies should only be included when strictly
necessary. Especially for consumer facing components dependencies should be kept at an absolute minimum to avoid
introducing too many transitive dependencies downstream.

| Name                  | License                              | Type                   |
|-----------------------|--------------------------------------|------------------------|
| astral-sh/uv          | Apache Software License (Apache 2.0) / MIT License (MIT) | Dependency Management  |
| rdflib                | [LICENSE AGREEMENT FOR RDFLIB](https://github.com/RDFLib/rdflib/blob/master/LICENSE)     | Dependency             |
| requests              | Apache Software License (Apache 2.0) | Dependency             |
| psf/black             | MIT License (MIT)                    | Development dependency |
| nedbat/coverage       | Apache Software License (Apache 2.0) | Development dependency |
| isort                 | MIT License (MIT)                    | Development dependency |
| python/mypy           | MIT License (MIT)                    | Development dependency |
| pytest                | MIT License (MIT)                    | Development dependency |
| pytest-dev/pytest-cov | MIT License (MIT)                    | Development dependency |
| pytest-sugar          | BSD License (BSD)                    | Development dependency |
| tox                   | MIT License (MIT)                    | Development dependency |
| tox-uv                | MIT License (MIT)                    | Development dependency |
| types-requests        | Apache Software License (Apache 2.0) | Development dependency |

### Documentation

Further documentation and howto's are provided in the
official [Python SDK User Documentation](https://eclipse-esmf.github.io/python-sdk-guide/index.html)

### License

SPDX-License-Identifier: MPL-2.0

This program and the accompanying materials are made available under the terms of the
[Mozilla Public License, v. 2.0](LICENSE).

The [Notice file](NOTICE.md) details contained third party materials.
