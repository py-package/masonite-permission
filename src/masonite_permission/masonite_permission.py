from masonite.configuration import config


class MasonitePermission:
    def _config(self):
        return config("masonite_permission")

    def _cache(self):
        from wsgi import application

        return application.make("cache")

    def _cache_enabled(self):
        return self._config().get("enable_cache", False)

    def _update_permissions_cache(self, query, user_id):
        if self._cache_enabled():
            self._cache().put(f"permissions-{user_id}", query().get().serialize(), 300)

    def _get_permissions_cache(self, query, user_id):
        if self._cache_enabled():
            if not self._cache().has(f"permissions-{user_id}"):
                self._update_permissions_cache(query, user_id)
            return self._cache().get(f"permissions-{user_id}")
        else:
            return query().get().serialize()
