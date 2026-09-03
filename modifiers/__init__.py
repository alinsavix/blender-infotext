"""Automatic discovery and registration for modifier display handlers.

Every public module in this package must declare ``MODIFIER_HANDLERS`` as a
mapping from Blender modifier type to a callable or a callable's local name.
"""

from importlib import import_module
from pkgutil import iter_modules
from typing import Any, Callable, Dict, Mapping, Union


ModifierHandler = Callable[..., None]
HandlerDeclaration = Union[str, ModifierHandler]


def discover_modifier_handlers() -> Dict[str, ModifierHandler]:
    """Import modifier modules and build their declared handler registry."""
    handlers: Dict[str, ModifierHandler] = {}

    for module_info in sorted(iter_modules(__path__), key=lambda info: info.name):
        if module_info.name.startswith("_"):
            continue

        module = import_module(f"{__name__}.{module_info.name}")
        declarations: Any = getattr(module, "MODIFIER_HANDLERS", None)

        if not isinstance(declarations, Mapping) or not declarations:
            raise RuntimeError(
                f"{module.__name__} must declare a non-empty MODIFIER_HANDLERS mapping"
            )

        for modifier_type, declaration in declarations.items():
            if not isinstance(modifier_type, str) or not modifier_type:
                raise TypeError(
                    f"{module.__name__} declares an invalid modifier type: {modifier_type!r}"
                )

            if isinstance(declaration, str):
                try:
                    handler = getattr(module, declaration)
                except AttributeError as error:
                    raise RuntimeError(
                        f"{module.__name__} has no handler named {declaration!r}"
                    ) from error
            else:
                handler = declaration
            if not callable(handler):
                raise TypeError(
                    f"Handler for {modifier_type} in {module.__name__} is not callable"
                )

            if modifier_type in handlers:
                raise RuntimeError(f"Duplicate handler for modifier {modifier_type}")

            handlers[modifier_type] = handler

    return handlers
