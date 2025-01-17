import flask
import configparser
import os
import hashlib
import hmac
import jinja2
from filabel.cli import parse_labels, Filabel
from filabel.github import GitHub


def webhook_verify_signature(payload, signature, secret, encoding='utf-8'):
    """
    Verify the payload with given signature against given secret

    see https://developer.github.com/webhooks/securing/

    payload: received data as dict
    signature: included SHA1 signature of payload (with secret)
    secret: secret to verify signature
    encoding: encoding for secret (optional)
    """
    h = hmac.new(secret.encode(encoding), payload, hashlib.sha1)
    return hmac.compare_digest('sha1=' + h.hexdigest(), signature)



def process_webhook_pr(payload):
    """
    Process webhook event "pull_request"

    payload: event payload
    """
    filabel = flask.current_app.config['filabel']
    try:
        action = payload['action']
        pull_request = payload['pull_request']
        pr_number = payload['number']
        pr_url = pull_request['url'].split('/')  # no repo field in payload!
        owner = pr_url[-4]
        repo = pr_url[-3]
        reposlug = '{}/{}'.format(owner, repo)

        if action not in ('opened', 'synchronize'):
            flask.current_app.logger.info(
                'Action {} from {}#{} skipped'.format(action, reposlug, pr_number)
            )
            return 'Accepted but action not processed', 202

        filabel.run_pr(owner, repo, pull_request)

        flask.current_app.logger.info(
            'Action {} from {}#{} processed'.format(action, reposlug, pr_number)
        )
        return 'PR successfully filabeled', 200
    except (KeyError, IndexError):
        flask.current_app.logger.info(
            'Incorrect data entity from IP {}'.format(flask.request.remote_addr)
        )
        flask.abort(422, 'Missing required payload fields')
    except Exception:
        flask.current_app.logger.error(
            'Error occurred while processing {}#{}'.format(repo, pr_number)
        )
        flask.abort(500, 'Processing PR error')


def process_webhook_ping(payload):
    """
    Process webhook event "ping"

    payload: event payload
    """
    try:
        repo = payload['repository']['full_name']
        hook_id = payload['hook_id']
        flask.current_app.logger.info(
            'Accepting PING from {}#WH-{}'.format(repo, hook_id)
        )
        return 'PONG', 200
    except KeyError:
        flask.current_app.logger.info(
            'Incorrect data entity from IP {}'.format(flask.request.remote_addr)
        )
        flask.abort(422, 'Missing payload contents')


webhook_processors = {
    'pull_request': process_webhook_pr,
    'ping': process_webhook_ping
}

def create_app():
    """
    Prepare Filabel Flask application listening to GitHub webhooks
    """
    app = flask.Flask(__name__)
    cfg = configparser.ConfigParser()
    """if 'FILABEL_CONFIG' not in os.environ:
        app.logger.critical('Config not supplied by envvar FILABEL_CONFIG')
        exit(1)"""
    app.cfg = cfg
    config_filename=os.getenv('FILABEL_CONFIG', None)
    if config_filename != None:
        configs = os.environ['FILABEL_CONFIG'].split(':')
        cfg.read(configs)

    return app


# Importing, FILABEL_CONFIG must be set!
app = create_app()



@app.before_first_request
def finalize_setup():
    if 'labels' not in app.cfg:
        app.logger.critical('Labels configuration not supplied!', err=True)
        exit(1)
    try:
        app.config['labels'] = parse_labels(app.cfg)
    except Exception:
        app.logger.critical('Labels configuration not usable!', err=True)
        exit(1)

    try:
        app.config['github_token'] = app.cfg.get('github', 'token')
        app.config['secret'] = app.cfg.get('github', 'secret', fallback=None)
    except Exception:
        app.logger.critical('Auth configuration not usable!', err=True)
        exit(1)

    filabel = Filabel(app.config['github_token'], app.config['labels'])

    try:
        app.config['github_user'] = filabel.github.user()
        app.config['filabel'] = filabel
    except Exception:
        app.logger.critical('Bad token: could not get GitHub user!', err=True)
        exit(1)


@app.template_filter('github_user_link')
def github_user_link_filter(github_user):
    """
    Template filter for HTML link to GitHub profile

    github_user: User data from GitHub API
    """
    url = flask.escape(github_user['html_url'])
    login = flask.escape(github_user['login'])
    return jinja2.Markup('<a href="{}" target="_blank">{}</a>'.format(url, login))

@app.route('/', methods=['GET'])
def index():
    """
    Landing info page
    """
    return flask.render_template(
        'infopage.html',
        labels=flask.current_app.config['labels'],
        user=flask.current_app.config['github_user']
    )

@app.route('/', methods=['POST'])
def webhook_listener():
    """
    Webhook listener endpoint
    """
    signature = flask.request.headers.get('X-Hub-Signature', '')
    event = flask.request.headers.get('X-GitHub-Event', '')
    payload = flask.request.get_json()

    secret = flask.current_app.config['secret']

    if secret is not None and not webhook_verify_signature(
            flask.request.data, signature, secret
    ):
        flask.current_app.logger.warning(
            'Attempt with bad secret from IP {}'.format(flask.request.remote_addr)
        )
        flask.abort(401, 'Bad webhook secret')

    if event not in webhook_processors:
        supported = ', '.join(webhook_processors.keys())
        flask.abort(400, 'Event not supported (supported: {})'.format(supported))

    return webhook_processors[event](payload)