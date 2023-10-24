from enum import Enum as EnumType


class Role(str, EnumType):
    developer = "developer"
    maintainer = "maintainer"
    viewer = "viewer"
