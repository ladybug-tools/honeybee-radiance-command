import os
from honeybee_radiance_command._typing import normpath, path_checker, \
    path_checker_multiple
import pytest

test_path1 = 'tests/assets/receiver.rad'
test_path2 = 'tests/assets/dir with space/Jan 1 12.sky'


def test_normpath():
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


def test_path_checker():
    pth1 = path_checker(test_path1)

    pth2 = path_checker(test_path1, extn_list=['.rad'])

    with pytest.raises(ValueError):
        pth2 = path_checker(test_path2, extn_list=['.rad', '.mat'])


def test_path_checker_multiple():
    pth_list = path_checker_multiple([test_path1, test_path2])
    if os.name == 'nt':
        assert pth_list == ['tests/assets/receiver.rad',
                            '"tests/assets/dir with space/Jan 1 12.sky"']
    else:
        assert pth_list == ['tests/assets/receiver.rad',
                            "'tests/assets/dir with space/Jan 1 12.sky'"]

    pth_list_str = path_checker_multiple([test_path1, test_path2],
                                         outputs_as_string=True)
    if os.name == 'nt':
        assert pth_list_str == r'tests/assets/receiver.rad ' \
                               r'"tests/assets/dir with space/Jan 1 12.sky"'
    else:
        assert pth_list_str == r'tests/assets/receiver.rad ' \
                               r"'tests/assets/dir with space/Jan 1 12.sky'"

    pth_list = path_checker_multiple([test_path1, test_path2],
                                     extn_list=('.rad', '.sky'))

    with pytest.raises(ValueError):
        pth_list = path_checker_multiple([test_path1, test_path2],
                                         extn_list=('.rad', '.mat'))
