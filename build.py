from datetime import datetime
import json
import requests

head = '''# Framework
'''
table = '''
## {} Framework

| Project Name | Stars | Forks | Description | Last Commit |
| ------------ | ----- | ----- | ----------- | ----------- |
'''
tail = '\n*Update Date: {}*'

repos = list()
api = 'https://api.github.com/repos/'

def main():
    token = get_token()
    with open('web_list.txt', 'r') as f:
        for url in f.readlines():
            url = url.strip()
            if url.startswith('https://github.com/'):
                print(url)
                path = '{}{}?access_token={}'.format(api, url[19:], token)
                r = requests.get(path)
                repo = json.loads(r.content)

                path = '{}{}/commits/{}?access_token={}'.format(api, url[19:], repo['default_branch'], token)
                r = requests.get(path)
                commit = json.loads(r.content)

                repo['last_commit_date'] = commit['commit']['committer']['date']
                repos.append(repo)

        repos.sort(key=lambda r: r['stargazers_count'], reverse=True)
        build(repos)

def get_token():
    with open('github_token.txt', 'r') as f:
        return f.read().strip()

def build(repos):
    with open('test.md', 'w') as f:
        f.write(head)
        f.write(table.format('Web'))
        for repo in repos:
            f.write('| [{}]({}) | {} | {} | {} | {} |\n'.format(repo['name'],
                                                                repo['html_url'],
                                                                repo['stargazers_count'],
                                                                repo['forks_count'],
                                                                repo['description'],
                                                                datetime.strptime(repo['last_commit_date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')))
        f.write(tail.format(datetime.now().strftime('%Y-%m-%dT%H:%M:%S%Z')))

if __name__ == '__main__':
    main()