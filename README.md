## Welcome to Code Monitor

Purpose of code monitor project is to track overall activity of code across languages. There are two parts of codebase, main server which records all the activity and 2nd are various kinds of agent which are to be installed on users system for sending those reports

### Prerequisite: Python3.5

##### For setting code in local:
 - Create a python virtual env
 - Clone code inside virtual env
 - Inside env run "pip install -r requirements.txt"
 - Install redis and run it
 - From local_settings.py.template file create "local_settings.py" file
 - Make necessary database chages

### Things which can be done

- Track each commits: 
  - Download [pre-commit](https://github.com/saurabhprakash/code-monitor/blob/master/agents/pre-commit.py) file to your root codebase, and run "python pre-commit.py": This will install the required dependencies to your system
  - Post setup pre-commit.py downloaded above can be deleted(or remove from git tracking code)
- Track overall status of codebase


### Addtional setup specific to languages(Default setup handles for python and html):
  - css lint setup process: https://github.com/CSSLint/csslint/wiki/Command-line-interface#running-on-nodejs
  - scss lint setup process: https://github.com/brigade/scss-lint#installation
  - php setup process: http://pear.php.net/package/PHP_CodeSniffer/
  - Javascript:
    - http://jshint.com/install/
    - https://github.com/google/closure-linter/zipball/master
  - Ruby: https://github.com/yorickpeterse/ruby-lint#installation
  - C++: https://github.com/google/styleguide/tree/gh-pages/cpplint
  - CofeeScript: http://www.coffeelint.org/#install
  - Java: https://github.com/pmd/pmd
  

Java setup:
 -  brew install checkstyle
 - ```
     $ cd $HOME
     $ curl -OL https://github.com/pmd/pmd/releases/download/pmd_releases%2F6.8.0/pmd-bin-6.8.0.zip
     $ unzip pmd-bin-6.8.0.zip
     $ alias pmd="$HOME/pmd-bin-6.8.0/bin/run.sh pmd"
     $ pmd -d /usr/src -R rulesets/java/quickstart.xml -f text
   ```
 - ln -s <location>/pmd-bin-6.8.0/bin/run.sh /usr/local/bin/run.sh
