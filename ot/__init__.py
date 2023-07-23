# SPDX-License-Identifier: GPL-2.0-or-later

from . import operators
from . import converter
from . import presets

modules = (
    operators,
    converter,
    presets,
)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()