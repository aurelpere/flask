#!/bin/sh
trap 'exit' ERR
tar -cvf project.tar app/

echo 'uploading/copying with scp -i /Users/macbook/github/digitalocean ./project.tar kr1p@server:/tmp/project.tar'
scp -P 4444 -i /Users/macbook/github/digitalocean ./project.tar kr1p@$(cat ./terraform/ip.txt | sed 's/"//g'):/tmp/project.tar


echo 'Uploaded complete.'

echo 'ssh and building docker into server ...'
ssh -p 4444 -i /Users/macbook/github/digitalocean kr1p@$(cat ./terraform/ip.txt | sed 's/"//g') << 'ENDSSH'
    echo 'deploying zabbix'
	cd /zabbix && docker-compose up -d
	echo 'zabbix deployed'
	echo 'copying zabbix module to container'
	docker exec -it zabbixserver mkdir -p /var/lib/zabbix/modules/dockermodule
	docker cp /zabbix/zabbix_module_docker.so zabbixserver:/var/lib/zabbix/modules/dockermodule
	echo 'copied zabbix module to container done'
	echo 'extracting tar file'
    sudo rm -rf /app/* && sudo tar -xf /tmp/project.tar -C /
	echo 'tar file extracted'		
	echo 'configuring for python package fine deployment'
	sudo chown -R kr1p /app
	sudo chmod -R u=rwx /app
	export PATH="/home/kr1p/.local/lib/python3.9/site-packages:$PATH"
	echo 'configuring done'
	echo 'going into app folder'	
    cd /app
	echo 'getting rid of hidden macos files'
	sudo find . -type f -name '._*' -delete 
	echo 'hidden macos files deleted'
	echo 'running install'	
	make install
	echo 'install done'
	echo 'running format'
	yapf -ir -vv --style pep8 .
	echo 'format done'
	echo 'running lint'
	pylint app --verbose --disable=R,C -sy
	echo 'lint done'
	echo 'running test'
	make test
	echo 'test done'
	#echo 'running vulnerability check'
	#trivy fs --severity HIGH,CRITICAL --security-checks vuln / > security_check.txt
	#echo 'vuln check done'
	echo 'running docker build & run'
	make docker 
	echo 'docker built and running'		
ENDSSH
echo 'Build complete.'
echo 'removing project.tar'
rm project.tar
echo 'project.tar removed'

