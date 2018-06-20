# coding: utf-8
import sys
import subprocess
import re


def exec_cmd(sys_argvs):
    cmd = ''
    for i in range(1, len(sys_argvs)):
        if len(sys_argvs) - 1 == i:
            cmd += sys_argvs[i]
        else:
            cmd += sys_argvs[i]+' '
    result = subprocess.check_output(cmd, shell=True).decode("utf-8")
    return result


def extract_machine_code(dump_result, fuc_name):
    section = select_section(dump_result, fuc_name)
    result = section.split('\t')
    result = list(filter(lambda x: False if re.compile(
        '\n').search(x) else True, result))
    result = ''.join(result)
    result = result.split()
    result = set_raw_machine_code(result)
    return (section, result)


def select_section(dump_result, fuc_name):
    sections = dump_result.split('\n\n')
    result = list(filter(lambda x: re.compile(
        fuc_name+':').search(x), sections))  # <main> <func>
    return result[0].replace('...', '00')


def set_raw_machine_code(machine_code_list):
    for i in range(0, len(machine_code_list)):
        machine_code_list[i] = '\\x'+machine_code_list[i]
    return ''.join(machine_code_list)


if __name__ == "__main__":
    dump_result = exec_cmd(sys.argv)
    result = extract_machine_code(dump_result, '<main>')
    print(result[0]+'\n', result[1])

