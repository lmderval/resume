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
        python = pythonPackages.python;
        pythonEnv = python.withPackages (ps: with ps; [ jinja2 dacite pyyaml ]);
      in
      {
        formatter = pkgs.nixpkgs-fmt;
        packages = rec {
          resume = pkgs.stdenv.mkDerivation {
            pname = "resume";
            version = "0.0.0";
            src = self;
            nativeBuildInputs = [ pkgs.makeWrapper ];
            installPhase = ''
              runHook preInstall
              mkdir -p $out/lib/resume $out/bin
              cp -r src/{resume.py,styles,templates,utils,translations} \
                $out/lib/resume/
              makeWrapper ${pythonEnv}/bin/python $out/bin/resume \
                --add-flags "$out/lib/resume/resume.py"
              runHook postInstall
            '';
          };
          generated = pkgs.runCommand "resume-generated" { } ''
            cp -r ${resume}/lib/resume workdir
            chmod +w workdir
            (
              cd workdir
              ${pythonEnv}/bin/python resume.py \
                --path ${self}/src/resumes/resume.yaml
            )
            mkdir -p $out
            cp workdir/generated/{resume.css,resume.html} $out/
          '';
          default = self.packages.${system}.resume;
        };
      });
}
