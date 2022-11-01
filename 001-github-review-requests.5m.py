#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# <xbar.title>Github PR</xbar.title>
# <xbar.desc>Display all PRs, assigned to me</xbar.desc>
# <xbar.author>Alex Vasylenko</xbar.author>
# <xbar.dependencies>python3</xbar.dependencies>
# <xbar.var>string(VAR_GITHUB_USERNAME=""): Your github username.</xbar.var>
# <xbar.var>string(VAR_GITHUB_TOKEN=""): Your github token with `repo` permission.</xbar.var>

import urllib.request
import json
import os
import sys

# need `repo` permission
USERNAME = os.environ.get("VAR_GITHUB_USERNAME")
TOKEN = os.environ.get("VAR_GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
query = """
{
  search(query: "is:open is:pr review-requested:{USERNAME} archived:false", type: ISSUE, first: 100) {
    issueCount
    edges {
      node {
        ... on PullRequest {
          number
          title
          createdAt
          mergedAt
          url
          changedFiles
          additions
          deletions
          repository {
            nameWithOwner
          }
        }
      }
    }
  }
}
""".replace("{USERNAME}", USERNAME)

if __name__ == "__main__":
    if not USERNAME or not TOKEN:
        print("Please configure with username and token | color=red")
        print("---")
        sys.exit()

    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers=headers
    )
    resp = urllib.request.urlopen(req)
    resp = json.loads(resp.read())
    data = resp["data"]["search"]["edges"]
    data = [
        {
            "title": x["node"]["title"],
            "url": x["node"]["url"],
            "createdAt": x["node"]["createdAt"],
            "repo": x["node"]["repository"]["nameWithOwner"]
            # additions, deletions, changedFiles
        }
        for x in data
    ]
    print(f"📃 {len(data)} | font=UbuntuMono-Bold")
    print("---")
    if data:
        print("---")
    for x in data:
        title = x['title'].replace('|', 'ǀ')
        color = "444444"
        if title.startswith("chore(deps):"):
            color = "999999"
        print(f"{title} | color=#{color} | size=12")
        print(f"{x['url']} | size=10 | href={x['url']}")
        print("---")

"""
📃 10
---
New feature request
https://github.com/anaconda/te-repo/pull/102
---
chore(deps): update dependency wagtail to v2.16.2 #1424
https://github.com/anaconda/bigbend-platform/pull/1424
---
"""



"""
📃 10 | font=UbuntuMono-Bold
---
New feature request | color=#444444 | size=12
https://github.com/anaconda/te-repo/pull/102 | size=10 | href=https://github.com/anaconda/te-repo/pull/102
---
chore(deps): update dependency wagtail to v2.16.2 #1424 | color=#999999 | size=12
https://github.com/anaconda/bigbend-platform/pull/1424 | size=10 | href=https://github.com/anaconda/bigbend-platform/pull/1424
---
"""
