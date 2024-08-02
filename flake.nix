{
  description = "A Nix-flake-based Python development environment packaged using poetry2nix";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { 
        inherit system;
      };
    in
    {
      devShells.default = pkgs.mkShell {
        packages = with pkgs; [ 
          python312
          poetry
          go-task
          grafana-alloy
        ] ++
        (with pkgs.python312Packages; [
          venvShellHook
        ]);
        venvDir = ".venv";
        postVenvCreation = ''
          poetry install
        '';
        env = {
          PROMETHEUS_MULTIPROC_DIR = ".prometheus";
        };
      };
    });
}
