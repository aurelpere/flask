#!/bin/sh
#PACKER_LOG=1
#to get key id : curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer token" "https://api.digitalocean.com/v2/account/keys" 
trap 'exit' ERR
packer validate packer.pkr.hcl
packer init .
packer build .
