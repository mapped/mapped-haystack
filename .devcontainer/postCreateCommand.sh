#!/bin/bash

set -e

echo 'Setting up Poetry auth for private registry...'
poetry config http-basic.fury ${FURY_SECRET} NOPASS

echo 'Adding SSH key to access github repos...'
ssh-add
