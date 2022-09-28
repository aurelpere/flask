
test-vulnerability:
	echo "\nmake test-vulnerability\n" &&\
	trivy fs --severity HIGH,CRITICAL . 

test-misconfiguration:
	echo "\nmake test-misconfiguration\n" &&\
	trivy config --severity HIGH,CRITICAL .

install:
	echo "\nmake install\n" &&\
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	echo "\nmake format\n" &&\
	cd app &&\
	yapf -ir -vv --style pep8 .

yamllint:
	yamllint -c yml_lint.yml .

lint:
	echo "\nmake lint\n" &&\
	pylint app --verbose --disable=R,C -sy

testapp:
	echo "\nmake testapp\n" &&\
	cd app &&\
	 pytest -vv . --cov=. --cov-report xml:reports/coverage/coverage.xml

coverage_badge:
	echo "\nmake coverage_badge\n" &&\
	cd app &&\
	 genbadge coverage

cleaning:
	echo "\nmake cleaning\n" &&\
	cd app &&\
	 rm -rf app/reports

packerbuild:
	echo "\nmake packerbuild\n" &&\
	PVT_KEY=$$(cat ~/github/digitalocean) &&\
	PUBLIC_KEY=$$(cat ~/github/digitalocean.pub)&&\
	echo "$$PVT_KEY">packer/digitalocean &&\
	 echo "$$PUBLIC_KEY" >packer/digitalocean.pub &&\
	  cd packer &&\
	   chmod +x build.sh &&\
	    ./build.sh &&\
		rm digitalocean.pub &&\
		rm digitalocean

terraformbuild:
	echo "\nmake terraformebuild\n" &&\
	PVT_KEY=$$(cat ~/github/digitalocean) &&\
	PUBLIC_KEY=$$(cat ~/github/digitalocean.pub) &&\
	echo "$$PVT_KEY">terraform/digitalocean &&\
	 echo "$$PUBLIC_KEY" >terraform/digitalocean.pub &&\
	  cd terraform &&\
	   chmod +x create_droplet.sh &&\
	    ./create_droplet.sh &&\
	     rm digitalocean.pub &&\
	      rm digitalocean
	  
testmachine:
	echo "\nmake testmachine\n" &&\
	PVT_KEY=$$(cat ~/github/digitalocean) &&\
	echo "$$PVT_KEY">digitalocean &&\
	pytest test_infra.py --ssh-config="sshconfig" --hosts="$$(cat ./terraform/ip.txt)"&&\
	rm digitalocean
deploy:
	echo "\nmake deploy\n" &&\
	chmod +x auto_deploy.sh &&\
	./auto_deploy.sh
	date
	cat ./terraform/ip.txt

destroy:
	echo "\nmake destroy\n" &&\
	PVT_KEY=$$(cat ~/github/digitalocean) &&\
	PUBLIC_KEY=$$(cat ~/github/digitalocean.pub) &&\
	echo "$$PVT_KEY">terraform/digitalocean &&\
	 echo "$$PUBLIC_KEY" >terraform/digitalocean.pub &&\
	cd terraform &&\
	terraform destroy -auto-approve -var "do_token=${DO_PAT}" -var "pvt_key=$HOME/github/digitalocean" &&\
	rm digitalocean.pub &&\
	rm digitalocean 

build: test-vulnerability test-misconfiguration install format yamllint lint testapp packerbuild terraformbuild
buildlight: test-vulnerability test-misconfiguration install format lint testapp terraformbuild
all: build testmachine deploy

