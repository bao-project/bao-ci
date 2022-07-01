# Bao CI utilities

This repository aims at centralizing the artifacts used for continuous
integration across all other repositories in the Bao Project. Its main goal is
to provide a consistent framework for running the code quality checks and tests
both in a developer's local machine, as well in a remote CI pipeline, in a
reproducible manner. It provides two main facilities:

- A [ci.mk](ci.mk) makefile, that defines how the tools used for the checks are
  invoked;
- A [docker container](docker/Dockerfile) definition which provides a
reproducible enviroment for running the checks.

Besides these two main pillars, the repository contains a number of configuration
and template files used by the tools and CI process in general.

Although we use GitHub Actions for the remote CI pipeline, all workflow steps
are rab in the docker container by calling the rules defined in makefile.

The following checks are provided:

- gitlint: checks commit messages follow the conventional commit style
- pylint: python formatting and linting
- yamllint: yaml formatting and linting
- format: C formatting
- tidy and cppcheck: C static analysis
- misra: MISRA C checking

## Setting up CI in a repository

To make use of the facilities provided by this repository, first add it as a
submodule name *ci* in each project's top-level directory.

```bash
cd bao-project-repo
git submodule add git@github.com:bao-project/bao-ci.git ci
```

Then you should include *ci.mk* in your projects Makefile, preferably at the
very end, but it must be after your first rule definition. Before including
*ci.mk* you must define the `root_dir` variable with the of the project
top-level directory. Assuming the Makefile is located at the project's top-level
directory:

```make
root_dir:=$(realpath .)

all:

include ci/ci.mk
```

The makefile rules might also assume a number of standard predefined make
variables containing C toolchain definition such as `CPPFLAGS` or the target's
`CROSS_COMPILE` prefix.

Then you can add the CI predefined checks using Make's call syntax. For example
to run the static-analysis cppcheck tool on three C files:

```
$(call ci, cppcheck, file1.c file2.c file3.h)
```

Then you can invoke CI checks by running it as typical make target:

```
make cppcheck
```

If the checks are successful they will return 0, otherwise they'll return an
error code, as is typical of CLI tools.

Note that each instantiated check might offer one or more rules. For example,
when you instantiate the *format* rule:

```
$(call ci, format, file1.c file2.c file3.h)
```

You'll get a make target for checking if the formatting is correct and another
to apply the formatting:

```
make format-check # checks if the files are correctly formatted
make format # formats the files
```

Check [ci.mk](ci.mk) for more details on the available CI rules, its arguments
and how to invoke them.

### Global CI rule

By convention, repos using this CI infrastructure should also define a make
rule such that running `make ci` locally runs all rules necessary for that
repo, except rules related to the commits themselves such as gitlint.
For example, for a repo composed of a mix of C an Python sources:

```
ci: license pylint format-check tidy cppcheck misra
```

## Using the Docker Container

We provide a docker container with all the needed tools and dependencies for
building Bao, as well as running all the necessary CI rules, already installed.
It is used in GitHub Actions workflows to run all CI rules remotely. To use it
locally, please make sure you have [installed
docker](https://docs.docker.com/engine/install/).

We try to keep a docker hub image
[bao-project/bao:latest](https://hub.docker.com/repository/docker/baoproject/bao)
as updated as possible. Docker will automatically fetch it when you start the
container for the first time.

We provide a Makefile to ease running any command inside the container. For
example, if you want to run the format check in the container just:

```bash
make -C ci/docker format-check
```

If you prefer, you can build the container image locally by running:

```bash
make -C ci/docker build
```

## Setting up GitHub Actions

When setting up GitHub Actions' workflows for you repo, each step should make
use of the docker container to run the CI rules instantiated in that repo's
Makefile as such:

```yaml
name: Bao Project example workflow

on:
  push:
    branches: [ main ]
  pull_request:
  workflow_dispatch:

jobs:
  example-ci-step:
    runs-on: ubuntu-latest
    container: baoproject/bao:latest
    steps:
      - uses: actions/checkout@v2
        with:
          submodules: recursive
      - run: make <example-ci-check-target>
```

This repo also provides a [template for the base CI
Workflow](.github/workflows/templates/base.yml) that should be used by all C
language projects by copying it to the *.github/workflows* directory, and
adapting it to the repo's specific needs (e.g. target platform matrix). You
should settup any GitHub setting for your repository's Github Actions CI
pipeline according to the project's guidelines.
