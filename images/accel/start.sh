#!/bin/sh

varnishd -f /etc/varnish/varnish.vcl -s malloc,${MEMORY} -a ${ADDRESS}:${PORT}
sleep 1
varnishlog -b
