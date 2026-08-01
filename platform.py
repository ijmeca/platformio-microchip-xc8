import os

from platformio.public import PlatformBase


XC8_MAIN_TEMPLATE = """#include <xc.h>


void main(void)
{


    while (1) {

    }
}
"""


class Microchip8Platform(PlatformBase):
    def configure_default_packages(self, variables, targets):
        return super().configure_default_packages(variables, targets)

    def generate_sample_code(self, project_config, environment):
        frameworks = project_config.get(
            "env:%s" % environment, "framework", []
        )
        if "xc8" not in frameworks:
            raise NotImplementedError

        src_dir = project_config.get("platformio", "src_dir")
        main_path = os.path.join(src_dir, "main.c")
        if os.path.isfile(main_path):
            return False

        os.makedirs(src_dir, exist_ok=True)
        with open(main_path, "w", encoding="utf-8", newline="\n") as fp:
            fp.write(XC8_MAIN_TEMPLATE)
        return True
