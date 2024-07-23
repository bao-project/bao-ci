# base image
FROM ubuntu:22.04
ARG DEBIAN_FRONTEND=noninteractive

# docker image arguments
ARG AARCH64_TOOLCHAIN_LINK=https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-x86_64-aarch64-none-elf.tar.xz
ARG AARCH32_TOOLCHAIN_LINK=https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-x86_64-arm-none-eabi.tar.xz
ARG RISCV_TOOLCHAIN_LINK=https://github.com/bao-project/bao-riscv-toolchain/releases/download/gc891d8dc23e/riscv64-unknown-elf-13.2.0-ubuntu-22.04.tar.gz
ARG ASMFMT_LINK=https://github.com/klauspost/asmfmt/releases/download/v1.3.2/asmfmt-Linux_x86_64_1.3.2.tar.gz
ARG CLANG_VERSION=18
# use this repo temporarily while the patches for misra fps are not in a new official version
ARG CPPCHECK_REPO=https://github.com/danmar/cppcheck.git
ARG CPPCHECK_VERSION=2.9

# Install base dependencies
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
        nodejs \
        npm \
        enchant-2 \
        software-properties-common \
        ninja-build \
        pkg-config \
        libglib2.0-dev \
        libpixman-1-dev \
        libslirp-dev \
        bison \
        flex \
        tree \
        vim \
        nano \
        device-tree-compiler \
        gawk

# Install python packages
RUN pip3 install \
        gitlint \
        license-expression \
        pyenchant \
        sphinxcontrib-spelling \
        sphinx-rtd-theme \
        sphinx-tabs \
        doc8 \
        psutil \
        pyserial \
        pydevicetree \
        doorstop \
        pyspellchecker \
        ROPgadget \
        capstone \
        GitPython

# Install javascript packages
RUN npm install -g cspell@latest

# Install static analyzers
# clang-format and clang-tidy
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - && \
    add-apt-repository "deb http://apt.llvm.org/jammy/ llvm-toolchain-jammy-$CLANG_VERSION main" && \
    apt-get update && apt-get install -y \
        clang-format-$CLANG_VERSION \
        clang-tidy-$CLANG_VERSION
# cppcheck
RUN mkdir /opt/cppcheck && git clone $CPPCHECK_REPO --depth 1 --branch $CPPCHECK_VERSION /opt/cppcheck && \
        make -C /opt/cppcheck FILESDIR=/usr/share/cppcheck && make -C /opt/cppcheck install FILESDIR=/usr/share/cppcheck
# asmfmt
RUN mkdir /opt/asmfmt && curl -L $ASMFMT_LINK | tar xz -C /opt/asmfmt

# Install toolchains
RUN mkdir /opt/aarch64-toolchain && curl $AARCH64_TOOLCHAIN_LINK | tar xJ -C /opt/aarch64-toolchain --strip-components=1 && \
    mkdir /opt/aarch32-toolchain && curl $AARCH32_TOOLCHAIN_LINK | tar xJ -C /opt/aarch32-toolchain --strip-components=1 && \
    mkdir /opt/riscv-toolchain && curl $RISCV_TOOLCHAIN_LINK | tar xz -C /opt/riscv-toolchain --strip-components=1

# Add generic non-root user
RUN addgroup bao && adduser -disabled-password --ingroup bao bao

# Add qemu-riscv64-virt
RUN git clone https://github.com/qemu/qemu.git /opt/qemu-riscv64-virt --depth 1 --branch v7.2.0 && \
    cd /opt/qemu-riscv64-virt/ && ./configure --target-list=riscv64-softmmu --enable-slirp && \
    make -j$(nproc) && \
    make install

# Add qemu-aarch64-virt
RUN git clone https://github.com/qemu/qemu.git /opt/qemu-aarch64-virt --depth 1 --branch v7.2.0 && \
    cd /opt/qemu-aarch64-virt && ./configure --target-list=aarch64-softmmu --enable-slirp && \
    make -j$(nproc) && \
    make install

# setup environment
ENV PATH=$PATH:/opt/aarch64-toolchain/bin
ENV PATH=$PATH:/opt/aarch32-toolchain/bin
ENV PATH=$PATH:/opt/riscv-toolchain/bin
ENV PATH=$PATH:/opt/cppcheck
ENV PATH=$PATH:/opt/asmfmt

# default startup command
CMD /bin/bash
