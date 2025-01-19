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
    pkgs.terraform
    pkgs.cloud-init
  ];

  languages.nix.enable = true;
  languages.python.enable = true;
  languages.python.directory = "./restapi-flask";
  languages.python.venv.enable = true;
  languages.python.venv.requirements = ./restapi-flask/requirements.txt;

  languages.ansible.enable = true;

  scripts.k.exec = ''kubectl "$@"'';
  scripts.ta.exec = ''terraform apply -auto-approve'';
  scripts.td.exec = ''terraform destroy -auto-approve'';
  scripts.gip.exec = ''
    sudo virsh domifaddr ubuntu-qcow2 | tail -n 2 | head -n 1 | awk '{print $4}' | tr '/' '\n' | head -n 1
  '';
  scripts.dossh.exec = ''ssh ubuntu@$(gip)'';

  pre-commit.hooks.black.enable = true;
}
