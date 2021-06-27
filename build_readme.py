#!/usr/bin/env python3
from pathlib import Path
import os
import requests
import json
from datetime import datetime

file_path = Path(__file__).parent.resolve() / 'README.md'
user = 'Ex-iT'
main_url = 'https://github.com'
api_url = 'https://api.github.com'
headers = { 'Accept': 'application/vnd.github.v3+json' }
params = { 'per_page': '10' }
content = '''<table>
    <tr>
        <td>
            <a href="https://stackoverflow.com/users/3351720/ex-it">
                <img alt="Profile for Ex-iT at Stack Overflow, Q&amp;A for professional and enthusiast programmers" src="https://stackoverflow.com/users/flair/3351720.png?theme=dark" />
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

<h2>GitHub activity</h2>

<pre>'''

if __name__ == '__main__':
    response = requests.get(f'{api_url}/users/{user}/events', headers=headers, params=params)
    json_data = json.loads(response.text)

    push_events = (event for event in json_data if event['type'] == 'PushEvent')
    for event in push_events:
        created_at = event['created_at'][:-1] # Strip the zero offset `Z`
        formatted_date = datetime.fromisoformat(created_at).strftime('%H:%M %d-%m-%Y')
        repo_name = event['repo']['name'];
        repo_label = repo_name.replace(f'{user}/', '') # Remove username and slash
        repo_url = f'{main_url}/{repo_name}'
        commit_message = event['payload']['commits'][0]['message'] # Always take the first message
        commit_sha = event['payload']['commits'][0]['sha']
        commit_url = f'{main_url}/{repo_name}/commit/{commit_sha}'

        content += f'''
    ┌──[{formatted_date}]─[<a href="{repo_url}">{repo_label}</a>]
    └───■ <a href="{commit_url}">{commit_message}</a><br />'''

    content += '''
</pre>'''

file_path.open('w').write(content)
