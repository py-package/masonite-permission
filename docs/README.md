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

## Getting Started

Install the package using pip:

```bash
pip install masonite-permission
```

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

Publish the package configuration files.

```bash
python craft package:publish masonite-permission
```

This will add migrations and other `masonite-permission` related configuration to your project. Run your migrations to create the related database tables.

```bash
python craft migrate
```

Now, extend `User` model class with `HasRoles` mixin.

```python
from masoniteorm.models import Model
from masoniteorm.scopes import SoftDeletesMixin
from masonite.authentication import Authenticates
from masonite_permission.mixins import HasRoles

class User(Model, SoftDeletesMixin, Authenticates, HasRoles):
    """User Model."""

    __fillable__ = ["name", "email", "password"]
    __hidden__ = ["password"]
    __auth__ = "email"
```

## Usage

#### Working with Role

<details>
<summary style="font-weight: bolder">Creating Role</summary>

```python

""" Creating Role
    Arguments:
        name: The name of the role
        slug: The slug of the role, must be unique
"""
from masonite_permission.models import Role

role = Role.create({
    "name": "Admin",
    "slug": "admin"
})

```

</details>

<details>
<summary style="font-weight: bolder">Add permissions into roles</summary>

```python
""" Add permissions into roles
    Available Methods:
        1. sync_permissions: Syncs the permissions with the role
            arguments: Takes a list of permission ids or permission collection
        2. attach_permission: Adds a permission to a role
            arguments: Takes permission model object or permission id
        3. detach_permission: Removes a permission from the role
            arguments: Takes permission model object or permission id
"""
```

```python
""" Syncing permissions with role, adds provided permissions and removes all other permissions
    Arguments:
        permissions: Takes a list of permission ids or permission collection
"""
permission_collection = Permission.all()
permission_ids = [1, 2, 3, 4, ...]

role.sync_permissions(permission_collection)
# or
role.sync_permissions(permission_ids)
# or
role.sync_permissions([]) # clears all permissions from role
```

```python
""" Attach permission, this will add new permission into role if already not added
    Arguments:
        permission: Takes permission model object or permission id
"""
permission = Permission.first()

role.attach_permission(permission)
# or
role.attach_permission(1)
```

```python
""" Detach permission, this will remove permission from role if already added
    Arguments:
        permission: Takes permission model object or permission id
"""
permission = Permission.first()

role.detach_permission(permission)
# or
role.detach_permission(1)
```

</details>

<br/>

#### Working with Permission

<details>
<summary style="font-weight: bolder">Creating Permission</summary>

```python
""" Creating Permission
    Arguments:
        name: The name of the permission
        slug: The slug of the permission, must be unique
"""
from masonite_permission.models import Permission
permission = Permission.create({
  "name": "Create Post",
  "slug": "create-post" # must be unique
})
```

</details>

<details>
<summary style="font-weight: bold;">Add permissions into roles</summary>

```python
""" Add permissions into roles
    Available Methods:
        1. sync_roles: Syncs the roles with the permission
            arguments: Takes a list of role ids or role collection
        2. attach_role: Adds a permission to a role
            arguments: Takes role model object or role id
        3. detach_role: Removes a permission from a role
            arguments: Takes role model object or role id
"""
```

```python
""" Syncing permissions with role, adds provided roles and removes all other roles
    Arguments:
        roles: Takes a list of role ids or role collection
"""
role_collection = Role.all()
role_ids = [1, 2, 3, 4, ...]

permission.sync_roles(role_collection)
# or
permission.sync_roles(role_ids)
# or
permission.sync_roles([]) # clears all role from permission
```

```python
""" Attach role, this will add new permission into role if already not added
    Arguments:
        role: Takes role model object or role id
"""
role = Role.first()

permission.attach_role(role)
# or
permission.attach_role(1)
```

```python
""" Detach role, this will remove permission from role if already added
    Arguments:
        role: Takes role model object or role id
"""
role = Role.first()

permission.detach_role(role)
# or
permission.detach_role(1)
```

</details>
<br/>

#### Working with User

```python
user = User.first()
```

```python
# Add/Remove single role
role = Role.first()

user.assign_role(role) # or you can pass role id
user.revoke_role(role) # or you can pass role id
```

```python
# add/remove multiple roles
roles = Role.all()

user.sync_roles(roles) # or you can also pass list of ids...
user.sync_roles([]) # clears all roles from user
```

```python

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
