# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python3
#     language: python
#     name: Python3
# ---

# %%
import requests
from src.baduk import OGSGame

# %% [markdown]
# # Template Notebook

# %%
users = []
url = 'https://online-go.com/api/v1/players'
page = 0
while True:
    page += 1
    r = requests.get(url)
    data = r.json()
    users += data['results']
    print(page)

    if 'next' not in data:
        break

    url = data['next']

# %%
[u['username'] for u in users]

# %%
def find_ogs_user(search: str) -> dict:
    r = requests.get(
        'https://online-go.com/api/v1/ui/omniSearch',
        params={'q': search}
    )
    return r.json()['players']

# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
