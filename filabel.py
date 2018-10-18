import click
import configparser
import sys
import re
import fnmatch
import traceback
from constants import CREDENTIAL_FAIL, LABELS_FAIL, CREDENTIAL_FILE_FAIL, LABELS_FILE_FAIL, REPO_FAIL, GITHUB_API_ADRESS
from github import GitHub, GitHubGetException
from print import Print
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'MI-PYT je nejlepší předmět na FITu!'

def erprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

@click.command()
@click.option('-s', '--state', type=click.Choice(['open', 'closed', 'all']), help='Filter pulls by state.  [default: open]', default='open')
@click.option('-d/-D', '--delete-old/--no-delete-old', help='Delete labels that do not match anymore.\n [default: True]', default=True)
@click.option('-b', '--base', metavar='BRANCH', help='Filter pulls by base (PR target) branch name.')
@click.option('-a', '--config-auth', metavar='FILENAME', help='File with authorization configuration.')
@click.option('-l', '--config-labels', metavar='FILENAME', help='File with labels configuration.')
@click.argument('REPOSLUGS', nargs=-1)
#-s, --state [open|closed|all]   Filter pulls by state.  [default: open]
#  -d, --delete-old / -D, --no-delete-old
#                                  Delete labels that do not match anymore.
#                                  [default: True]
#  -b, --base BRANCH               Filter pulls by base (PR target) branch
#                                  name.
#  -a, --config-auth FILENAME      File with authorization configuration.
#  -l, --config-labels FILENAME    File with labels configuration.
def filabel(state, delete_old, base, config_auth, config_labels, reposlugs):
	"""CLI tool for filename-pattern-based labeling of GitHub PRs"""
	if config_auth is None: 
		erprint(CREDENTIAL_FILE_FAIL)
		exit(1)
	if config_labels is None: 
		erprint(LABELS_FILE_FAIL)
		exit(1)
	tokenConfig = readConfig(config_auth, {'github' : ['token']}, CREDENTIAL_FILE_FAIL, CREDENTIAL_FAIL)
	labelConfig = readConfig(config_labels, {'labels' : []}, LABELS_FILE_FAIL, LABELS_FAIL)
	repos = loadRepos(reposlugs)
	knownLabels = {i for i in labelConfig['labels']}
	try:
		gitHub = GitHub(token = tokenConfig['github']['token'])
		for repo in repos:
			labelOneRepo(repo, gitHub, base, state, delete_old, labelConfig, knownLabels)
	except GitHubGetException as exception:
		click.echo(exception.getMessage(), err=True)
		sys.exit(exception.getCode())

def labelOneRepo(repo, gitHub, base, state, delete_old, labelConfig, knownLabels):
	if base != None:
		data = { 'state' : state, 'base' : base}
	else:
		data = { 'state' : state}
	try:
		IS = {value['html_url']:value['number'] for value in gitHub.getIssuesAsPR(repo, data)}
		PR = [[x['html_url'], x['number'], IS[x['html_url']]] for x in gitHub.getPRForRepo(repo, data) ]
		Print.printRepoOK(repo)
	except Exception as exception:
		Print.printRepoFAIL(repo)
		#traceback.print_exc()
		return
	for pr in PR:
		try:
			actLabels = {x['name'] for x in gitHub.getLabelsForIssue(repo, pr[2])}
			actFiles = [x['filename'] for x in gitHub.getFilesforPR(repo, pr[1])]
			addLabels = matchFiles(labelConfig, actFiles)
			PRknownLabels = actLabels & knownLabels
			keepLabelsNotKnow = actLabels - knownLabels
			deleteLabels = set()
			keepLabels = PRknownLabels & addLabels
			if delete_old:
				deleteLabels = PRknownLabels - addLabels
			addLabels = addLabels - PRknownLabels
			tp = [[x, '-'] for x in deleteLabels] + [[x, '+'] for x in addLabels] + [[x, '='] for x in keepLabels]
			pushLabelsSet = (keepLabelsNotKnow | keepLabels | addLabels)
			if not delete_old:
				pushLabelsSet = pushLabelsSet | (PRknownLabels - addLabels)
			gitHub.addLabelsForIssue(repo, pr[2], [x for x in pushLabelsSet])
			testLabels = [x['name'] for x in gitHub.getLabelsForIssue(repo, pr[2])]
			if (set(testLabels) ==  pushLabelsSet):
				Print.printPROK(pr[0])
				Print.printLabels(tp)
			else:
				Print.printPRFAIL(pr[0])
		except Exception as exception:
			Print.printPRFAIL(pr[0])
			#traceback.print_exc()
			continue
	
def matchFiles(config, files):
	lb = set()
	for file in files:
		for i in config['labels']:
			for j in config['labels'][i].strip().split('\n'):
				if fnmatch.fnmatch(file, j.strip()):
					lb.add(i)
	return lb


# Check reposlug if is in valid format.
def loadRepos(reposlugs):
	pattern = re.compile('.+/.+')
	for repo in reposlugs:
		if not pattern.match(repo):
			erprint(REPO_FAIL.format(repo))
			sys.exit(1)
	return reposlugs

# Try read configuration from config files.
def readConfig(file, sections, fileFail, fail):
	config = configparser.ConfigParser()
	config.read(file)
	for sec in sections:
		if sec not in config.sections(): 
			erprint(fail)
			sys.exit(1)
		for lb in sections[sec]:
			if lb not in config[sec]:
				erprint(fail)
				sys.exit(1)
	return config


if __name__ == '__main__':
	filabel()


