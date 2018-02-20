# Code.gov stats with Jupyter Notebook
Extract some stats for Code.gov using the Github GraphQL API

This repository is useful once you have all unique repository owners (AKA agencies for Code.gov).

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

# Dependencies
## Github Dependencies

This Jupyter Notebook makes use of Github GraphQL API (API v4). If you are unfamiliar with GraphQL and/or Github API v4 we recomend reading:

- [GraphQL - Learn](http://graphql.org/learn/)
- [Github API v4](https://developer.github.com/v4/)

We also recommend taking a look at [Github's GraphQL API v4 Explorer](https://developer.github.com/v4/explorer/). With tool you will be able to test the GraphQL queries that we use in this notebook.

## Python Dependencies
- Jupyter Notebook: To read up on how to install please visit [Jupyter.org - Install](http://jupyter.org/install)
- [graphcool/python-graphql-client](https://github.com/graphcool/python-graphql-client)
  ```
  pip install graphqlclient
  ```
- All other dependencies are found in the standard library

# Contributing

See something that's not quite right? Have a question or some feedback? Please let us know by [creating a Github Issue](https://github.com/GSA/code-gov-stats-jupyter-notebook/issues/new) on this repo.

Want to be more hands on? We evaluate and accept Pull Requests!
