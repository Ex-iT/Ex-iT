#!/usr/bin/env python3
from pathlib import Path
import requests
import json
from datetime import datetime

file_path = Path(__file__).parent.resolve() / 'README.md'
user = 'Ex-iT'
main_url = 'https://github.com'
api_url = 'https://api.github.com'
headers = { 'Accept': 'application/vnd.github.v3+json' }
params = { 'per_page': '15' }
content = '''<table>
    <tr>
        <td>
            <a href="https://stackoverflow.com/users/3351720/ex-it">
                <img alt="Profile for Ex-iT at Stack Overflow, Q&amp;A for professional and enthusiast programmers" src="https://stackoverflow.com/users/flair/3351720.png?theme=dark" />
            </a>
        </td>
        <td>
            <a href="https://steamcommunity.com/id/Ex-iT">
                <img alt="Profile for Ex-iT at Steam" src="https://steamcommunity-a.akamaihd.net/public/shared/images/header/globalheader_logo.png" />
            </a>
        </td>
        <td rowspan="2">
            <a href="https://github.com/Ex-iT/">
                <img alt="Most Used Languages" src="https://github-readme-stats.vercel.app/api/top-langs/?username=ex-it&layout=compact&theme=algolia" />
            </a>
        </td>
    </tr>
    <tr>
        <td>
            <a href="https://app.hackthebox.eu/profile/169430">
                <img alt="Hack The Box :: MrBlonde" src="https://www.hackthebox.eu/badge/image/169430" />
            </a>
        </td>
        <td>
            <a href="https://tryhackme.com/p/MrBlonde/">
                <img alt="TryHackMe :: MrBlonde" src="https://tryhackme-badges.s3.amazonaws.com/MrBlonde.png" />
            </a>
        </td>
    </tr>
</table>

<h2>Recent activity</h2>

<pre>'''

def pushMessage(event):
    for event in (event for event in json_data if event['type'] == 'PushEvent'):
        created_at = datetime.strptime(event['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        formatted_date = created_at.strftime('%d-%m-%Y')
        repo_name = event['repo']['name'];
        repo_label = repo_name.replace(f'{user}/', '')
        repo_url = f'{main_url}/{repo_name}'

        commit_texts = f'''┌──[{formatted_date}]─[<a href="{repo_url}">{repo_label}</a>]'''

        for commit in event['payload']['commits']:
            commit_texts += commitMessage(commit, repo_name)

        return commit_texts + '<br /><br />'

def commitMessage(commit, repo_name):
    commit_url = f'''{main_url}/{repo_name}/commit/{commit['sha']}'''
    commit_message = commit['message']

    return f'''
└───■ <a href="{commit_url}">{commit_message}</a>'''


if __name__ == '__main__':
    response = requests.get(f'{api_url}/users/{user}/events/public', headers=headers, params=params)
    json_data = json.loads(response.text)

    for event in (event for event in json_data if event['type'] == 'PushEvent'):
        content += pushMessage(event)

    content += '''
</pre>'''

    file_path.open('w', encoding='utf-8').write(content)
