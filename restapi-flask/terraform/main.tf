terraform {
 required_version = ">= 0.13"
  required_providers {
    libvirt = {
      source  = "dmacvicar/libvirt"
    }
  }
}

provider "libvirt" {
  uri = "qemu:///system"
}

resource "libvirt_pool" "ubuntu" {
  name = "ubuntu"
  type = "dir"
  path = "/home/igor/terraform-provider-libvirt-pool-ubuntu"
}

locals {
  domains = [
    { name = "ubuntu-qcow2-1" },
    { name = "ubuntu-qcow2-2" },
    { name = "ubuntu-qcow2-3" },
  ]
}


resource "libvirt_volume" "ubuntu-qcow2" {
  count = length(local.domains)
  name   = "${local.domains[count.index].name}"

  pool   = libvirt_pool.ubuntu.name
  source = "https://cloud-images.ubuntu.com/releases/24.04/release/ubuntu-24.04-server-cloudimg-amd64.img"
  format = "qcow2"
}

data "template_file" "user_data" {
  template = file("${path.module}/cloud_init.cfg")
}

data "template_file" "network_config" {
  template = file("${path.module}/network_config.cfg")
}

resource "libvirt_cloudinit_disk" "commoninit" {
  name           = "commoninit.iso"
  user_data      = data.template_file.user_data.rendered
  network_config = data.template_file.network_config.rendered
  pool           = libvirt_pool.ubuntu.name
}

resource "libvirt_domain" "domain-ubuntu" {
  count = length(local.domains)
  name   = "${local.domains[count.index].name}"

  memory = "512"
  vcpu   = 1

  cloudinit = libvirt_cloudinit_disk.commoninit.id

  network_interface {
    addresses = [ "192.168.124.7${count.index}" ]
    network_name = "default"
  }

  console {
    type        = "pty"
    target_port = "0"
    target_type = "serial"
  }

  console {
    type        = "pty"
    target_type = "virtio"
    target_port = "1"
  }

  disk {
    volume_id = libvirt_volume.ubuntu-qcow2[count.index].id
  }

  graphics {
    type        = "spice"
    listen_type = "address"
    autoport    = true
  }
}
