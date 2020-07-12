{
  pkgs ? import <nixpkgs> {}
}:

let
  customPython = pkgs.python3.withPackages
    (ps: [
      ps.python-telegram-bot
      ps.pytest
    ]);
in

pkgs.mkShell {
  buildInputs = [
    customPython
  ];
}
