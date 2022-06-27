terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}


variable "do_token" {
	type = string
	default=""
}
variable "pvt_key" {
	type = string
	default=""
}
variable "public_key" {
	type = string
	default= ""
}
provider "digitalocean" {
  token = var.do_token
}

data "digitalocean_ssh_key" "sshkey_5_mai_22" {
  name = "sshkey_5_mai_22"
}