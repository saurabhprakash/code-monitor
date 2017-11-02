import pip
import os
import subprocess

REQUIRED_PACKAGES = ['git-lint', 'https://github.com/saurabhprakash/closure-linter/archive/master.zip', 'requests',
                     'pylint', 'pep8']

RUNNABLE_CODE_ON_PRE_COMMIT = """#!/usr/bin/env python
import subprocess
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

def internet_on():
    try:
        urllib2.urlopen('https://www.google.co.in', timeout=3)
        return True
    except urllib2.URLError as err:
        return False

def send_data(data):
    import requests
    r = requests.post("http://localhost:8000/commit/", data=data, timeout=(3, 15))
    print(r.status_code, r.reason)

def send_code_diff_status():
    proc = subprocess.Popen(["git lint"], shell=True, stdout=subprocess.PIPE)
    email = subprocess.Popen(["git", "config", "user.email"], shell=True, stdout=subprocess.PIPE)
    username = subprocess.Popen(["git", "config" "user.name"], shell=True, stdout=subprocess.PIPE)
    data = {
        'lint_report': proc.stdout.read().decode("utf-8"),
        'email': email.stdout.read().decode("utf-8").strip(),
        'username': username.stdout.read().decode("utf-8").strip()
    }
    if internet_on():
        send_data(data)
    else:
        print('Internet Not Working, Please enable')

def main():
   send_code_diff_status()

if __name__ == "__main__":
    main()
"""

def checks_required_package_installation():
    """Checks packages which are required for working of modules and installs them if missing"""
    installed_packages = sorted(["%s==%s" % (i.key, i.version) for i in pip.get_installed_distributions()])
    for package in REQUIRED_PACKAGES:
        if package not in installed_packages:
            pip.main(['install', package])

def install_git_hook():
    """
    """
    try:
        os.remove('.git/hooks/pre-commit')
    except:
        print('No existing pre commit hook found')
        pass

    f = open('.git/hooks/pre-commit', 'w+')
    f.write(RUNNABLE_CODE_ON_PRE_COMMIT)
    f.close()
    subprocess.call(['chmod', '0755', '.git/hooks/pre-commit'])


def main():
    """main function executor, call package installation and git hooks setup methods
    """
    checks_required_package_installation()
    install_git_hook()


if __name__ == '__main__':
    main()

