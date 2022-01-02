#
# Configuration management
#

#
# Returns system name and system's slash
#
def get_system_params() -> list:
    try:
        # uname doesn't exist in Windows...
        from os import uname
        return [uname()[0], "/"]
    except ImportError:
        return ["nt", "\\"]


SYS_NAME, SYS_SLASH = get_system_params()
