# DEPRECATED 
## This project repo is no longer being maintained. For more information on code-gov repos, go to [GSA/code-gov](https://github.com/GSA/code-gov).

## Code.gov stats with Jupyter Notebook
Extract some stats for Code.gov using the Github GraphQL API

To view the [Jupyter Notebook](https://github.com/GSA/code-gov-stats-jupyter-notebook/blob/master/code-gov-github-stats.ipynb)

This repository is useful once you have all unique repository owners (AKA agencies for Code.gov) or if you use the [U.S. Federal Agency List](https://github.com/github/government.github.com/blob/gh-pages/_data/governments.yml#L621) compiled by Github.

The goal is to extract some basic repository information / stats from the Code.gov inventory. The data we are interested in is:

- Owner name
- Owner email
- Owner Github URL
- Repo's name with owner
- Repo's created at date
- Total fork count
- Is the repo a fork
- Total watchers
- Total stargazers
- Total pull requests
- Total issues

Eg.

```Python
{
 'created_at': '2012-01-26T17:30:51Z',
 'fork_count': 24,
 'is_fork': False,
 'issues': 50,
 'name_with_owner': 'cfpb/django-nudge',
 'owner_email': '',
 'owner_name': 'Consumer Financial Protection Bureau',
 'owner_url': 'https://github.com/cfpb',
 'pull_request': 13,
 'stargazers': 75,
 'watchers': 13
}
```

## Dependencies
### Github Dependencies

This Jupyter Notebook makes use of Github GraphQL API (API v4). If you are unfamiliar with GraphQL and/or Github API v4 we recommend reading:

- [GraphQL - Learn](http://graphql.org/learn/)
- [Github API v4](https://developer.github.com/v4/)

We also recommend taking a look at [Github's GraphQL API v4 Explorer](https://developer.github.com/v4/explorer/). With this tool you will be able to test the GraphQL queries that we use in this notebook.

### Python Dependencies

- Python 3.6+ - Should work with other versions of Python but has not been tested. To install Python please take a look at: [https://www.python.org/downloads/](https://www.python.org/downloads/)

#### Pipenv

We are using Pipenv in this project to manage our dependencies. To install __pipenv__ please take a look at: [https://pipenv.readthedocs.io/en/latest/#install-pipenv-today](https://pipenv.readthedocs.io/en/latest/#install-pipenv-today)

After installing pipenv you can install the dependencies by executing:

```bash
$ pipenv install
```

#### Manual Install

- Jupyter Notebook: To read up on how to install please visit [Jupyter.org - Install](http://jupyter.org/install)
- [graphcool/python-graphql-client](https://github.com/graphcool/python-graphql-client)
  ```
  pip install graphqlclient
  ```
- All other dependencies are found in the standard library

## Running the Notebook

### Pipenv

If you are using __pipenv__ you need to activate the virtual environment that was created. To activate this project's virtualenv, run `pipenv shell`.

```bash
$ pipenv shell
$ (your-virtualenv) jupyter notebook
```

To exit the virtualenv just execute the `exit` command.

Alternatively, you can run a command inside the virtualenv with `pipenv run`.

```bash
$ pipenv run jupyter notebook
```


## Contributing

Here’s how you can help contribute to this repo:

* Code of Conduct
  * Community is very important for us. We strive to be welcoming to all. To achive this we have drafted a [Code of Conduct](CODE_OF_CONDUCT.md), please take a look at it and leave us any feedback as a [Github issue](https://github.com/GSA/code-gov-stats-jupyter-notebook/issues)
* See something that's not quite right? Have a question or some feedback? Please let us know by [creating a Github Issue](https://github.com/GSA/code-gov-stats-jupyter-notebook/issues/new) on this repo.
* Want to be more hands on? We evaluate and accept Pull Requests!
