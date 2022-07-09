# Masonite Permission

<p align="center">
    <img src="https://banners.beyondco.de/Masonite%20Permission.png?theme=light&packageManager=pip+install&packageName=masonite-permission&pattern=charlieBrown&style=style_2&description=Associate+users+with+roles+and+permissions.&md=1&showWatermark=1&fontSize=100px&images=adjustments&widths=50&heights=50">
</p>

<p align="center">
  
  <img alt="GitHub Workflow Status" src="https://github.com/py-package/masonite-permission/actions/workflows/pythonapp.yml/badge.svg">

  <img alt="PyPI" src="https://img.shields.io/pypi/v/masonite-permission">
  <img alt="issues" src="https://img.shields.io/github/issues/py-package/masonite-permission">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python Version">
  <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/v/release/py-package/masonite-permission">
  <img alt="License" src="https://img.shields.io/github/license/py-package/masonite-permission">
  <a href="https://github.com/py-package/masonite-permission/stargazers"><img alt="star" src="https://img.shields.io/github/stars/py-package/masonite-permission" /></a>
  <img alt="downloads" src="https://img.shields.io/pypi/dm/masonite-permission?style=flat" />
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## Introduction

Associate users with roles and permissions to control access to your application.

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
from src.masonite_permission.mixins import (HasPermissions, HasRoles)

class User(Model, SoftDeletesMixin, Authenticates, HasRoles, HasPermissions):
    """User Model."""

    __fillable__ = ["name", "email", "password"]
    __hidden__ = ["password"]
    __auth__ = "email"
```

## Usage

#### Working with Role

**Creating Roles**

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

**Add permissions into roles**

```python
""" Add permissions into roles
    Available Methods:
        1. sync_permissions: Syncs the permissions with the role
            arguments: Takes a list/tuple of permission slugs
        2. attach_permission: Adds a permission to a role
            arguments: Takes permission model object or permission slug
        3. detach_permission: Removes a permission from the role
            arguments: Takes permission model object or permission slug
"""
```

```python
""" Syncing permissions with role, adds provided permissions and removes all other permissions
    Arguments:
        permissions: Takes a list/tuple of permission slugs
"""
role.sync_permissions(["create-post", "read-post", "update-post", "delete-post"])
# or
role.sync_permissions("create-post", "read-post", "update-post", "delete-post")
# or
role.sync_permissions([]) # clears all permissions from role
```

```python
""" Attach permission, this will add new permission into role if already not added
    Arguments:
        permission: Takes permission model object or permission slug
"""
role.attach_permission("create-post")
# or
role.attach_permission(Permission.first())
```

```python
""" Detach permission, this will remove permission from role if already added
    Arguments:
        permission: Takes permission model object or permission slug
"""

role.detach_permission("create-post")
# or
role.detach_permission(Permission.first())
```

#### Working with Permission

**Creating Permission**

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

**Add permissions into roles**

```python
""" Add permissions into roles
    Available Methods:
        1. sync_roles: Syncs the roles with the permission
            arguments: Takes a list/tuple of role slugs
        2. attach_role: Adds a permission to a role
            arguments: Takes role model object or role slug
        3. detach_role: Removes a permission from a role
            arguments: Takes role model object or role slug
"""
```

```python
""" Syncing permissions with role, adds provided roles and removes all other roles
    Arguments:
        roles: Takes a list of role ids or role collection
"""
permission.sync_roles(['admin', 'editor'])
# or
permission.sync_roles('admin', 'editor')
# or
permission.sync_roles([]) # clears all role from permission
```

```python
""" Attach role, this will add new permission into role if already not added
    Arguments:
        role: Takes role model object or role slug
"""
role = Role.first()

permission.attach_role(role)
# or
permission.attach_role('admin')
```

```python
""" Detach role, this will remove permission from role if already added
    Arguments:
        role: Takes role model object or role id
"""
role = Role.first()

permission.detach_role(role)
# or
permission.detach_role('admin')
```

#### Working with User

```python
user = User.first()
```

**Adding/Removing single role**

```python
# Add/Remove single role
role = Role.first()

user.assign_role(role) # or you can pass role id
user.revoke_role(role) # or you can pass role id
```

**Adding/Removing multiple roles**

```python
# add/remove multiple roles
roles = Role.all()

user.sync_roles(roles) # or you can also pass list of ids...
user.sync_roles([]) # clears all roles from user
```

**Checking if user has roles**

```python
# check if user has role
user.has_role_of("admin") # returns boolean

# check if user has any of the roles
user.has_any_role(["admin", "editor"]) # returns boolean
# or
user.has_any_role("admin", "editor")

# check if user has all of the roles
user.has_all_roles(["admin", "editor"]) # returns boolean
# or
user.has_all_roles("admin", "editor")
```

**Adding/Removing single direct permission**

```python
# Add/Remove single permission
user.give_permission_to("read-post", "edit-post") # this can be a tuple or a list
# or
user.give_permission_to(["read-post", "edit-post"])

user.revoke_permission_to("read-post", "edit-post") # this can be a tuple or a list
# or
user.revoke_permission_to(["read-post", "edit-post"])
```

**Adding/Removing multiple direct permissions**

```python
# add/remove multiple direct permissions
permissions = Permission.all().pluck("slug")

user.sync_permissions(permissions) # tuples or list of permission slug
user.sync_permissions([]) # clears all permissions from user
```

**Checking if user has permissions**

```python

# check if user has permission (for single permission)
user.has_permission_to("read-post") # returns boolean

# check if user has any of the permissions
user.has_any_permission(["read-post", "edit-post"]) # returns boolean
# or
user.has_any_permission("read-post", "edit-post")

# check if user has all of the permissions
user.has_all_permissions(["read-post", "edit-post"]) # returns boolean
# or
user.has_all_permissions("read-post", "edit-post") # returns boolean

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


## License

Masonite Permission is open-sourced software licensed under the [MIT license](LICENSE).
