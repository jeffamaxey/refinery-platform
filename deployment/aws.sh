#!/bin/sh

set -x

# This script is intended to be executed on AWS instance after
# the bootstraph.sh script. The bootstrap.sh script is common
# to both Vagrant and AWS. Both bootstrap.sh and aws.sh (this
# script) are supplied via cloudinit userdata.

# Normally supplied as input, but use a default if not.
GIT_BRANCH=${GIT_BRANCH:-develop}

/usr/bin/apt-get -q -y install htop
/usr/bin/apt-get -q -y install awscli jq postgresql-client-9.3

mkdir /srv/refinery-platform
chown ubuntu:ubuntu /srv/refinery-platform
sudo su -c 'git clone -b '"$GIT_BRANCH"' https://github.com/parklab/refinery-platform.git /srv/refinery-platform' ubuntu

cd /srv/refinery-platform/deployment

# Discover IP endpoint for our PostgreSQL RDS, and place it in
# environment variables for puppet/facter to use
bin/aws-rds-endpoint db20160111 > /home/ubuntu/rds
export FACTER_RDS_HOST=$(jq -r .Address /home/ubuntu/rds)
export FACTER_RDS_PORT=$(jq -r .Port /home/ubuntu/rds)

# Create RDS user and database here, instead of using puppet
# (because drj cou;dn't work out how to do it in puppet)
bin/ensure-postgresql-role
bin/ensure-postgresql-database

sudo su -c '/usr/local/bin/librarian-puppet install' ubuntu

/usr/bin/puppet apply --modulepath=/srv/refinery-platform/deployment/modules /srv/refinery-platform/deployment/manifests/aws.pp
