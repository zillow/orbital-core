from uranium import current_build

current_build.packages.install("uranium-plus[vscode]")
import uranium_plus

current_build.config.update(
    {
        "uranium-plus": {
            "module": "orbital_core",
            "test": {"packages": ["pytest-aiohttp", "pytest-xdist"]},
        }
    }
)

uranium_plus.bootstrap(current_build)
