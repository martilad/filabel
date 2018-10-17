import requests
from constants import GITHUB_API_ADRESS

class GitHubGetException(Exception):

	def __init__(self, response):
		self.code = response.status_code
		self.mess = response.json().get('message', 'No message')

	def getMessage(self):
		return 'GitHub ERROR - {} - {}'.format(self.code, self.mess)

	def getCode(self):
		return self.code


class GitHub:

	def __init__(self, token, session=None):
		self.token = token
		self.session = requests.Session()
		self.session.auth = self.token_auth()
		
	def token_auth(self):
		def auth(req):
			req.headers = {
					'Authorization': 'token ' + self.token,
					'User-Agent': 'Python'
				}
			return req
		return auth

	def getUrl(self, url, data):
		r = self.session.get(url, json=data)
		if r.status_code != 200:
			raise GitHubGetException(r)
		return r

	def putUrl(self, url, data):
		r = self.session.post(url, json=data)
		if r.status_code != 200:
			raise GitHubGetException(r)
		return r

	def getPRForRepo(self, repo, data):
		r = self.getUrl('{}/repos/{}/pulls'.format(GITHUB_API_ADRESS, repo), data)
		return r.json()

	def getFilesforPR(self, repo, number):
		r = self.getUrl('{}/repos/{}/pulls/{}/files'.format(GITHUB_API_ADRESS, repo, number), {})
		return r.json()

	def getIssuesAsPR(self, repo):
		r = self.getUrl('{}/repos/{}/issues'.format(GITHUB_API_ADRESS, repo), {})
		return [x for x in r.json() if "pull_request" in x]

	def addLabelsForIssue(self, repo, number, labels):
		r = self.putUrl('{}/repos/{}/issues/{}'.format(GITHUB_API_ADRESS, repo, number), {'labels' : labels})
		return r.json()

	def getLabelsForIssue(self, repo, number):
		r = self.getUrl('{}/repos/{}/issues/{}/labels'.format(GITHUB_API_ADRESS, repo, number), {})
		return [x for x in r.json()]
		
	def getUserRepositories(self):
		r = self.getUrl('{}/{}'.format(GITHUB_API_ADRESS, 'user/repos'), {})
		return [x['full_name'] for x in r.json()]