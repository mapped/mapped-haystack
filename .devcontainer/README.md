# Why devcontainers?
Ivan is tired to adjusting python and poetry versions for every python repo while fixing CVEs.
Devcontainer perfecty matches all the versions.

# How to configure host machine?
Add 3 env var variables to your `~/.bash_profile` or `~/.zprofile` (if using zsh on Mac). I using both consider doing `source ~/.bash_profile` inside of `~/.zprofile` to reduce duplication.

Env vars:
```bash
export FURY_SECRET=<your personal key from gemfury to access private python packages>
export DEV_CONTAINER_SSH_KEY_PATH=~/.ssh/<ssh key on host machine>
export DEV_CONTAINER_SSH_KNOWN_HOSTS_PATH=~/.ssh/known_hosts
```