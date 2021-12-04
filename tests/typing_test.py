import os
from honeybee_radiance_command._typing import normpath
import pytest


def test_normpath():
    test_path1 = 'tests/assets/receiver.rad'
    test_path2 = 'tests/assets/dir with space/Jan 1 12.sky'

    normpath_1 = normpath(test_path1)
    normpath_2 = normpath(test_path2)

    assert normpath_1 == 'tests/assets/receiver.rad'
    if os.name == 'nt':
        assert normpath_2 == '"tests/assets/dir with space/Jan 1 12.sky"'
    else:
        assert normpath_2 == "'tests/assets/dir with space/Jan 1 12.sky'"

    assert os.path.exists(test_path1)
    assert os.path.exists(test_path2)

    assert os.path.exists(normpath_1)
    with pytest.raises(AssertionError):
        assert os.path.exists(normpath_2)
