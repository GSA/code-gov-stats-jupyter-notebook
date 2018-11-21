from graphqlclient import GraphQLClient
import json
import csv
from datetime import datetime
import time
import requests
from dotenv import DotEnv
import re
import logging


def get_gh_query(repo_owner, repo_name, gh_cursor=None):
    str_cursor = 'null'
    if gh_cursor:
        str_cursor = f'"{gh_cursor}"'

    query = '''
        query {
            repository(owner: "%s", name: "%s") {
                owner{
                    ... on Organization {
                        name
                        url
                        email
                        login
                    }
                    ... on User {
                        name
                        url
                        email
                        login
                    }
                }
                issues(first: 100, labels: ["help wanted", "code.gov"], after: %s) {
                    nodes {
                        title
                        bodyHTML
                        url
                        state
                        createdAt
                        lastEditedAt
                        publishedAt
                        updatedAt
                        labels(first:20) {
                            nodes {
                                name
                            }
                        }
                        locked
                        participants {
                            totalCount
                        }
                    }
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                }
            }
            rateLimit {
                limit
                cost
                remaining
                resetAt
            }
        }
    '''
    return query % (repo_owner, repo_name, str_cursor)

def get_gh_issues(gh_api_token, repo_owner, repo_name, gh_cursor=None):
    client = GraphQLClient('https://api.github.com/graphql')
    client.inject_token(f'token {gh_api_token}')

    query = get_gh_query(repo_owner, repo_name, gh_cursor)    
    response = client.execute(query)
    json_response = json.loads(response)

    if json_response is None:
        logging.error(f'[ERROR] while getting issues for {repo_owner}/{repo_name}. Error: Not Found')
        return []
    if 'errors' in json_response:
        logging.error(f'[ERROR] while getting issues for {repo_owner}/{repo_name}. Error: {json_response}')
        return []
    
    issues = json_response['data']['repository']['issues']
    repository_owner_data = json_response['data']['repository']['owner']
    return_issues = []

    if issues['nodes']:
        for issue in issues['nodes']:
            return_issues.append({
                'repo_name': repo_name,
                'repo_owner_name': repository_owner_data['name'],
                'repo_owner_email': repository_owner_data['email'],
                'repo_owner_user_name': repository_owner_data['login'],
                'repo_owner_profile_url': repository_owner_data['url'],
                'title': issue['title'],
                'bodyHTML': issue['bodyHTML'],
                'url': issue['url'],
                'state': issue['state'],
                'createdAt': issue['createdAt'],
                'lastEditedAt': issue['lastEditedAt'],
                'publishedAt': issue['publishedAt'],
                'updatedAt': issue['updatedAt'],
                'labels': [node['name'] for node in issue['labels']['nodes']],
                'is_locked': issue['locked'],
                'total_participants': issue['participants']['totalCount'],
            })

        hasNext = issues['pageInfo']['hasNextPage']

        if hasNext:
            cursor = issues['pageInfo']['endCursor']
            remaining = json_response['data']['rateLimit']['remaining']
            limit = json_response['data']['rateLimit']['limit']
            reset_at = json_response['data']['rateLimit']['resetAt']

            percent_remaining = remaining / limit
            if percent_remaining < 0.15:
                reset_at = datetime.strptime(reset_at, '%Y-%m-%dT%H:%M:%SZ')
                current_time = datetime.now()
                time_diff = current_time - reset_at
                seconds = time_diff.total_seconds()
                time.sleep(seconds)
            else:
                time.sleep(2)
            
            return return_issues.extend(get_gh_issues(gh_api_token, repo_owner, repo_name, cursor))
        else:
            return return_issues
    else:
        logging.debug(f'No issues found for {repo_owner}/{repo_name}')
        return []

def get_repo_owner_and_name(gh_url):
    if re.match(r'https:\/\/github.com', gh_url):
        url_split = gh_url.split('/')

        return url_split[-2], url_split[-1]
    
    if re.match(r'git@github.com', gh_url):
        url_split = gh_url.split(':')

        owner_and_repo = url_split[-1].split('/')

        return owner_and_repo[0], owner_and_repo[1]

def getReposFromCodeGov(api_token):
    logging.info('Getting repos from Code.gov')
    headers = {
        'X-API-KEY': api_token,
        'Content-Type': 'application/json',
    }
    response = requests.get('https://api.code.gov/repos?permissions.usageType=openSource&size=5000', headers=headers)
    json_response = response.json()

    return json_response['repos']

def main(environment):
    logging.info('Entered main function')
    repos = getReposFromCodeGov(environment.get('CODE_GOV_API_TOKEN'))

    github_repos = list(filter(lambda repo: re.match(r'(https:\/\/||git@)github.com', repo['repositoryURL']), repos))
    
    github_issues = []
    logging.info('Getting Github Issues')
    for repo in github_repos:
        repo_url = repo['repositoryURL']

        repo_owner, repo_name = get_repo_owner_and_name(repo_url)
        github_issues.extend(get_gh_issues(environment.get('GITHUB_TOKEN'), repo_owner, repo_name))

    logging.info('Creating issues csv file')
    with open('issues.csv', 'a') as issues_csv:
        fields = [
            'repo_name',
            'repo_owner_name',
            'repo_owner_email',
            'repo_owner_user_name',
            'repo_owner_profile_url',
            'title',
            'bodyHTML',
            'url',
            'state',
            'createdAt',
            'lastEditedAt',
            'publishedAt',
            'updatedAt',
            'labels',
            'is_locked',
            'total_participants',
        ]
        writer = csv.DictWriter(issues_csv, fieldnames=fields)
        writer.writeheader()
        writer.writerows(github_issues)

if __name__ == '__main__':
    environment = DotEnv()

    start_time = datetime.now()
    logging.info(f'Script started: {start_time}')
    
    main(environment)
    
    finish_time = datetime.now()
    delta = finish_time - start_time
    
    logging.info(f'Script finished: {finish_time}')
    logging.info(f'Script took {delta.seconds} seconds')
  