#!/bin/bash -ue

# Copyright (C) 2010 Codership Oy
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston
# MA  02110-1301  USA.

# This is a reference script for rsync-based state snapshot tansfer

RSYNC_PID=
RSYNC_CONF=

cleanup_joiner()
{
    echo "Joiner cleanup:" >&2
set -x
    local PID=$(cat "$RSYNC_PID" 2>/dev/null || echo 0)
    [ "0" != "$PID" ] && kill $PID && sleep 0.5 && kill -9 $PID || :
set +x
    rm -rf "$RSYNC_CONF"
    rm -rf "$MAGIC_FILE"
    rm -rf "$RSYNC_PID"
}

check_pid()
{
    local pid_file=$1
    [ -r $pid_file ] && ps -p $(cat $pid_file) >/dev/null 2>&1
}

check_pid_and_port()
{
    local pid_file=$1
    local rsync_pid=$(cat $pid_file)
    local rsync_port=$2

    check_pid $pid_file && \
    netstat -anpt 2>/dev/null | \
    grep LISTEN | grep \:$rsync_port | grep $rsync_pid/rsync >/dev/null
}

ROLE=$1
ADDR=$2
AUTH=$3
DATA=$4
CONF=$5

MAGIC_FILE="$DATA/rsync_sst_complete"
rm -rf "$MAGIC_FILE"

if [ "$ROLE" = "donor" ]
then
    UUID=$6
    SEQNO=$7
    BYPASS=$8

    if [ $BYPASS -eq 0 ]
    then

        FLUSHED="$DATA/tables_flushed"
        rm -rf "$FLUSHED"

        # Use deltaxfer only for WAN
        inv=$(basename $0)
        [ "$inv" = "wsrep_sst_rsync_wan" ] && WHOLE_FILE_OPT="" \
                                           || WHOLE_FILE_OPT="--whole-file"

        echo "flush tables"

        # wait for tables flushed and state ID written to the file
        while [ ! -r "$FLUSHED" ] && ! grep -q ':' "$FLUSHED" >/dev/null 2>&1
        do
            sleep 0.2
        done

        STATE="$(cat $FLUSHED)"
        rm -rf "$FLUSHED"

        sync

        # Old filter - include everything except selected
        # FILTER=(--exclude '*.err' --exclude '*.pid' --exclude '*.sock' \
        #         --exclude '*.conf' --exclude core --exclude 'galera.*' \
        #         --exclude grastate.txt --exclude '*.pem' \
        #         --exclude '*.[0-9][0-9][0-9][0-9][0-9][0-9]' --exclude '*.index')

        # New filter - exclude everything except dirs (schemas) and innodb files
        FILTER=(-f '+ /ibdata*' -f '+ /ib_logfile*' -f '+ */' -f '-! */*')

        RC=0
        rsync --archive --no-times --ignore-times --inplace --delete --quiet \
              $WHOLE_FILE_OPT "${FILTER[@]}" "$DATA" rsync://$ADDR || RC=$?

        [ $RC -ne 0 ] && echo "rsync returned code $RC:" >> /dev/stderr

        case $RC in
        0)  RC=0   # Success
            ;;
        12) RC=71  # EPROTO
            echo "rsync server on the other end has incompatible protocol. " \
                 "Make sure you have the same version of rsync on all nodes."\
                 >> /dev/stderr
            ;;
        22) RC=12  # ENOMEM
            ;;
        *)  RC=255 # unknown error
            ;;
        esac

        [ $RC -ne 0 ] && exit $RC

    else # BYPASS
        STATE="$UUID:$SEQNO"
    fi

    echo "continue" # now server can resume updating data

    echo "$STATE" > "$MAGIC_FILE"
    rsync -aqc "$MAGIC_FILE" rsync://$ADDR

    echo "done $STATE"

elif [ "$ROLE" = "joiner" ]
then
    MYSQLD_PID=$6

    MODULE="rsync_sst"

    RSYNC_PID="$DATA/$MODULE.pid"

    if check_pid $RSYNC_PID
    then
        echo "rsync daemon already running."
        exit 114 # EALREADY
    fi
    rm -rf "$RSYNC_PID"

    RSYNC_PORT=$(echo $ADDR | awk -F ':' '{ print $2 }')
    if [ -z "$RSYNC_PORT" ]
    then
        RSYNC_PORT=4444
        ADDR="$(echo $ADDR | awk -F ':' '{ print $1 }'):$RSYNC_PORT"
    fi

    trap "exit 32" HUP PIPE
    trap "exit 3"  INT TERM
    trap cleanup_joiner EXIT

    MYUID=$(id -u)
    MYGID=$(id -g)
    RSYNC_CONF="$DATA/$MODULE.conf"

cat << EOF > "$RSYNC_CONF"
pid file = $RSYNC_PID
use chroot = no
[$MODULE]
	path = $DATA
	read only = no
	timeout = 300
	uid = $MYUID
	gid = $MYGID
EOF

#    rm -rf "$DATA"/ib_logfile* # we don't want old logs around

    # listen at all interfaces (for firewalled setups)
    rsync --daemon --port $RSYNC_PORT --config "$RSYNC_CONF"

    until check_pid_and_port $RSYNC_PID $RSYNC_PORT
    do
        sleep 0.2
    done

    echo "ready $ADDR/$MODULE"

    # wait for SST to complete by monitoring magic file
    while [ ! -r "$MAGIC_FILE" ] && check_pid "$RSYNC_PID" && \
          ps -p $MYSQLD_PID >/dev/null
    do
        sleep 1
    done

    if ! ps -p $MYSQLD_PID >/dev/null
    then
        echo "Parent mysqld process (PID:$MYSQLD_PID) terminated unexpectedly." >&2
        exit 32
    fi

    if [ -r "$MAGIC_FILE" ]
    then
        cat "$MAGIC_FILE" # output UUID:seqno
    else
        # this message should cause joiner to abort
        echo "rsync process ended without creating '$MAGIC_FILE'"
    fi

#    cleanup_joiner
else
    echo "Unrecognized role: $ROLE"
    exit 22 # EINVAL
fi

exit 0
