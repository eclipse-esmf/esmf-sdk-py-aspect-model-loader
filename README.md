# ESMF SDK Python Aspect Model loader

## Table of Contents

- [Introduction](#introduction)
- [Getting help](#getting-help)
- [Getting Started](#getting-started)
- [SDK Structure](#sdk-structure)
- [Python Core Components](#python-core-components)
    - [esmf-aspect-meta-model-python](#esmf-aspect-meta-model-python)
- [Version Handling](#version-handling)
    - [SAMM Versioning](#samm-versioning)
    - [API Versioning](#api-versioning)
- [About](#about)
    - [Building](#building)
    - [Contributors](#contributors)
    - [Contribution Guidelines](#contribution-guidelines)
    - [3rd Party Licenses](#3rd-party-licenses)
    - [Documentation](#documentation)
    - [License](#license)

## Introduction

The ESMF SDK Python Aspect Model loader contains artifacts and resources for all parties that intent to use, extend or
integrate with the Semantic Aspect Meta Model, e.g., Solution Developers,
Domain Experts or OEMs.

At its core are components which help to work with the Semantic Aspect Meta Model (SAMM).

This repository contains a detailed developer documentation written in AsciiDoc. The source files (AsciiDoc) are
located [here](documentation/python-sdk-guide)
and are built using
[Antora](https://antora.org/) which generates the documentation as HTML files.

## Getting help

Are you having trouble with ESMF SDK Python? We want to help!

* Check the [developer documentation](https://eclipse-esmf.github.io)
* Having issues with the ESMF SDK Python? Open
  a [GitHub issue](https://github.com/eclipse-esmf/esmf-sdk-py-aspect-model-loader/issues).

## Getting Started

This document provides an overall overview of the SDK and the concepts applied throughout it. Detailed documentation and
concepts for each component can be found in the respective subfolders or subrepositories.

## SDK Structure

To ease navigation through the SDK and its components, the following structure is employed:

```
esmf-sdk-py-aspect-model-loader
 │
 ├─── core                                      # e.g. meta model implementation etc.
 │     ├─── esmf-aspect-meta-model-python
 │     ├─── ...
 └─── samples                                   # sample projects to get you started quickly
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

The aspect meta model loader work with the SAMM versions specified in the [download_samm_release.py](core/esmf-aspect-meta-model-python/esmf_aspect_meta_model_python//samm_aspect_meta_model/download_samm_release.py). This version will be used for deployment.

As SAMM evolves over time, the Aspect Meta Model Loader should also adapt and evolve accordingly.
Due to this fact it is important to understand the versioning concept that is applied to the SAMM,
APIs and SDK components that are derived from them.

In case of a prerelease there will be a postfix added and it will be released under Github.
The way to access the artifact is described
in [Github-Installing a package](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-apache-maven-registry#installing-a-package)

### SAMM Versioning

For the SAMM, semantic versioning (`major.minor.micro`) is applied with the following rules:

* A breaking change increases the `major` part
* Backwards compatible new features increase the `minor` part
* Changes to existing features or bug fixes increase the `micro` part

A new SAMM version always comprises new releases of the aspect meta model loader that depend on the SAMM, 
and new releases of aspect meta model loader may be crafted that are built on the existing SAMM version.

## About

### Building

The Python SDK is built using [python-poetry](https://python-poetry.org/). Each SDK component is a poetry package. In
order to e.g. build a package or run the tests for a package navigate to the packages root directory.

*install dependencies*

`poetry install`

*build package*

`poetry build`

*run tests*

`poetry run pytest`

### Contributors

... and you? Feel free to add [yourself](AUTHORS.md) to this list when issuing your PR!

### Contribution Guidelines

We highly appreciate any [contributions](CONTRIBUTING.md)! Feel free to issue a PR at any time.

### 3rd Party Licenses

The following 3rd party libraries are used within the SDK. Further dependencies should only be included when strictly
necessary. Especially for consumer facing components dependencies should be kept at an absolute minimum to avoid
introducing too many transitive dependencies downstream.

| Name                                  | License                              | Type                   |
|---------------------------------------|--------------------------------------|------------------------|
| python-poetry/poetry                  | MIT License (MIT)                    | Dependency Management  |
| zipfile37                             | Python Software Foundation License   | Dependency             |
| rdflib                                | [LICENSE AGREEMENT FOR RDFLIB](https://github.com/RDFLib/rdflib/blob/master/LICENSE)     | Dependency             |
| requests                              | Apache Software License (Apache 2.0) | Dependency             |
| types-requests                        | Apache Software License (Apache 2.0) | Development dependency |
| pytest-dev/pytest                     | MIT License (MIT)                    | Development dependency |
| python/mypy                           | MIT License (MIT)                    | Development dependency |
| psf/black                             | MIT License (MIT)                    | Development dependency |

### Documentation

Further documentation and howto's are provided in the
official [Python SDK User Documentation](https://eclipse-esmf.github.io/python-sdk-guide/index.html)

### License

SPDX-License-Identifier: MPL-2.0

This program and the accompanying materials are made available under the terms of the
[Mozilla Public License, v. 2.0](LICENSE).

The [Notice file](NOTICE.md) details contained third party materials.
