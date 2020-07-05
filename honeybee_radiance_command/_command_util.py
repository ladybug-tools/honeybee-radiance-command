"""Utility functions to process and run shell commands."""
import subprocess
import re
import shlex
import platform
import os
import traceback


def run_command(input_command, env=None, cwd=None):
    """Run a shell command.

    Args:
        input_command:

    """
    open_files = []
    processes = []
    if platform.system() == 'Windows':
        shell = True if env else False
    else:
        shell = False

    # change cwd - Popen cwd input simply doesn't work.
    if cwd:
        cur_dir = os.getcwd()
        os.chdir(cwd)

    cmds = _process_command(input_command)
    for cmd in cmds:
        command = shlex.split(cmd['cmd'])
        # stdin
        if not cmd['stdin']:
            stdin = None
        elif cmd['stdin'] == -1:
            stdin = processes[-1].stdout
        else:
            # std information is streamed from a file
            open_files.append(open(cmd['stdin'], 'r'))
            stdin = open_files[-1]
        # stdout
        if cmd['stdout'][0] == -1:
            stdout = subprocess.PIPE
        else:
            fp, mode = cmd['stdout']
            open_files.append(open(fp, mode))
            stdout = open_files[-1]
        try:
            p = subprocess.Popen(
                command, stdin=stdin, stdout=stdout, stderr=subprocess.PIPE,
                env=env, shell=shell
            )
        except Exception:
            # change the path back to cur_dir
            if cwd:
                os.chdir(cur_dir)
            raise Exception(traceback.format_exc())
        else:
            processes.append(p)
    # Allow processes to receive a SIGPIPE if process after that exits.
    # based on https://security.openstack.org/guidelines/dg_avoid-shell-true.html
    for process in processes[:-1]:
        process.stdout.close()

    process = processes[-1]
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

    # close all the open files
    for f in open_files:
        f.close()

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

        assert '>' not in command, \
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
