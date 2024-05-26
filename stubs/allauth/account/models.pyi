from typing import Iterable

from django.contrib.auth.models import User
from django.db.models import Manager, Model

class EmailAddress(Model):
    user: User
    emial: str
    primary: bool
    verified: bool

    objects: Manager["EmailAddress"]

    def save(
        self,
        force_insert: bool | tuple[type, ...] = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None: ...
