# kali-setup

Ansible Scripts to build out Kali machines.

# Pre-requisites
1. A kali machine up and running
2. Update ssh.cfg with the kali IP address

**Note**: Include your SSH private Key(s) into the Keys directory (optional)

# How to run this Ansible Build

When using your kali password:

```
ansible-playbook -i inventory/kali_hosts  playbooks/master_playbook.yml --ask-pass --ask-become-pass

ansible-playbook -i inventory/kali_hosts  playbooks/master_playbook.yml --ask-pass --ask-become-pass --tags sectools_binaries
```
When using SSH keys:

```
ansible-playbook -i inventory/kali_hosts  playbooks/master_playbook.yml
```
## Kali Architecture supported
The variable 'arch' is being used to deal with the following kali architecture:
- ARM64
- x64

If you want to add new tools or tasks to this playbook, please keep in mind that you may need to use the 'arch' variable.
Eg.

```
binaries:
    - {name: 'postman.tar.gz', url: 'https://dl.pstmn.io/download/latest/linux64', compressed: 'yes', arch: 'x64', symbolic: 'yes', sym_src: 'Postman/Postman', sym_dest: '{{ local_bin }}/postman'}
    - {name: 'postman.tar.gz', url: 'https://dl.pstmn.io/download/latest/linux_arm64', compressed: 'yes', arch: 'arm64', symbolic: 'yes', sym_src: 'Postman/Postman', sym_dest: '{{ local_bin }}/postman'}
  
```
## Desktop supported
Desktop tools for Kali is also supported by this playbook. Just enable it in group_vars/kali.yml

```
desktop_enabled: yes
```

*If you kali is running in AWS and you get an error when installing common packages, comment this line:*
```
# - linux-headers-{{ ansible_kernel }}
```

# Acknowledgements

The development of te playbook was inspired by the following authors and projects:

- [@hackedbyagirl -  Offensive Kali Ansible Playbook ](https://github.com/hackedbyagirl/offensive-kali-ansible)
- [@denis6400 - kali-setup](https://github.com/dennis6400/kali-setup)
