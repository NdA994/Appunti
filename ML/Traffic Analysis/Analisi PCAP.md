**REQUIREMENTS:** è necessario avere tshark e pv installato.
```
sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt install pv tshark -y
```

------------------------------------------------------------------------

## Split pcap
Divide i pcap in chunk più piccoli in base al numero di pacchetti forniti in input

```bash
editcap -c <chop_len> input.pcap outfile
```

comando di esempio:

```bash
editcap -c 1000000 input.pcap chunk_
```

------------------------------------------------------------------------

## Show stats
Mostrare le statistiche per ogni protocollo

```bash
tshark -r input.pcap -q -z io,phs
```

Mostrare le statistiche per IPv4

```bash
tshark -r chunk__00001_20191206030545 -Y ip -T fields -e ip.proto | sort | uniq -c | sort -nr
```

Mostrare le statistiche per IPv6

```
tshark -r chunk__00001_20191206030545 -Y ipv6 -T fields -e ipv6.nxt \
| sort | uniq -c | sort -nr
```

Per vedere a che tipo di protocollo fanno riferimento i seguenti protocolli, fare riferimento ai [protocol numbers di IANA](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)

------------------------------------------------------------------------

## Extract biflows

### Divide pcap 

Separate il pcap in differenti flussi in base al livello 

#### Estrazione campi L2 

```bash
tshark -r input.pcap -n -Y "not ip and not ipv6" -w lvl2_l2_non_ip.pcap
```

#### IPv4 + IPv6, esclusi TCP e UDP 

```bash
tshark -r input.pcap -n -Y "(ip or ipv6) and not tcp and not udp" -w lvl3_l3_ip_only.pcap
```

#### TCP/UDP su IPv4, escluso DHCPv4 e DHCPv6

```bash
tshark -r input.pcap -n -Y "ip && not (udp.port == 67 or udp.port == 68 or udp.port == 546 or udp.port == 547)" -w lvl4_ipv4_no_dhcp.pcap
```

#### TCP/UDP su IPv6, escluso DHCPv4 e DHCPv6

```bash
tshark -r input.pcap -n -Y "ipv6 && not (udp.port == 67 or udp.port == 68 or udp.port == 546 or udp.port == 547)" -w lvl4_ipv6_no_dhcp.pcap
```

------------------------------------------------------------------------

### Estarre le connessioni

Per separare in biflussi, inanzitutto conviene estrapolare solamente le informazioni utili e rilevanti dal pcap, quindi quelli che hanno IP (questo è per IPv4)

```bash
tshark -r input.pcap -T fields -e frame.number -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e ip.proto -E separator=, > packets.csv
```

```pv input.pcap | tshark -r - -T fields -Y ip -e frame.number -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -e ip.proto -E separator=, > packets.csv
```



Normalizzare  (da fare in pandas)

Per IPv6 invece si dovrà effettuare il seguente comando

```
awk -F',' '
{
  src_ip=$2; dst_ip=$3;

  src_port=($4!="")?$4:$6;
  dst_port=($5!="")?$5:$7;

  proto=$8;

  if (src_port=="" || dst_port=="") next;

  # build endpoint identifiers
  ep1 = src_ip ":" src_port
  ep2 = dst_ip ":" dst_port

  # canonical ordering (bidirectional normalization)
  if (ep1 <= ep2) {
    print $1 "," src_ip "," dst_ip "," src_port "," dst_port "," proto
  } else {
    print $1 "," dst_ip "," src_ip "," dst_port "," src_port "," proto
  }
}' packets.csv > packets_norm.csv
```

```
cut -d',' -f2-6 packets_norm.csv | sort | uniq > flows.txt
```

```
while IFS=',' read src_ip dst_ip src_port dst_port proto; do
  proto_filter=""

  [ "$proto" = "6" ] && proto_filter="tcp"
  [ "$proto" = "17" ] && proto_filter="udp"

  # skip unsupported protocols
  [ -z "$proto_filter" ] && continue

  fname="flow_${src_ip}_${src_port}__${dst_ip}_${dst_port}_${proto_filter}.pcap"

  pv chunk__00000_20191206030504 | tshark -r - -n -w "$fname" \
    -Y "$proto_filter && (
          (ip.src==$src_ip && ip.dst==$dst_ip &&
           $proto_filter.srcport==$src_port &&
           $proto_filter.dstport==$dst_port)
          ||
          (ip.src==$dst_ip && ip.dst==$src_ip &&
           $proto_filter.srcport==$dst_port &&
           $proto_filter.dstport==$src_port)
        )"
done < flows.txt
```

```
parallel -j 8 < split_script.sh

```


------------------------------------------------------------------------

**NOTA:** per vedere lo stato di esecuzione del comando è possibile utilizzare pv, il quale monitora il prograsso attraverso il passaggio dei dati da una pipe (nel nostro caso stdin)

```bash
pv input.pcap | tshark -r - -q -z io,phs
```
 
 monitor the progress of data through a pipe

```

total=$(wc -l < flows.txt)
count=0
logfile="progress.log"

: > "$logfile"   # svuota il file all’inizio

while IFS=',' read -r src_ip dst_ip src_port dst_port proto; do
  count=$((count+1))

  printf "Flow progress: %d/%d (%.2f%%)\n" \
    "$count" "$total" "$(awk "BEGIN{print ($count/$total)*100}")" \
    >> "$logfile"

  proto_filter=""
  [ "$proto" = "6" ]  && proto_filter="tcp"
  [ "$proto" = "17" ] && proto_filter="udp"
  [ -z "$proto_filter" ] && continue

  fname="./biflow/flow_${src_ip}_${src_port}_${dst_ip}_${dst_port}_${proto_filter}.pcap"

  tshark -r chunk_00438_20191206054502.pcap -n -w "$fname" \
    -Y "$proto_filter && (
          (ip.src==$src_ip && ip.dst==$dst_ip &&
           $proto_filter.srcport==$src_port &&
           $proto_filter.dstport==$dst_port)
          ||
          (ip.src==$dst_ip && ip.dst==$src_ip &&
           $proto_filter.srcport==$dst_port &&
           $proto_filter.dstport==$src_port)
        )"

done < flows.txt
```

```
total=$(wc -l < flows.txt)
count=0
logfile="progress.log"

: > "$logfile"   # truncate log at start

while IFS=',' read -r src_ip dst_ip src_port dst_port proto; do
  count=$((count+1))

  printf "Flow progress: %d/%d (%.2f%%)\n" \
    "$count" "$total" "$(awk "BEGIN{print ($count/$total)*100}")" \
    >> "$logfile"

  proto_filter=""
  [ "$proto" = "6" ]  && proto_filter="tcp"
  [ "$proto" = "17" ] && proto_filter="udp"
  [ -z "$proto_filter" ] && continue

  fname="./biflow/flow_${src_ip}_${src_port}_${dst_ip}_${dst_port}_${proto_filter}.pcap"

  tcpdump -r chunk_00438_20191206054502.pcap -n -w "$fname" \
    "$proto_filter and (
        (src host $src_ip and dst host $dst_ip and src port $src_port and dst port $dst_port) or
        (src host $dst_ip and dst host $src_ip and src port $dst_port and dst port $src_port)
     )"

done < flows.txt
```

**NOTA:** Per eseguire queste operazioni è possibile utilizzare gli scripts presenti all'interno della seguente directory:
- script 1
- script 2
- script 3
- script 4
- 