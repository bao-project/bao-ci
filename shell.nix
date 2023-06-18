let
  pkgs = import <nixpkgs> {};

in
pkgs.mkShell {
  buildInputs = [
    pkgs.docutils
    pkgs.sphinx
    pkgs.python311Packages.sphinxcontrib-spelling
    pkgs.python311Packages.sphinx-tabs
    pkgs.python311Packages.pyenchant
    pkgs.python311Packages.doc8
    pkgs.enchant
    pkgs.python311Packages.sphinx-rtd-theme
  ];
  shellHook = ''
    echo ""
    echo "######################################################################"
    echo "#           Welcome to bao-project Nix shell environment!            #"
    echo "######################################################################"
  '';
}
