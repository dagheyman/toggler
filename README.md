# toggler
Alternative CLI for Toggl.

# Installation and setup

1. Clone repository

```
git clone https://github.com/dagheyman/toggler.git
```

2. Create a config file from template

```
cp conf.ini.template conf.ini
```

3. Edit conf.ini and add your API-token from Toggl.com (My Profile > API Token)

4. Install the requests module

```
pip install requests
```

5. Get your primary workspace id

```
./toggler.py workspaces
```

6. Edit conf.ini and add your primary workspace id.

7. Get the project id for being sick and add to the conf.ini file

```
./toggler.py projects
```

8. Done!
