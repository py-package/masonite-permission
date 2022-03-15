# Masonite Permission

<p align="center">
    <img src="https://banners.beyondco.de/Masonite Permission.png?theme=light&packageManager=pip+install&packageName=masonite-permission&pattern=topography&style=style_1&description=Associate users with roles and permissions&md=1&showWatermark=1&fontSize=100px&images=https%3A%2F%2Fgblobscdn.gitbook.com%2Fspaces%2F-L9uc-9XAlqhXkBwrLMA%2Favatar.png">
</p>

<p align="center">
  
  <img alt="GitHub Workflow Status" src="https://github.com/yubarajshrestha/masonite-permission/actions/workflows/pythonapp.yml/badge.svg">

  <img alt="PyPI" src="https://img.shields.io/pypi/v/masonite-permission">
  <img alt="issues" src="https://img.shields.io/github/issues/yubarajshrestha/masonite-permission">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python Version">
  <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/yubarajshrestha/masonite-permission">
  <img alt="License" src="https://img.shields.io/github/license/yubarajshrestha/masonite-permission">
  <a href="https://github.com/yubarajshrestha/masonite-permission/stargazers"><img alt="star" src="https://img.shields.io/github/stars/yubarajshrestha/masonite-permission" /></a>
  <img alt="downloads" src="https://img.shields.io/pypi/dm/masonite-permission?style=flat" />
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## Introduction

Associate users with roles and permissions

## Features

## Installation

```bash
pip install masonite-permission
```

## Configuration

Add PermissionProvider to your project in `config/providers.py`:

```python
# config/providers.py
# ...
from masonite_permission import PermissionProvider

# ...
PROVIDERS = [
    # ...
    # Third Party Providers
    PermissionProvider,
    # ...
]
```

Then you can publish the package resources (if needed) by doing:

```bash
python craft package:publish masonite-permission
```

## Usage

```python
""" Permission Syncing """
permissions = Permission.all()
role.sync_permissions(permissions) # sync permissions to role
role.sync_permissions([]) # remove all permissions from role

""" Attach/Detatch Permission """
permission = Permission.first()
role.attach_permission(permission) # add permission to role, ignores if permission already exists
role.detach_permission(permission) # remove permission from role, ignores if permission doesn't exist

""" Role Syncing """
roles = Role.all()
permission.sync_roles(roles) # sync roles to role
permissioin.sync_roles([]) # remove all roles from role

""" Attach/Detatch Role """
role = Role.first()
permission.attach_role(role) # add role to permission, ignores if role already exists
permission.detach_role(role) # remove role from permission, ignores if role doesn't exist
```

## Contributing

Please read the [Contributing Documentation](CONTRIBUTING.md) here.

## Maintainers

- [Yubaraj Shrestha](https://www.github.com/yubarajshrestha)

## License

Masonite Permission is open-sourced software licensed under the [MIT license](LICENSE).
