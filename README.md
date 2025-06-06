# join-any-player-on-roblox
Quick writeup using Roblox's API to scan through servers and return a command to join the targeted player



## Features

- Join using player username / id
- Minimum player count field for faster searches
- Open source
- Works on any operating system, given it can run python and roblox


## Deployment

This was only tested on python 3.11.0, but should work for python versions >3.6

### Requirements

```bash
  pip install requests
```
Or
```bash
python -m pip install requests
```

Then download main.py in the repository, and run.
- User: Player's username / ID who you want to join
- Place ID: Game/Place ID that you want to search for the player in
- Minimum player count: Speeds up search by filtering out low player count servers




## Feedback

If you have any feedback or issues using, please reach out to me at nvyme on Discord, I'll be happy to help

