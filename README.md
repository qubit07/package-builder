# package-builder

A small Python-based task runner that executes build and deployment steps defined in a YAML configuration file.

It allows you to automate common tasks such as:

running build commands

copying files or directories

creating archives

deploying artifacts via SSH

The goal is to provide a simple alternative to shell scripts for multi-step build and deployment workflows.

## Supported tasks:

command – run shell commands

copy – copy files or directories

tar – create .tar.gz archives

ssh – deploy files via scp

## Some tasks rely on external tools:

dotnet

npm

tar

scp
