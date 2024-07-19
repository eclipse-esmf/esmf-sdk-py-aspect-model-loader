# ESMF SDK PY Aspect Model Loader Code Conventions

The following document contains a compilation of conventions and guidelines to format, 
structure and write code for the ESMF SDK PY Aspect Model Loader.

## General Conventions

Our code conventions are based on the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html), 
but detailed and adjusted for the needs of the ESMF SDK PY Aspect Model Loader.
 
## Copyright header
See [CONTRIBUTING](CONTRIBUTING.md)

## Code Recommendations

The code for this project follows the guidelines of [PEP 8](https://peps.python.org/pep-0008/).
The libraries black, flake8 and isort are also used so that the code can be checked for compliance with the PEP 8 style.

## Documentation

### Developer Documentation
Developer documentation is put into a README.md placed in the project root. This should contain documentation like:
* Checking out the source code and getting it to run/build
* Mandatory (external system) dependencies and how to set them up (e.g. databases)
* Configuration options and how to apply them
* General important concepts that are relevant to working on the project but are not directly obvious from the source code
  itself. Links to further readings and information, e.g. wiki or other external sources.

### User documentation

User documentation (this includes technical documentation on how to use an application or tool from the 
ESMF SDK PY Aspect Model Loader Code Conventions) should be on its own.

It is written in AsciiDoc, rendered with [Antora](https://antora.org) and the generated static content is
publicly hosted for direct user access.
The source files of the documentation are placed in a subfolder /documentation from the project root.
Documentation is structured so that it can be processed by Antora. This e.g. involves structuring the documentation files
according to [Antora's specification](https://docs.antora.org/antora/2.3/organize-content-files/) and organizing resources
so that Antora [can handle them](https://docs.antora.org/antora/2.3/page/resource-id/).
[AsciiDoc's syntax](https://docs.antora.org/antora/2.3/asciidoc/asciidoc/) is pretty close to Markdown, however it is
way more targeted towards writing fully fledged documents and with its multitude of backends (HTML, PDF, ...) it is a
very good source format.
Publishing is realized by means of [GitHub pages](https://docs.antora.org/antora/2.3/publish-to-github-pages/).
