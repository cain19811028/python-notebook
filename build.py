from datetime import datetime
import json
import requests

head = '''# Framework
'''
table = '''
## {} Framework

| Project Name | Stars | Forks | Last Commit |
| ------------ | ----- | ----- | ----------- |
'''
tail = '\n*Update Date: {}*'

md = 'framework.md'
api = 'https://api.github.com/repos/'

def main():
    token = get_token()
    build_head()
    load(token, 'Web', 'web_list.txt')
    load(token, 'Crawler', 'crawler_list.txt')
    load(token, 'GraphQL', 'graphql_list.txt')
    build_tail()
    
def load(token, title, file):
    repos = list()
    with open(file, 'r') as f:
        for url in f.readlines():
            url = url.strip()
            print(url)
            if url.startswith('https://github.com/'):
                path = '{}{}?access_token={}'.format(api, url[19:], token)
                r = requests.get(path)
                repo = json.loads(r.content)

                path = '{}{}/commits/{}?access_token={}'.format(api, url[19:], repo['default_branch'], token)
                r = requests.get(path)
                commit = json.loads(r.content)

                repo['last_commit_date'] = commit['commit']['committer']['date']
                repos.append(repo)

        repos.sort(key=lambda r: r['stargazers_count'], reverse=True)
        build(title, repos)

def build(title, repos):
    with open(md, 'a') as f:
        f.write(table.format(title))
        for repo in repos:
            f.write('| [{}]({}) | {} | {} | {} |\n'.format(repo['name'],
                                                           repo['html_url'],
                                                           repo['stargazers_count'],
                                                           repo['forks_count'],
                                                           datetime.strptime(repo['last_commit_date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')))

def build_head():
    with open(md, 'w') as f:
        f.write(head)

def build_tail():
    with open(md, 'a') as f:
        f.write(tail.format(datetime.now().strftime('%Y-%m-%dT%H:%M:%S%Z')))

def get_token():
    with open('github_token.txt', 'r') as f:
        return f.read().strip()

if __name__ == '__main__':
    main()
