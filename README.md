# toggler
Script to automate some time reporting in Toggl.

# Installation and setup

Clone repository

```
git clone https://github.com/dagheyman/toggler.git
```

Create a config file from template

```
cp conf.ini.template conf.ini
```

Edit conf.ini and add your API-token from Toggl.com (My Profile > API Token)

Install the requests module

```
pip install requests
```

Get your primary workspace id

```
./toggler.py workspaces
```

Edit conf.ini and add your primary workspace id.

Get the project id for being sick and add to the conf.ini file

```
./toggler.py projects
```

Done!
