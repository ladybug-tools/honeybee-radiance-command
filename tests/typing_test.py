from honeybee_radiance_command._typing import path_checker, path_checker_multiple
import pytest
import os

# TODO: Add tests for all methods in the typing module.

def test_path_checker():
    test_path1 = r'test/some directory/some_file.rad'
    test_path2 = r'test/some directory/some_file.bmp'

    pth1 = path_checker(test_path1)
    if os.name == 'nt':
        assert pth1 == r'"test\some directory\some_file.rad"'
    else:
        assert pth1 == r"'test/some directory/some_file.rad'"

    with pytest.raises(ValueError):
        pth2 = path_checker(test_path2, extn_list=['.rad', '.sky'])


def test_path_checker_multiple():
    test_path1 = r'test/some directory/some_file.rad'
    test_path2 = r'test/some directory/some_file.bmp'
    test_path3 = r'test/some directory/some_file2.rad'

    pth_list = path_checker_multiple([test_path1, test_path2])
    if os.name == 'nt':
        assert pth_list == [r'"test\some directory\some_file.rad"',
                            r'"test\some directory\some_file.bmp"']
    else:
        assert pth_list == [r"'test/some directory/some_file.rad'",
                            r"'test/some directory/some_file.bmp'"]

    pth_list_str = path_checker_multiple([test_path1, test_path2],
                                         outputs_as_string=True)
    if os.name == 'nt':
        assert pth_list_str == r'"test\some directory\some_file.rad" ' \
                               r'"test\some directory\some_file.bmp"'
    else:
        assert pth_list_str == r"'test/some directory/some_file.rad' " \
                               r"'test/some directory/some_file.bmp'"

    with pytest.raises(ValueError):
        pth_list = path_checker_multiple([test_path1, test_path2, test_path3],
                                         extn_list=('.rad', '.sky'))
