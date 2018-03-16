
def test_tasks_importable_individually():
    """
    tasks should be importable individually,
    to be extended or used separately.
    """
    from orbital_core.build.tasks import (
        main, test, publish, stamp, build_docs
    )
