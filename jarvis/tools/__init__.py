from . import filesystem, shell

TOOL_REGISTRY = {
    "filesystem.read": filesystem.read,
    "filesystem.write": filesystem.write,
    "filesystem.list": filesystem.list,
    "shell.run": shell.run,
}
