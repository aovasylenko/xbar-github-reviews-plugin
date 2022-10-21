# xbar-onduty-plugin

## Setup

* Install [xbar](https://github.com/matryer/xbar/releases) by downloading the latest release `.dmg` and dragging it to your applications folder when prompted, or use [homebrew](https://brew.sh/)
```
brew install --cask xbar
```

* Once `xbar` is installed, install the plugin from the repo source.
```
cd ~/REPO_ROOT
git pull
make install
```

* Click on `xbar` again and click 'Refresh' to reload the plugins.
1. You should see the bar change from saying `xbar` to a warning message about the plugin.  Click on the message and select 'Step 1' to generate a new GitHub access token.
<img width="469" alt="image" src="https://user-images.githubusercontent.com/4342684/197207685-e33f3360-1674-47b8-84f6-9f6a26525a1d.png">

* Accept the default scopes (it should be `repo`) and copy the token to clipboard.
* Click on 'Step 2' in the plugin instructions to enter your secret into the config file.  Insert the secret after all the stars to obscure the token from view in the UI.  All stars will be stripped from the token before it is used.
* Click on 'Step 3' to reload the plugin.
