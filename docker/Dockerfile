# base image
FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive

# docker image arguments
ARG AARCH64_TOOLCHAIN_LINK=https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu/12.3.rel1/binrel/arm-gnu-toolchain-12.3.rel1-x86_64-aarch64-none-elf.tar.xz
ARG RISCV_TOOLCHAIN_LINK=https://static.dev.sifive.com/dev-tools/freedom-tools/v2020.12/riscv64-unknown-elf-toolchain-10.2.0-2020.12.8-x86_64-linux-ubuntu14.tar.gz
ARG ASMFMT_LINK=https://github.com/klauspost/asmfmt/releases/download/v1.3.2/asmfmt-Linux_x86_64_1.3.2.tar.gz
ARG CLANG_VERSION=14
# use this repo temporarily while the patches for misra fps are not in a new official version
ARG CPPCHECK_REPO=https://github.com/danmar/cppcheck.git
ARG CPPCHECK_VERSION=2.9

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
        nodejs \
        npm \
        enchant-2 && \
    pip3 install gitlint && \
    pip3 install license-expression && \
    pip3 install pyenchant && \
    pip3 install sphinxcontrib-spelling && \
    pip3 install sphinx-rtd-theme && \
    pip3 install sphinx-tabs && \
    pip3 install doc8 && \
    pip3 install psutil && \
    pip3 install pyserial && \
    pip3 install pydevicetree && \
    pip3 install doorstop && \
    pip3 install pyspellchecker && \
    pip3 install ROPgadget && \
    pip3 install capstone && \
    pip3 install GitPython && \
    npm install -g cspell@latest && \
    mkdir /opt/cppcheck && git clone $CPPCHECK_REPO --depth 1 --branch $CPPCHECK_VERSION /opt/cppcheck && make -C /opt/cppcheck FILESDIR=/usr/share/cppcheck && make -C /opt/cppcheck install FILESDIR=/usr/share/cppcheck  && \
    mkdir /opt/aarch64-toolchain && curl $AARCH64_TOOLCHAIN_LINK | tar xJ -C /opt/aarch64-toolchain --strip-components=1 && \
    mkdir /opt/riscv-toolchain && curl $RISCV_TOOLCHAIN_LINK | tar xz -C /opt/riscv-toolchain --strip-components=1 && \
    mkdir /opt/asmfmt && curl -L $ASMFMT_LINK | tar xz -C /opt/asmfmt

# Add generic non-root user
RUN addgroup bao && adduser -disabled-password --ingroup bao bao

# setup environment
ENV PATH=$PATH:/opt/aarch64-toolchain/bin
ENV PATH=$PATH:/opt/riscv-toolchain/bin
ENV PATH=$PATH:/opt/cppcheck
ENV PATH=$PATH:/opt/asmfmt

# default startup command
CMD /bin/bash
