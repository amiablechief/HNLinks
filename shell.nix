# shell.nix

let
# we pin to a specific nixpkgs commit for reproducibility
# last updated 2024-04-29. Check for new commits at https://status.nixos.org
  pkgs = import (fetchTarball
	"https://github.com/NixOS/nixpkgs/archive/cf8cc1201be8bc71b7cbbbdaf349b22f4f99c7ae.tar.gz") {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      # select python packages here
      python-pkgs.urllib3
      python-pkgs.feedparser
      python-pkgs.beautifulsoup4
      python-pkgs.datetime
      python-pkgs.unidecode
    ]))
  ];
}
