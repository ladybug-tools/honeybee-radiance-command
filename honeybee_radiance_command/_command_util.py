"""Utility functions to process and run shell commands."""
import subprocess
import re
import shlex
import platform
import os


def run_command(input_command, env=None, cwd=None):
    """Run a shell command.

    Args:
        input_command: Input command.
        env: Additional environmental variable that will be added to global environment.
        cwd: Current working directory. If provided command will be executed from this
            folder.
    """
    if platform.system() == 'Windows':
        command = input_command.replace('\'', '"')
    else:
        command = input_command.replace('"', '\'')

    # change cwd - Popen cwd input simply doesn't work.
    cur_dir = os.getcwd()
    if cwd:
        os.chdir(cwd)

    # update environmental variable
    g_env = os.environ.copy()
    if env:
        for k, v in env.items():
            if k.strip().upper() == 'PATH':
                g_env['PATH'] = os.pathsep.join((v, g_env['PATH']))
            else:
                g_env[k] = v

    process = subprocess.Popen(
        command.replace('\\', '/'), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, shell=True, env=g_env
    )

    if process.stdout:
        while True:
            output = process.stdout.readline()
            if (output == b'' or output == '') and process.poll() is not None:
                break
            if output:
                print(output.strip())
        stderr = process.stderr
        rc = process.poll()
    else:
        # stdout is redirected to a file
        _, stderr = process.communicate()
        rc = process.returncode

    if cwd:
        os.chdir(cur_dir)

    if rc != 0:
        errors = _stream_file_content(stderr)
        raise RuntimeError(errors)

    # only gets here is successful
    return 0


def _process_command(input_command):
    """Process input command before execution.

    This method:
        1. separates output file if the output is redirected to a file using >
        2. breaks-down the command into several commands if piping is happening |
    """
    def _raw(text):
        """Raw string representation.

        This is useful to handle edge cases in Windows.
        """

        escape_dict = {
            '\a': r'\a', '\b': r'\b', '\c': r'\c', '\f': r'\f', '\n': r'\n',
            '\r': r'\r', '\t': r'\t', '\v': r'\v', '\'': r'\'', '\"': r'\"',
            '\0': r'\0', '\1': r'\1', '\2': r'\2', '\3': r'\3', '\4': r'\4',
            '\5': r'\5', '\6': r'\6', '\7': r'\7', '\8': r'\8', '\9': r'\9'
        }

        new_string = ''
        for char in text:
            try:
                new_string += escape_dict[char]
            except KeyError:
                new_string += char
        return new_string.replace('\\', '/')

    output_cmd = []
    commands = ' '.join(input_command.split()).split('|')
    STDOUT = (-1, '')  # -1 is PIPE

    for count, command in enumerate(commands[:-1]):

        assert '>' not in command.split('&')[-1], \
            'You cannot redirect stdout with > and pipe the' \
            ' outputs at the same time:\n\t%s' % command

        # check for stdin
        # -1 means use of stdout from the command before this command
        stdin = -1 if count != 0 else ''
        if '<' in command:
            if count == 0:
                stdin = _raw(shlex.split(command.split('<')[-1])[0])
                # replace stdin from the original command
                command = re.sub(r"\s<+\s\S+", '', command)
            else:
                raise ValueError(
                    'You cannot use < for stdin and pipe data to command '
                    'at the same time:\n\t%s' % command
                )

        output_cmd.append(
            {
                'cmd': command.strip().replace('\\', '/'),
                'stdin': stdin.strip() if stdin != -1 else stdin,
                'stdout': STDOUT
            }
        )

    # set-up stdout for the last command
    last_command = commands[-1]
    mode = None
    if '>>' in last_command:
        mode = 'a'
        stdout = _raw(shlex.split(last_command.split('>>')[-1])[0])
    elif '>' in last_command:
        mode = 'w'
        stdout = _raw(shlex.split(last_command.split('>')[-1])[0])
    else:
        stdout = subprocess.PIPE

    command = re.sub(r"\s>+\s\S+", '', last_command)

    stdin = None if len(commands) == 1 else -1
    if '<' in command:
        # now check for stdin
        stdin = _raw(shlex.split(command.split('<')[-1])[0])
        # replace stdin from the original command
        command = re.sub(r"\s<+\s\S+", '', command)

    output_cmd.append(
        {
            'cmd': command.strip().replace('\\', '/'),
            'stdin': stdin,
            'stdout': (stdout, mode)
        }
    )
    return output_cmd


def _stream_file_content(file_object):
    """Return contents of a file like object as a single string."""
    try:
        file_object.seek(0)
    except AttributeError:
        return str(file_object)
    else:
        return ''.join(map(lambda s: s.decode('utf-8'), file_object.readlines()))
