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
		lists = []
		page = 1
		while True:
			data['page'] = page
			r = self.session.get(url, params=data)
			if r.status_code != 200:
				raise GitHubGetException(r)
			r = [x for x in r.json()]
			if len(r) == 0:
				return lists
			lists.extend(r)
			page+=1
		return lists

	def putUrl(self, url, data):
		r = self.session.post(url, json=data)
		if r.status_code != 200:
			raise GitHubGetException(r)
		return r

	def getPRForRepo(self, repo, data):
		return self.getUrl('{}/repos/{}/pulls'.format(GITHUB_API_ADRESS, repo), data)

	def getFilesforPR(self, repo, number):
		return self.getUrl('{}/repos/{}/pulls/{}/files'.format(GITHUB_API_ADRESS, repo, number), {})

	def getIssuesAsPR(self, repo, data):
		return [x for x in self.getUrl('{}/repos/{}/issues'.format(GITHUB_API_ADRESS, repo), data) if "pull_request" in x]

	def addLabelsForIssue(self, repo, number, labels):
		return self.putUrl('{}/repos/{}/issues/{}'.format(GITHUB_API_ADRESS, repo, number), {'labels' : labels})

	def getLabelsForIssue(self, repo, number):
		return self.getUrl('{}/repos/{}/issues/{}/labels'.format(GITHUB_API_ADRESS, repo, number), {})
		
	def getUserRepositories(self):
		return [x['full_name'] for x in self.getUrl('{}/{}'.format(GITHUB_API_ADRESS, 'user/repos'), {})]