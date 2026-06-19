import os
import shutil

import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    chromium = os.environ.get(
        "PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH",
        shutil.which("chromium"),
    )
    if chromium:
        return {**browser_type_launch_args, "executable_path": chromium}
    return browser_type_launch_args
