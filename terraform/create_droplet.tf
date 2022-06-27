data "digitalocean_droplet_snapshot" "packer-snapshot" {
  name_regex  = "^packer"
  most_recent = true
}

resource "digitalocean_droplet" "tf-server-name" {
  region="ams3"
  size="s-1vcpu-1gb"
  image=data.digitalocean_droplet_snapshot.packer-snapshot.id
  name="do-server-name"
  backups=true
  ipv6=false
  monitoring=true
  ssh_keys = [data.digitalocean_ssh_key.sshkey_5_mai_22.id]
  
  connection {
    host = self.ipv4_address
    user = "kr1p"
    type = "ssh"
    private_key = file("digitalocean")
    timeout = "2m"
	port="4444"
  }
  
  provisioner "remote-exec" {
    inline = [
      "echo test",
    ]
  }
  
  }
resource "digitalocean_project" "tf-project-name" {
    name        = "do-project-name"
    description = "Description"
    purpose     = "Description purposes"
    environment = "Development"
    resources   = [digitalocean_droplet.tf-server-name.urn]
  }


output "droplet_ip_address" {
  value = digitalocean_droplet.tf-server-name.ipv4_address
}

resource "local_file" "ip" {
    content  = digitalocean_droplet.tf-server-name.ipv4_address
    filename = "ip.txt"
}