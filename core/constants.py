SUBJECT = 'Code monitor report'
MESSAGE = 'Code monitor report'

SUCCESS = 'success'
MESSAGE = 'message'
DOT = '.'
FILE_EXTENSIONS_LOCATION_INDEX = -1


USER_DOES_NOT_EXIST = 'user does not exist, please get created by admin'

PYTHON = 'python'
JAVA = 'java'
JAVASCRIPT = 'javascript'
HTML = 'html'

LANGUAGE_FILE_EXTENSIONS = {
    'py': PYTHON,
    'java': JAVA,
    'js': JAVASCRIPT,
    'html': HTML
}

LANGUAGE_FILE_EXTENSIONS_REGEX = {
    PYTHON: r'[0-9a-zA-Z:\/\-_ ]+.py',
    JAVA: r'[0-9a-zA-Z:\/\-_ ]+.java',
    JAVASCRIPT: r'[0-9a-zA-Z:\/\-_ ]+.js'
}

INSTANT_COMMIT_REPORT = 'commit_report'
