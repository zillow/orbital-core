
def main(build):
    build.packages.install(".", develop=True)

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
    return subprocess.call(
        ["make", "html"], cwd=os.path.join(build.root, "docs")
    )
