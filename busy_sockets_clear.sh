sudo sysctl -w net.ipv4.tcp_fin_timeout=5

# Source: https://serverfault.com/a/637203

# record what tcp_max_orphans's current value
original_value=$(cat /proc/sys/net/ipv4/tcp_max_orphans)

#set the tcp_max_orphans to 0 temporarily
echo 0 > /proc/sys/net/ipv4/tcp_max_orphans

# watch /var/log/messages
# it will split out "kernel: TCP: too many of orphaned sockets"
# it won't take long for the connections to be killed

# restore the value of tcp_max_orphans whatever it was before.
echo $original_value > /proc/sys/net/ipv4/tcp_max_orphans

# verify with
netstat -an|grep FIN_WAIT1