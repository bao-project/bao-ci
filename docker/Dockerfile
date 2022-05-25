# base image
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# docker image arguments
ARG AARCH64_TOOLCHAIN_LINK=https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu/11.2-2022.02/binrel/gcc-arm-11.2-2022.02-x86_64-aarch64-none-elf.tar.xz
ARG RISCV_TOOLCHAIN_LINK=https://static.dev.sifive.com/dev-tools/freedom-tools/v2020.12/riscv64-unknown-elf-toolchain-10.2.0-2020.12.8-x86_64-linux-ubuntu14.tar.gz
ARG CLANG_VERSION=12
# use this repo temporarily while the patches for misra fps are not in a new official version
ARG CPPCHECK_REPO=https://github.com/josecm/cppcheck.git

# install dependencies
RUN apt-get update && apt-get install -y \
        git \
        curl \
        wget \
        xz-utils \
        build-essential \
        gcc-multilib \
        python3 \
        python3-pip \
        yamllint \
        pylint \
        clang-format-$CLANG_VERSION \
        clang-tidy-$CLANG_VERSION \
        nodejs npm && \
    pip3 install gitlint && \
    pip3 install sphinxcontrib-spelling && \
    pip3 install doc8 && \
    npm install -g cspell@latest && \
    mkdir /opt/cppcheck && git clone $CPPCHECK_REPO --depth 1 /opt/cppcheck && make -C /opt/cppcheck FILESDIR=/usr/share/cppcheck && make -C /opt/cppcheck install FILESDIR=/usr/share/cppcheck  && \
    mkdir /opt/aarch64-toolchain && curl $AARCH64_TOOLCHAIN_LINK | tar xJ -C /opt/aarch64-toolchain --strip-components=1 && \
    mkdir /opt/riscv-toolchain && curl $RISCV_TOOLCHAIN_LINK | tar xz -C /opt/riscv-toolchain --strip-components=1

# Add generic non-root user
RUN addgroup bao && adduser -disabled-password --ingroup bao bao

# setup environment
ENV PATH=$PATH:/opt/aarch64-toolchain/bin
ENV PATH=$PATH:/opt/riscv-toolchain/bin
ENV PATH=$PATH:/opt/cppcheck

# default startup command
CMD /bin/bash
