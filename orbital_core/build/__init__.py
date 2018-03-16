import os
import subprocess
from .tasks import (
    main, test, publish, stamp, build_docs
)

def bootstrap_build(build):
    """
    This file contains shared code used by orbital in the build process,
    ensuring consistency across all orbital python services.

    consumers should set some configuration defaults in their ubuild.py, looking like:

        import os
        import subprocess
        from uranium import current_build

        current_build.config.set_defaults({
            "module": "orbital_core"
        })

        current_build.packages.install("orbital-core")
        from orbital_core.build import bootstrap_build
        bootstrap_build(current_build)

    """
    build.task(main)
    build.task(test)
    build.tasks.prepend("test", "main")
    build.task(publish)
    build.task(stamp)
    build.task(build_docs)
