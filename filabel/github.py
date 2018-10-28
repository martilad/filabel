import requests
import os


class GitHub:
    """
    This class can communicate with the GitHub API
    just give it a token and go.
    """
    API = 'https://api.github.com'

    def __init__(self, token, session=None):
        """
        token: GitHub token
        session: optional requests session
        """
        self.token = token
        self.session = session or requests.Session()
        self.session.headers = {'User-Agent': 'filabel'}
        self.session.auth = self._token_auth

    def _token_auth(self, req):
        """
        This alters all our outgoing requests
        """
        req.headers['Authorization'] = 'token ' + self.token
        return req

    def _paginated_json_get(self, url, params=None):
        r = self.session.get(url, params=params)
        r.raise_for_status()
        json = r.json()
        if 'next' in r.links and 'url' in r.links['next']:
            json += self._paginated_json_get(r.links['next']['url'], params)
        return json

    def user(self):
        """
        Get current user authenticated by token
        """
        return self._paginated_json_get(f'{self.API}/user')

    def pull_requests(self, owner, repo, state='open', base=None):
        """
        Get all Pull Requests of a repo

        owner: GtiHub user or org
        repo: repo name
        state: open, closed, all
        base: optional branch the PRs are open for
        """
        params = {'state': state}
        if base is not None:
            params['base'] = base
        url = f'{self.API}/repos/{owner}/{repo}/pulls'
        return self._paginated_json_get(url, params)

    def pr_files(self, owner, repo, number):
        """
        Get files of one Pull Request

        owner: GtiHub user or org
        repo: repo name
        number: PR number/id
        """
        url = f'{self.API}/repos/{owner}/{repo}/pulls/{number}/files'
        return self._paginated_json_get(url)

    def pr_filenames(self, owner, repo, number):
        """
        Get filenames of one Pull Request. A generator.

        owner: GtiHub user or org
        repo: repo name
        number: PR number/id
        """
        return (f['filename'] for f in self.pr_files(owner, repo, number))

    def reset_labels(self, owner, repo, number, labels):
        """
        Set's labels for Pull Request. Replaces all existing lables.

        owner: GtiHub user or org
        repo: repo name
        lables: all lables this PR will have
        """
        url = f'{self.API}/repos/{owner}/{repo}/issues/{number}'
        r = self.session.patch(url, json={'labels': labels})
        r.raise_for_status()
        return r.json()['labels']