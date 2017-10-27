from urllib.parse import urlencode
from urllib.request import Request, urlopen

import requests
import json

from pylint.lint import Run

url = 'http://localhost:8000/monitor/'
PROJECT_NAME = 'cvc'
CODEBASE = '/Users/saurabh/office/cvc/webapp'

#results_file = open("result.txt", "w")

results = Run(['--load-plugins=pylint_django', '--rcfile=pylintrc', CODEBASE], exit=False)

print ("Current Score is: %s, Errors: %s, Convention issues: %s, Warnings: %s" % (\
	results.linter.stats['global_note'], results.linter.stats['error'], 
	results.linter.stats['convention'], results.linter.stats['warning']))

data = {
	'project': PROJECT_NAME,
	'score': results.linter.stats['global_note'],
	'metadata': json.dumps({
		"errors": results.linter.stats['error'],
		"convention": results.linter.stats['convention'],
		"warning": results.linter.stats['warning']
	})	
}
print (data)

r = requests.post(url, 
	data=data
	# files={
	# 	"report": results_file,
	# }
)
#results_file.close()
