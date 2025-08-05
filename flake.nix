{
  description = "A flake for the resume tool";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    let
      systems = [ "x86_64-linux" ];
    in
    flake-utils.lib.eachSystem systems (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pythonPackages = pkgs.python313Packages;
      in
      {
        formatter = pkgs.nixpkgs-fmt;
        packages = {
          resume = pkgs.stdenv.mkDerivation {
            pname = "resume";
            version = "0.0.0";
            src = self;
            nativeBuildInputs =
              with pythonPackages;
              [
                python
                jinja2
                dacite
              ];
          };
          default = self.packages.${system}.resume;
        };
      });
}
