from __future__ import annotations

import asyncio
from collections.abc import MutableMapping
from dataclasses import dataclass
from typing import Any, Callable, Generic, Protocol, TypeVar, runtime_checkable

from reactpy.core.types import RootComponentConstructor, LocalStorage, SessionStorage

_App = TypeVar("_App")


@runtime_checkable
class BackendType(Protocol[_App]):
    """Common interface for built-in web server/framework integrations"""

    Options: Callable[..., Any]
    """A constructor for options passed to :meth:`BackendType.configure`"""

    def configure(
        self,
        app: _App,
        component: RootComponentConstructor,
        options: Any | None = None,
    ) -> None:
        """Configure the given app instance to display the given component"""

    def create_development_app(self) -> _App:
        """Create an application instance for development purposes"""

    async def serve_development_app(
        self,
        app: _App,
        host: str,
        port: int,
        started: asyncio.Event | None = None,
    ) -> None:
        """Run an application using a development server"""


_Carrier = TypeVar("_Carrier")


@dataclass
class Connection(Generic[_Carrier]):
    """Represents a connection with a client"""

    scope: MutableMapping[str, Any]
    """An ASGI scope or WSGI environment dictionary"""

    location: Location
    """The current location (URL)"""

    local_storage: LocalStorage
    """An object to obtain client localStorage"""

    session_storage: SessionStorage
    """An object to obtain client sessionStorage"""

    carrier: _Carrier
    """How the connection is mediated. For example, a request or websocket.

    This typically depends on the backend implementation.
    """


@dataclass
class Location:
    """Represents the current location (URL)

    Analogous to, but not necessarily identical to, the client-side
    ``document.location`` object.
    """

    pathname: str
    """the path of the URL for the location"""

    search: str
    """A search or query string - a '?' followed by the parameters of the URL.

    If there are no search parameters this should be an empty string
    """
