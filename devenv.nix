{ pkgs, lib, config, inputs, ... }:

{
  packages = [ 
    pkgs.git
    pkgs.insomnia
    pkgs.kind
    pkgs.kubectl
    pkgs.kubectl-neat
    pkgs.kubernetes-helm
    pkgs.helmfile
    pkgs.kubeseal
  ];

  languages.nix.enable = true;
  languages.python.enable = true;
  languages.python.directory = "./restapi-flask";
  languages.python.venv.enable = true;
  languages.python.venv.requirements = ./restapi-flask/requirements.txt;

  languages.ansible.enable = true;

  scripts.k.exec = ''kubectl "$@"'';

  pre-commit.hooks.black.enable = true;
}
