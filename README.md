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

Finally, extend `User` model class with `HasRoles`.

```python
from masoniteorm.models import Model
from masoniteorm.scopes import SoftDeletesMixin
from masonite.authentication import Authenticates
from masonite_permission.models.has_roles import HasRoles

class User(Model, SoftDeletesMixin, Authenticates, HasRoles):
    """User Model."""

    __fillable__ = ["name", "email", "password"]
    __hidden__ = ["password"]
    __auth__ = "email"
```

## Usage

**Role**

Methods that can be used in role model object:

```python
""" Creating Role """
role = Role.create({
  "name": "Admin",
  "slug": "admin" # must be unique
})

""" collection can be synced """
permission_collection = Permission.all()

role.sync_permissions(permission_collection)

""" id will also work """
permission_ids = [1,2,3,4,5]
role.sync_permissions(permission_ids)

""" clear related data """
role.sync_permissions([])


""" Attach/Detatch Permission """
permission = Permission.first()
role.attach_permission(permission) # add permission to role, ignores if permission already exists
role.detach_permission(permission) # remove permission from role, ignores if permission doesn't exist

""" this can also be done """
role.attach_permission(1) # passing permission id instead of object, ignores if permission already exists
role.detatch_permission(1) # passing permission id instead of object, ignores if permission doesn't exist
```

**Permission**

Methods that can be used in permission model object:

```python
""" Creating Permission """
permission = Permission.create({
  "name": "Create Post",
  "slug": "create-post" # must be unique
})

""" collection can be synced """
roles_collection = Role.all()

permission.sync_roles(role_collection)

""" id will also work """
role_ids = [1,2,3,4,5]
permission.sync_roles(role_ids)

""" clear related data """
permissioin.sync_roles([])


""" Attach/Detatch Role """
role = Role.first()
permission.attach_role(role) # add role to permission, ignores if role already exists
permission.detach_role(role) # remove role from permission, ignores if role doesn't exist

""" this can also be done """
permission.attach_role(1) # passing role id instead of object, ignores if role already exists
permission.detatch_role(1) # passing role id instead of object, ignores if role doesn't exist
```

**User**

Methods that can be used in user model object:

```python
user = User.first()

# Add/Remove single role
role = Role.first()

user.assign_role(role) # or you can pass role id
user.remove_role(role) # or you can pass role id

# if you want to add multiple roles
roles = Role.all()

user.sync_roles(roles) # or you can also pass list of ids...

# remove all roles from user at once
user.sync_roles([])

# check if user has role
user.has_role("role-1") # returns boolean

# check if user has any of the roles
user.has_any_role(["role-1", "role-2"]) # returns boolean

# check if user has all of the roles
user.has_all_roles(["role-1", "role-2"]) # returns boolean

# check if user has permission
user.has_permission("permission-1") # returns boolean

# check if user has any of the permissions
user.has_any_permission(["permission-1", "permission-2"]) # returns boolean

# check if user has all of the permissions
user.has_all_permissions(["permission-1", "permission-2"]) # returns boolean

```

## Using in Template

**In case of Roles**
Checking if user has role.

```jinja2
{% if user.is_("admin") %}
    <p>You are an admin</p>
{% endif %}
```

Checking if user has any of the roles

```jinja2
{% if user.is_("admin|editor|truck-driver") %}
    <p>You can be either admin, editor, truck driver or all of those</p>
{% endif %}
```

Checking if user has all of the roles

```jinja2
{% if user.is_("admin,editor,truck-driver") %}
    <p>You are an admin, editor and also truck-driver</p>
{% endif %}
```

**In case of Permissions**
Checking if user can do {permission}.

```jinja2
{% if user.can_("edit-post") %}
    <p>You can edit post</p>
{% endif %}
```

Checking if user can do any one or more of the {permissions}

```jinja2
{% if user.can_("edit-post|delete-post") %}
    <p>You can either edit-post, delete-post or both.</p>
{% endif %}
```

Checking if user can do all of the {permissions}

```jinja2
{% if user.can_("edit-post,delete-post") %}
    <p>You can edit post and also delete post.</p>
{% endif %}
```

## Contributing

Please read the [Contributing Documentation](CONTRIBUTING.md) here.

## Maintainers

- [Yubaraj Shrestha](https://www.github.com/yubarajshrestha)

## License

Masonite Permission is open-sourced software licensed under the [MIT license](LICENSE).

```

```
