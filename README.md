# list_unprotected_docker_engines

Scan account for servers running docker, which do not have Docker inspection
(ContainerSecure) enabled.

## What is this?

This is a tool which will use your Halo API credentials to scan your Halo
account for instances which are running Docker but do not have ContainerSecure enabled.

Using the `--fix` CLI argument will cause the script to enable Docker inspection for
all hosts running the `dockerd` process, which don't already have Docker inspection
enabled.

## Requirements

This tool requires Python 2.7.10+ and the CloudPassage SDK.

Install the CloudPassage SDK with `python2.7 -m pip install cloudpassage`


## Usage

Set these environment variables:

| Variable            | Purpose                                                 |
|---------------------|---------------------------------------------------------|
| HALO_API_KEY        | Auditor Halo API key (Administrator if using `--fix`)   |
| HALO_API_SECRET_KEY | API secret corresponding to HALO_API_KEY                |

Run:

Taking no corrective action:

`python2.7 ./application.py`

Enable Docker inspection on all hosts running `dockerd` process:

`python2.7 ./application.py --fix`

## Support

This is a community-supported tool (not officially supported by CloudPassage).
Use at your own risk. If you find a bug, please file an issue in Github.
