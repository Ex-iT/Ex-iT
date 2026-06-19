#!/usr/bin/env python3
import os
from pathlib import Path
import requests
from datetime import datetime

file_path = Path(__file__).parent.resolve() / "README.md"
user = "Ex-iT"
main_url = "https://github.com"
api_url = "https://api.github.com"
session = requests.Session()
session.headers.update({"Accept": "application/vnd.github.v3+json"})
token = os.getenv("GITHUB_TOKEN")
if token:
    session.headers["Authorization"] = f"Bearer {token}"
timeout = 15
params = {"per_page": "15"}
content = """<table>
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
                <img alt="Most Used Languages" src="images/top-langs.svg" />
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

<pre>"""


def get_commit_message(repo_name, sha):
    response = session.get(
        f"{api_url}/repos/{repo_name}/commits/{sha}",
        timeout=timeout
    )
    if response.status_code == 200:
        return response.json()["commit"]["message"].split("\n")[0]
    return "New commit"


def pushMessage(event):
    created_at = datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    formatted_date = created_at.strftime("%d-%m-%Y")
    repo_name = event["repo"]["name"]
    repo_label = repo_name.replace(f"{user}/", "")
    repo_url = f"{main_url}/{repo_name}"
    head = event["payload"]["head"]
    commit_url = f"""{main_url}/{repo_name}/commit/{head}"""
    commit_message = get_commit_message(repo_name, head)

    if commit_message.startswith("Merge"):
        return ""

    payload_text = f"""
[+]─[{formatted_date}]▶[<a href="{repo_url}">{repo_label}</a>]
 └─ <a href="{commit_url}">{commit_message}</a>"""
    return payload_text


if __name__ == "__main__":
    response = session.get(
        f"{api_url}/users/{user}/events/public",
        params=params,
        timeout=timeout
    )
    json_data = response.json()

    if not isinstance(json_data, list) or len(json_data) == 0:
        content += f"""
[-] No public recent activity"""
    else:
        for event in (event for event in json_data if event["type"] == "PushEvent"):
            content += pushMessage(event)

    content += """
</pre>"""

    file_path.open("w", encoding="utf-8").write(content)
