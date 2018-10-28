# Filabel

Filabel is tool for labeling PRs at GitHub by globs. Fitlabel is command line and web app. For usage type `filabel --help`. Web app is in Flask.

Application is created for subject MI-PYT on FIT CTU.

Assigment repository: https://github.com/cvut/filabel


## Intalation
* Install from test version of PyPI: https://test.pypi.org/project/filabel-martilad/
* Install from repo `python setup.py install`

## Config 
Configuration files are in INI format. 
Examples for cli app: 
```Auth
[github]
# GitHub personal access token
token=<TOKEN>
# Secret for securing webhooks (optional)
secret=<WEBHOOK_SECRET>
```
```Labels
[labels]
frontend=
    */templates/*
    static/*
backend=
    logic/*
docs=
    *.md
    LICENSE
    docs/*
```
For web app is need export FILABEL_CONFIG variable with path to config files separate by ':'. In config files must be tags `[github]` and `[labels]`.