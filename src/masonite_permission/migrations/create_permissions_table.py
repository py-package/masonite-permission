from masoniteorm.migrations import Migration


class CreatePermissionsTable(Migration):
    def up(self):
        """Run the migrations."""

        with self.schema.create("roles") as table:
            table.increments("id")
            table.string("name").nullable()
            table.string("slug")
            table.timestamps()

        with self.schema.create("permissions") as table:
            table.increments("id")
            table.string("name").nullable()
            table.string("slug")
            table.timestamps()
            
        # user, role, permission polymorphic relationship
        with self.schema.create("model_has_permissions") as table:
            table.increments('id')
            table.morphs("permissionable")
            table.unsigned_integer("permission_id")
            table.foreign("permission_id").references("id").on("permissions").on_delete("cascade")
            table.timestamps()

        with self.schema.create("role_user") as table:
            table.increments("id")
            table.unsigned_integer("role_id")
            table.unsigned_integer("user_id")
            table.foreign("role_id").references("id").on("roles").on_delete("cascade")
            table.foreign("user_id").references("id").on("users").on_delete("cascade")
            table.timestamps()

    def down(self):
        """Revert the migrations."""

        self.schema.drop("role_user")
        self.schema.drop("permission_role")
        self.schema.drop("permissions")
        self.schema.drop("roles")
