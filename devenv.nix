{ pkgs, lib, config, inputs, ... }:

{
  packages = [ 
    pkgs.git
    pkgs.insomnia
    pkgs.kind
    pkgs.kubectl
    pkgs.kubectl-neat
    pkgs.kubernetes-helm
  ];

  languages.nix.enable = true;
  languages.python.enable = true;
  languages.python.directory = "./restapi-flask";
  languages.python.venv.enable = true;
  languages.python.venv.requirements = ./restapi-flask/requirements.txt;

  pre-commit.hooks.black.enable = true;
}
