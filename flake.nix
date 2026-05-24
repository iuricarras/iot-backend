{
  description = "* flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        (python313.withPackages (python-pkgs: [
          python-pkgs.flask
          python-pkgs.flask-cors
          python-pkgs.firebase-admin
          python-pkgs.python-dotenv
          python-pkgs.pip
        ]))
      ];
      shellHook = ''
        export FLASK_APP=app
        export FLASK_ENV=development
        export FLASK_DEBUG=True
      '';
    };
  };
}
