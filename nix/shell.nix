# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Bao Project and Contributors. All rights reserved

# Pin the packages to a specific release to ensure 100% reproducibility
let
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/nixos-23.05.tar.gz") {};
in
pkgs.mkShell {
  buildInputs = [
    # bao-docs dependencies
    pkgs.docutils
    pkgs.sphinx
    pkgs.python311Packages.sphinxcontrib-spelling
    pkgs.python311Packages.sphinx-tabs
    pkgs.python311Packages.pyenchant
    pkgs.python311Packages.doc8
    pkgs.enchant
    pkgs.python311Packages.sphinx-rtd-theme
    # bao-ci dependencies
    pkgs.gitlint
    #TBD
    # bao-tests dependencies
    #TBD
    # bao-demos dependencies
    #TBD
    # bao-hypervisor dependencies
    #TBD
  ];
  shellHook = ''
    echo ""
    echo "######################################################################"
    echo "#           Welcome to bao-project Nix shell environment!            #"
    echo "######################################################################"
  '';
}
