#!/bin/sh

#export DO_PAT="your_personal_access_token" for token
#export TF_LOG=1 for logs
#yamllint cloud-config.yml
trap 'exit' ERR
terraform init
terraform plan -var "do_token=${DO_PAT}" 
terraform apply -auto-approve -var "do_token=${DO_PAT}" 
#terraform output droplet_ip_address > ip
#terraform destroy -auto-approve -var "do_token=${DO_PAT}" -var "pvt_key=$HOME/github/digitalocean"