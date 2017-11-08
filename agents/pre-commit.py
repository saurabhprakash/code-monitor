import pip
import os
import subprocess

REQUIRED_PACKAGES = ['git-lint', 'https://github.com/saurabhprakash/closure-linter/archive/master.zip', 'requests',
                     'pylint', 'pep8']

RUNNABLE_CODE_ON_PRE_COMMIT = """#!/usr/bin/env python
import subprocess
import os
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
    try:
        r = requests.post("http://35.200.18.224/commit/", json=data, timeout=(5, 15))
        print(r.status_code, r.reason)
    except:
        print ('Error sending commit statistics, commit will proceed. Please inform support')
def process_total_changes(total_changes_report):
    file_changes_status = []
    for line in total_changes_report.splitlines():
        report = line.split('\t')
        file_changes_status.append({
                'lines_added': int(report[0]),
                'lines_removed': int(report[1]),
                'file_path': report[2]
            })
    return file_changes_status
def send_code_diff_status():
    if os.name == 'nt':
        proc = subprocess.Popen(["git-lint", "--json"], shell=True, stdout=subprocess.PIPE)
        email = subprocess.Popen(["git", "config", "user.email"], shell=True, stdout=subprocess.PIPE)
        username = subprocess.Popen(["git", "config" "user.name"], shell=True, stdout=subprocess.PIPE)
        total_changes = subprocess.Popen(["git", "diff" "--numstat"], shell=True, stdout=subprocess.PIPE)
    else:
        proc = subprocess.Popen(["git-lint --json"], shell=True, stdout=subprocess.PIPE)
        email = subprocess.Popen(["git config user.email"], shell=True, stdout=subprocess.PIPE)
        username = subprocess.Popen(["git config user.name"], shell=True, stdout=subprocess.PIPE)
        total_changes = subprocess.Popen(["git diff --numstat"], shell=True, stdout=subprocess.PIPE)

    total_changes = process_total_changes(total_changes.stdout.read().decode("utf-8").strip())

    data = {
        'lint_report': proc.stdout.read().decode("utf-8"),
        'email': email.stdout.read().decode("utf-8").strip(),
        'username': username.stdout.read().decode("utf-8").strip(),
        'total_changes': total_changes
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

