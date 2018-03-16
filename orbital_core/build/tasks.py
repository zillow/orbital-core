import os
import multiprocessing

def main(build):
    build.packages.install(".", develop=True)
    build.run_task("build_docs")

def test(build):
    build.packages.install("jedi")
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    build.packages.install("pytest-xdist")
    build.packages.install("pytest-aiohttp")
    build.packages.install("pytest-runfailed")
    build.executables.run([
        "py.test", "--cov", build.config["module"],
        "{0}/tests".format(build.config["module"]),
        "--cov-report", "term-missing",
        "-n", "{0}".format(multiprocessing.cpu_count())
    ] + build.options.args)

def publish(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel", "--universal", "upload", "--release"
    ])

def stamp(build):
    """ after a distribution, stamp the current build. """
    build.packages.install("gitchangelog")
    changelog_text = subprocess.check_output(["gitchangelog"])
    with open(os.path.join(build.root, "CHANGELOG"), "wb+") as fh:
        fh.write(changelog_text)

def build_docs(build):
    build.packages.install("sphinx")
    build.packages.install("sphinx_rtd_theme")
    build.executables.run([
        "sphinx-build",
        os.path.join(build.root, "docs"),
        os.path.join(build.root, "target", "docs")
    ])
