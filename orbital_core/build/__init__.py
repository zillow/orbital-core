import os
import subprocess

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

    @build.task
    def main(build):
        build.packages.install(".", develop=True)

    @build.task
    def test(build):
        main(build)
        build.packages.install("jedi")
        build.packages.install("pytest")
        build.packages.install("pytest-cov")
        build.packages.install("pytest-aiohttp")
        build.executables.run([
            "py.test", "--cov", build.config["module"],
            "{0}/tests".format(build.config["module"]),
            "--cov-report", "term-missing"
        ] + build.options.args)

    @build.task
    def publish(build):
        """ distribute the uranium package """
        build.packages.install("wheel")
        build.executables.run([
            "python", "setup.py",
            "sdist", "bdist_wheel", "--universal", "upload", "--release"
        ])

    @build.task
    def stamp(build):
        """ after a distribution, stamp the current build. """
        build.packages.install("gitchangelog")
        changelog_text = subprocess.check_output(["gitchangelog"])
        with open(os.path.join(build.root, "CHANGELOG"), "wb+") as fh:
            fh.write(changelog_text)

    @build.task
    def build_docs(build):
        build.packages.install("sphinx")
        return subprocess.call(
            ["make", "html"], cwd=os.path.join(build.root, "docs")
        )
