import click
import configparser
import sys
import re
import requests
from constants import CREDENTIAL_FAIL, LABELS_FAIL, CREDENTIAL_FILE_FAIL, LABELS_FILE_FAIL, REPO_FAIL, GITHUB_API_ADRESS

def erprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

@click.command()
@click.option('-s', '--state', type=click.Choice(['open', 'close', 'all']), help='Filter pulls by state.  [default: open]', default='open')
@click.option('-d', '--delete-old/--no-delete-old', help='Delete labels that do not match anymore.\n [default: True]', default=True)
@click.option('-b', '--base', metavar='BRANCH', help='Filter pulls by base (PR target) branch name.')

@click.option('-a', '--config-auth', metavar='FILENAME', help='File with authorization configuration.')
@click.option('-l', '--config-labels', metavar='FILENAME', help='File with labels configuration.')
#prompt co se vypise pro spusteni
@click.option('--color/--no-color', help='make colored output')
@click.argument('REPOSLUGS', nargs=-1)
#-s, --state [open|closed|all]   Filter pulls by state.  [default: open]
#  -d, --delete-old / -D, --no-delete-old
#                                  Delete labels that do not match anymore.
#                                  [default: True]
#  -b, --base BRANCH               Filter pulls by base (PR target) branch
#                                  name.
#  -a, --config-auth FILENAME      File with authorization configuration.
#  -l, --config-labels FILENAME    File with labels configuration.
def filabel(state, delete_old, base, config_auth, config_labels, color, reposlugs):
	tokenConfig = readConfig(config_auth, {'github' : ['token']}, CREDENTIAL_FILE_FAIL, CREDENTIAL_FAIL)
	labelConfig = readConfig(config_labels, {'labels' : []}, LABELS_FILE_FAIL, LABELS_FAIL)
	repos = loadRepos(reposlugs)
	print(repos)
	click.echo(click.style('Hello World!', fg='green'))
	click.echo(click.style('ATTENTION', blink=True, bold=True))
	gitHub = GitHub(token = tokenConfig['github']['token'])

# Check reposlug if is in valid format.
def loadRepos(reposlugs):
	pattern = re.compile('.+/.+')
	for repo in reposlugs:
		if not pattern.match(repo):
			erprint(REPO_FAIL.format(repo))
			exit(1)
	return reposlugs

# Try read configuration from config files.
def readConfig(file, sections, fileFail, fail):
	if file is None: 
		erprint(fileFail)
		exit(1)
	config = configparser.ConfigParser()
	config.read(file)
	for sec in sections:
		if sec not in config.sections(): 
			erprint(fail)
			exit(1)
		for lb in sections[sec]:
			if lb not in config[sec]:
				erprint(fail)
				exit(1)
	return config

class GitHub:

	def __init__(self, token, session=None):
		self.token = token
		self.session = requests.Session()
		self.session.auth = self.token_auth()
		r = self.session.get('https://api.github.com/user')
		print(r.status_code)
		r.json()
		print(r.json())
	
	def token_auth(self):
		def auth(req):
			req.headers = {
					'Authorization': 'token ' + self.token,
					'User-Agent': 'martilad'
				}
			return req
		return auth

	

if __name__ == '__main__':
	filabel()


