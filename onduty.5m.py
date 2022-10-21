#!/usr/bin/env python3

# <xbar.title>DevOps OnDuty</xbar.title>
# <xbar.desc>Display detected onduty work.</xbar.desc>
# <xbar.author>Carl Anderson</xbar.author>
# <xbar.dependencies>python3</xbar.dependencies>
# <xbar.var>string(VAR_ONDUTY_TEAM_NAME="anaconda/anaconda-devops-onduty"): The GitHub team name of the onduty rotation.</xbar.var>
# <xbar.var>string(VAR_ONDUTY_USER_NAME="@me"): The GitHub username of the onduty assignee.</xbar.var>
# <xbar.var>string(VAR_GITHUB_TOKEN=""): SECRET - Your GitHub API token.</xbar.var>


import json
import os
import urllib.request
from datetime import datetime, timezone

TEAM_NAME = os.environ.get("VAR_ONDUTY_TEAM_NAME")
USER_NAME = os.environ.get("VAR_ONDUTY_USER_NAME")

FILTER = " ".join(f"""
    team-review-requested:{TEAM_NAME}
    user-review-requested:{USER_NAME}
    is:open
    is:pr
    draft:false
    archived:false
""".split())


def xbar(items):
    for row in items.strip().split('\n'):
        if row.strip():
            print(row.strip())


def print_shortcuts():
    xbar("""
        -- Shortcuts
        ---- DataDog | href=https://app.datadoghq.com/apm/home?env=prod
        ---- #ask-infrastructure | href=https://anaconda.slack.com/archives/C010ZDG1ACB
        ---- New IT ticket | href=https://it.anaconda.com/
        ---- Okta | href=https://anaconda.okta.com/app/UserHome
    """)

    
def print_needs_configuration():
    xbar("""
        :warning: Needs configuration!
        ---
        Step 1 - Click here to generate a token | href=https://github.com/settings/tokens/new?description=xbar&scopes=repo
        Step 2 - Click here to insert and save token into the config. | shell=/usr/bin/open | param1='{__file__}.vars.json'
        Step 3 - Reload after saving your token. | href=xbar://app.xbarapp.com/refreshAllPlugins
        ---
    """)


def get_token(name):
    return os.environ.get(name).lstrip('*')


def get_prs():
    query = """
    {
        search(query: "{FILTER}", type: ISSUE, first: 100)
        {
            issueCount
            edges {
            node {
                ... on PullRequest {
                title
                url
                createdAt
                }
            }
            }
        }
    }
    """.replace("{FILTER}", FILTER)

    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={
          "Authorization": f"Bearer {get_token('VAR_GITHUB_TOKEN')}",
          "Content-Type": "application/json"
      }
    )
    resp = urllib.request.urlopen(req)
    resp = json.loads(resp.read())
    data = resp["data"]["search"]["edges"]
    return [
        {
            "title": x["node"]["title"],
            "createdAt": x["node"]["createdAt"],
            "url": x["node"]["url"],
        }
        for x in data
    ]
    

# Lifted and shifted from: https://stackoverflow.com/a/1551394/280708
def ago_color(time):
    now = datetime.now(timezone.utc)
    diff = now - time
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff == 0:
        if second_diff < 10:
            return "just now", "purple"
        if second_diff < 60:
            return str(second_diff) + " seconds ago", "purple"
        if second_diff < 120:
            return "a minute ago", "red"
        if second_diff < 3600:
            return str(second_diff // 60) + " minutes ago", "orange"
        if second_diff < 7200:
            return "an hour ago", "orange"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago", "yellow"
    if day_diff == 1:
        return "Yesterday", "green"
    if day_diff < 7:
        return str(day_diff) + " days ago", "blue"
    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago", "purple"
    if day_diff < 365:
        return str(day_diff // 30) + " months ago", "black"
    return str(day_diff // 365) + " years ago", "black"


def main():
    try:
        data = get_prs()
    except Exception:
        print_needs_configuration()
        return

    print(f":fire: {len(data)}")
    print("---")
    print("Reload config | refresh=true")
    print("devops-onduty")
    print_shortcuts()
    print("-- PRs waiting review: " + str(len(data)))
    for x in data:
        ago, color = ago_color(datetime.fromisoformat(
            x["createdAt"].replace("Z", "+00:00")
        ))
        print(f"----{ago:>15} - {x['title']} | href={x['url']} | color={color} | size=12 | font=Courier-Bold | trim=false")


if __name__ == "__main__":
    main()