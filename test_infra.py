#!/usr/bin/python3
# coding: utf-8
"""
this is test_infra.py
"""
import os
import os.path
import subprocess
from tzlocal import get_localzone


#def test_timezone():
#    result = get_localzone()
#    assert result._key == 'Europe/Paris'


def test_journald_file(host):
    journalctl = host.file("/etc/systemd/journald.conf")
    assert journalctl.contains("Storage=persistent")
    assert journalctl.contains("SystemMaxUse=100M")

def test_journalctl_output(host):
    output = host.run("journalctl -xe --no-pager").stdout
    assert 'No journal files were found' not in output

def test_journalctl_running_and_enabled(host):
    journalctl = host.service("systemd-journald")
    assert journalctl.is_running
    assert journalctl.is_enabled

def test_user_exists(host):
    assert host.user("kr1p").exists

def test_docker_sudo_zabbix_group_exist(host):
    assert host.group("sudo").exists
    assert host.group("docker").exists
    assert host.group("zabbix").exists

def test_user_belongs_to_groups(host):
    assert 'sudo' in host.user("kr1p").groups 
    assert 'docker' in host.user("kr1p").groups 
    assert 'zabbix' in host.user("kr1p").groups 

def test_sudoers(host):
    with host.sudo():
        sudoers = host.file("/etc/sudoers")
        assert sudoers.contains("%sudo ALL=(ALL) NOPASSWD: ALL")

def test_packages_installed(host):
    assert host.package("acl").is_installed
    assert host.package("curl").is_installed
    assert host.package("ufw").is_installed
    assert host.package("docker-ce").is_installed
    assert host.package("docker-ce-cli").is_installed
    assert host.package("docker-compose").is_installed
    assert host.package("rsync").is_installed
    assert host.package("apt-transport-https").is_installed
    assert host.package("ca-certificates").is_installed
    assert host.package("gnupg2").is_installed
    assert host.package("software-properties-common").is_installed
    assert host.package("python3").is_installed
    assert host.package("python3-pip").is_installed
    assert host.package("virtualenv").is_installed
    assert host.package("python3-setuptools").is_installed
    assert host.package("trivy").is_installed
    assert host.pip_package("pytest-testinfra").is_installed
    #assert host.package("zabbix-agent2").is_installed

def test_package_last_version(host):
    with host.sudo():
        outstring=host.run("apt list –upgradable").stdout
        assert 'acl' not in outstring
        assert 'curl' not in outstring
        assert 'nano' not in outstring
        assert 'ufw' not in outstring
        assert 'docker-ce' not in outstring
        assert 'docker-ce-cli' not in outstring
        assert 'docker-compose' not in outstring
        assert 'ufw' not in outstring
        assert 'rsync' not in outstring
        assert 'apt-transport-https' not in outstring
        assert 'ca-certificates' not in outstring
        assert 'gnupg2' not in outstring
        assert 'software-properties-common' not in outstring
        assert 'python3' not in outstring
        assert 'python3-pip' not in outstring
        assert 'virtualenv' not in outstring
        assert 'python3-setuptools' not in outstring
        assert 'trivy' not in outstring
        #assert 'zabbix-agent2' not in outstring


#def test_check_dist_upgrade():
#    print(1)
#   /var/log/dist-upgrade

def test_dockersock(host):
    cmd=host.run("test -r /var/run/docker.sock")
    assert cmd.rc==0
    cmd = host.run("test -w /var/run/docker.sock")
    assert cmd.rc == 0

def test_dockeractive(host):
    docker = host.service("docker")
    assert docker.is_running
    assert docker.is_enabled

#def test_zabbix(host):
#    zabbix = host.service("zabbix-agent2")
#    assert zabbix.is_running
#    assert zabbix.is_enabled

def test_containerdenabled(host):
    containerd = host.service("containerd")
    assert containerd.is_running
    assert containerd.is_enabled

def test_swapfile(host):
    assert host.file("/swapfile").mode == 0o600

def test_fstab(host):
    fstab = host.file("/etc/fstab")
    assert fstab.contains('/swapfile none swap sw 0 0')

def test_swapon(host):
    with host.sudo():
        out=host.check_output("swapon --show")
        assert "2G" in out

def test_sysctl(host):
    sysctlconf = host.file("/etc/sysctl.conf")
    assert sysctlconf.contains('vm.swappiness=50')
    assert sysctlconf.contains('vm.vfs_cache_pressure=50')
    assert host.sysctl("vm.swappiness")==50
    assert host.sysctl("vm.vfs_cache_pressure")==50

def test_swappiness(host):
    swappiness = host.file("/proc/sys/vm/swappiness")
    assert swappiness.contains("50")
    
def test_vmscachepressure(host):
    vms = host.file("/proc/sys/vm/vfs_cache_pressure")
    assert vms.contains("50")

def test_sshdconfig(host):
    sshdconfig = host.file("/etc/ssh/sshd_config")
    assert sshdconfig.contains('Port 4444') 
    assert sshdconfig.contains('Protocol 2')
    assert sshdconfig.contains('HostKey /etc/ssh/ssh_host_rsa_key')
    assert sshdconfig.contains('HostKey /etc/ssh/ssh_host_dsa_key')
    assert sshdconfig.contains('HostKey /etc/ssh/ssh_host_ecdsa_key')
    assert sshdconfig.contains('HostKey /etc/ssh/ssh_host_ed25519_key')
    assert sshdconfig.contains('UsePrivilegeSeparation yes')
    assert sshdconfig.contains('KeyRegenerationInterval 3600')
    assert sshdconfig.contains('ServerKeyBits 1024')
    assert sshdconfig.contains('SyslogFacility AUTH')
    assert sshdconfig.contains('LogLevel INFO')
    assert sshdconfig.contains('LoginGraceTime 120')
    assert sshdconfig.contains('PermitRootLogin no')
    assert sshdconfig.contains('StrictModes yes')
    assert sshdconfig.contains('RSAAuthentication yes')
    assert sshdconfig.contains('PubkeyAuthentication yes')
    assert sshdconfig.contains('IgnoreRhosts yes')
    assert sshdconfig.contains('RhostsRSAAuthentication no')
    assert sshdconfig.contains('HostbasedAuthentication no')
    assert sshdconfig.contains('PermitEmptyPasswords no')
    assert sshdconfig.contains('ChallengeResponseAuthentication no')
    assert sshdconfig.contains('X11Forwarding yes')
    assert sshdconfig.contains('X11DisplayOffset 10')
    assert sshdconfig.contains('PrintMotd no')
    assert sshdconfig.contains('TCPKeepAlive yes')
    assert sshdconfig.contains('PrintLastLog yes')
    assert sshdconfig.contains('AcceptEnv LANG LC_*')
    assert sshdconfig.contains('Subsystem sftp /usr/lib/openssh/sftp-server')
    assert sshdconfig.contains('UsePAM yes')
    assert sshdconfig.contains('AllowUsers kr1p')
    assert sshdconfig.contains('PasswordAuthentication no')

def test_ufw(host):
    ufw = host.service("ufw")
    assert ufw.is_running
    assert ufw.is_enabled

def test_ufwports(host):
    with host.sudo():
        out=host.check_output("ufw status")
        assert '4000:4010/tcp              ALLOW       Anywhere' in out
        assert '4000:4010/udp              ALLOW       Anywhere' in out
        assert '4444                       ALLOW       Anywhere' in out
        assert '80                         ALLOW       Anywhere' in out
        assert '443                        ALLOW       Anywhere' in out
        assert '10051                      ALLOW       Anywhere' in out
        assert '10050                      ALLOW       Anywhere' in out


