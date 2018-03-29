#!/usr/local/env sh

if [ "$1" = 'check' ]; then
	varnishd -C -f /etc/varnish/varnish.vcl
	exit $?
fi

varnishd -f /etc/varnish/varnish.vcl -s malloc,${MEMORY} -a ${ADDRESS}:${PORT}
sleep 2
varnishlog -b
