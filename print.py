import click


class Print:

	@staticmethod
	def printLabels(tp):
		tp.sort(key=lambda x:x[0])
		for i in tp:
			if i[1] == '=':
				click.echo("    " + click.style(i[1]) + " " + click.style(i[0]))
			elif i[1] == '+':
				click.echo("    " + click.style(i[1],fg='green') +  " " + click.style(i[0], fg='green'))
			elif i[1] == '-':
				click.echo("    " + click.style(i[1],fg='red') + " " + click.style(i[0], fg='red'))
			else:
				raise ValueError("Unexpected exception. Label fail:" + i[1])

	@staticmethod
	def printRepoOK(repo):
		click.echo(click.style('REPO', bold=True) +  " " + repo + " - " + click.style('OK', fg='green', bold=True))

	@staticmethod
	def printRepoFAIL(repo):
		click.echo(click.style('REPO', bold=True) + " " + repo + " - " + click.style('FAIL', fg='red', bold=True))

	@staticmethod
	def printPROK(pr):
		click.echo("  " + click.style('PR', bold=True) + " " + pr + " - " + click.style('OK', fg='green', bold=True))

	@staticmethod
	def printPRFAIL(pr):
		click.echo("  " + click.style('PR', bold=True) + " " + pr + " - " + click.style('FAIL', fg='red', bold=True))