from platformio.public import PlatformBase


class Microchip8Platform(PlatformBase):
    def configure_default_packages(self, variables, targets):
        return super().configure_default_packages(variables, targets)
