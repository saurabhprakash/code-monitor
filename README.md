## Welcome to Code Monitor

Purpose of code monitor project is to track overall activity of code across languages. There are two parts of codebase, main server which records all the activity and 2nd are various kinds of agent which are to be installed on users system for sending those reports

### Prerequisite: Python3.5

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
  


