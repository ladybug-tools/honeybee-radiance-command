import pytest

from honeybee_radiance_command._command import Command


def test_defaults():
    cmd = Command()
    assert cmd.command == 'command'
    assert cmd.output == None
    assert cmd.pipe_to == None
    assert cmd.to_radiance() == 'command'


def test_output_assignment():
    cmd = Command(output='command.res')
    assert cmd.output == 'command.res'
    assert cmd.to_radiance() == 'command > command.res'


def test_pipe_to():
    cmd_1 = Command(output='command_1.res')
    assert cmd_1.output == 'command_1.res'
    cmd_2 = Command(output='command_2.res')
    cmd_1.pipe_to = cmd_2
    assert cmd_1.to_radiance() == 'command | command > command_2.res'


def test_subclass():

    class Rtrace(Command):
        pass

    rtrace = Rtrace()
    assert rtrace.command == 'rtrace'

def test_path_checker():
    test_path1=r'C:\some directory\some_file.rad'
    test_path2=r'C:\some directory\some_file.bmp'

    cmd=Command()
    pth1=cmd.path_checker(test_path1)
    assert pth1==r'"C:\some directory\some_file.rad"'

    with pytest.raises(ValueError):
        pth2=cmd.path_checker(test_path2,extn_list=['.rad','.sky'])

def test_path_checker_multiple():
    test_path1=r'C:\some directory\some_file.rad'
    test_path2=r'C:\some directory\some_file.bmp'
    test_path3 = r'C:\some directory\some_file2.rad'

    cmd=Command()
    pth_list=cmd.path_checker_multiple([test_path1,test_path2])
    assert pth_list==[r'"C:\some directory\some_file.rad"',
                  r'"C:\some directory\some_file.bmp"']

    pth_list_str=cmd.path_checker_multiple([test_path1,test_path2],outputs_as_string=True)
    assert pth_list_str==r'"C:\some directory\some_file.rad" "C:\some directory\some_file.bmp"'

    with pytest.raises(ValueError):
        pth_list=cmd.path_checker_multiple([test_path1,test_path2,test_path3],
                                           extn_list=('.rad','.sky'))

def test_instance_checker():
    cmd=Command()
    val1=cmd.instance_checker(32.1,float,'float')
    assert type(val1)==float

    with pytest.raises(TypeError):
        val2=cmd.instance_checker(32.1,int,'int')

    class Rtrace():
        pass

    val3=cmd.instance_checker(None,Rtrace,'Rtrace',return_class_default=True)

    assert isinstance(val3,Rtrace)

