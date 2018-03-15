import os
import subprocess
from uranium import current_build

current_build.config.set_defaults({
    "module": "orbital_core"
})

current_build.packages.install(".", develop=True)
from orbital_core.build import bootstrap_build
bootstrap_build(current_build)
