This is a PlayBooks deployment of Python3.6.4 using Ansible

#### Do the following：
- Change Yum source to Ali source
- Added EPEL source
- Firewalld open port 6800
- Disable Chronyd, change to NTP (Ali NTP Server)
- Disable Selinux
- Install Python3 compilation dependent components, and compile and install Python3, the soft connection is: / usr / bin / python3

#### Instructions：
- Install Ansible（[Install Docs](http://www.ansible.com.cn/docs/intro_installation.html)）
- Generate a management key
- Deploy host IP or domain name into host
- Run copy_ssh.sh（Default root user, manually enter the password (Ctrl + C and Ctrl + V)）
- All needed Python packages, written in list form install_pip_package (/Deploy_Python3/group_vars/all)
- If you want to change the Python installation path, change: Variable python_path（/Deploy_Python3/group_vars/all）


After preparation is completed。

Run the following command in the Deploy_Python3 directory：

        ansible-playbooks -i host site.yml
        
Waiting to be completed

Done

#### Instructions for Vagrant:

cd into project directory and run `vagrant up` then `cd Deploy_Python3` and run

        ansible-playbook site.yml
