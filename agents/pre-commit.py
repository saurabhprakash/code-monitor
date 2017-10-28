import pip

REQUIRED_PACKAGES = ['git-lint']

def checks_required_package_installation():
    """Checks packages which are required for working of modules and installs them if missing"""
    installed_packages = sorted(["%s==%s" % (i.key, i.version) for i in pip.get_installed_distributions()])
    for package in REQUIRED_PACKAGES:
        if package not in installed_packages:
            pip.main(['install', package])

def install_git_hook():
    """
    """
    

def main():
    """
    """
    checks_required_package_installation()


if __name__ == '__main__':
	main()