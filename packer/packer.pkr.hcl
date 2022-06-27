variable "do_token" {
  type    = string
  default = env("DO_PAT")
}
packer {
  required_plugins {
    digitalocean = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/digitalocean"
    }
  }
}

source "digitalocean" "flask-tutorial" {
  api_token    = var.do_token
  image        = "debian-11-x64"
  region       = "ams3"
  size         = "s-1vcpu-1gb"
  ssh_username = "root"
  monitoring = true
  snapshot_name = "packer-{{timestamp}}"
  droplet_name = "Debian-11-docker-zabbix"
  ssh_key_id = 34648169
  ssh_private_key_file = "digitalocean" 
}
 
build {
  sources = ["source.digitalocean.flask-tutorial"]

  provisioner "file" {
    source = "digitalocean.pub"
    destination = "/tmp/digitalocean.pub"
  }

  provisioner "file" {
    source = "../zabbix"
    destination = "/tmp/zabbix"
  }

  provisioner "shell" {
      inline = [
	  "mkdir -p /zabbix",
	  "cp -r /tmp/zabbix /",
	  "sleep 30", #for apt-get lock
	  "export DEBIAN_FRONTEND=\"noninteractive\"", #for debconf interactivity error
      "echo set debconf to Noninteractive", #for debconf interactivity error
      "echo 'debconf debconf/frontend select Noninteractive' | sudo debconf-set-selections", #for debconf interactivity error
	  "apt-get update -y",
	  "apt-get install -y aptitude",
	  "aptitude install ansible -y"]
  }	

  #provisioner "shell" {
  #  scripts = ["install.sh"]
  #}

  provisioner "ansible-local" {
    playbook_file = "../ansible/playbook.yml"
	extra_arguments= [ 
	  "-vvv",
	  "--extra-vars",
	  "'ansible_python_interpreter=/usr/bin/python3'"
	]
   # playbook_dir = "."
   # extra_arguments = [
   #   "-e",
   #   "'ansible_python_interpreter=/usr/bin/python3'"
   # ]
  }

}