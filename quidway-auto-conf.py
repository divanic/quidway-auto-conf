#!/usr/bin/env python3.7
import pexpect
import sys
import getpass
import time


def open_file(filename):
    # file lines to list
    with open(filename) as f:
        f = f.readlines()
        for i in range(len(f)):
            line = f[i].strip()
            f[i] = line
        return f

def check_version(session):
    session.expect('>')
    session.sendline('dis version')
    session.expect('>')
    f = session.before
    v = False
    if 'S5352C-EI ' in f:
        v = True
    return(v)


def main():
    USER = input('Enter existing user: ')
    PASSWORD = getpass.getpass()
    ips = open_file(sys.argv[2])
    conf = open_file(sys.argv[1])

    print('Adding configuration from file {} to hosts at {}'.format(sys.argv[1],time.ctime()))
    for i in range(len(ips)):
        HOST = ips[i]
        with pexpect.spawn('ssh {}@{}'.format(USER, HOST), encoding='utf-8') as ssh:
            i = ssh.expect(['word', 'yes/no'])
            if i == 1:
                ssh.sendline('yes')
                ssh.expect('word')
            ssh.sendline(PASSWORD)
            ssh.expect('>')
            ssh.sendline('screen-length 0 temporary')
            if check_version(ssh) is False:
                print('Host ' + HOST + ' has wrong platform.')
                continue
            ssh.sendline('sys')
            for i in conf:
                ssh.expect(']')
                ssh.sendline(i)
            ssh.expect(']')
            ssh.close()
            print('Host {} is done.'.format(HOST))


if __name__ == '__main__':
    main()
