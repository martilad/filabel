import click


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
	"""CLI tool for filename-pattern-based labeling of GitHub PRs"""
	...

if __name__ == '__main__':
	filabel()
