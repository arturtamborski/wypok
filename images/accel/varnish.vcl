# default config: https://github.com/varnishcache/varnish-cache/blob/master/bin/varnishd/builtin.vcl
vcl 4.0;

import std;
import directors;

acl purge {
    "localhost";
    "127.0.0.1";
    "::1";
}

backend app {
    .host = "app";
    .port = "8000";
    .connect_timeout = 3s;
    .max_connections = 256;
    .first_byte_timeout = 3s;
    .between_bytes_timeout = 3s;
    .probe = {
        .request =
            "HEAD / HTTP/1.1"
            "Host: localhost"
            "Connection: close"
            "User-Agent: Varnish Health Probe";
        .interval = 1m;
        .timeout = 3s;
        .threshold = 5;
        .window = 5;
    }
}

sub vcl_init {
    new vdir = directors.round_robin();
    vdir.add_backend(app);

    return (ok);
}

sub vcl_fini {
    return (ok);
}

sub vcl_recv {
    set req.backend_hint = vdir.backend();

    # remove proxy header, normalize host
    unset req.http.proxy;
    set req.http.Host = regsub(req.http.Host, ":[0-9]+", "");
    set req.http.Host = std.tolower(req.http.Host);

    # normalize url
    set req.url = std.querysort(req.url);
    set req.url = regsuball(req.url,"\?gclid=[^&]+$","");
    set req.url = regsuball(req.url,"\?gclid=[^&]+&","?");
    set req.url = regsuball(req.url,"&gclid=[^&]+","");
    set req.url = regsuball(req.url, "//", "/");
    if (req.url ~ "^http://") {
        set req.url = regsub(req.url, "http://[^/]*", "");
    }
    if (req.url ~ "\#") {
        set req.url = regsub(req.url, "\#.*$", "");
    }
    if (req.url ~ "\?$") {
        set req.url = regsub(req.url, "\?$", "");
    }

    # only local IPs can PURGE cache
    if (req.method == "PURGE") {
        if (client.ip ~ purge) {
            return (purge);
        }
        return (synth(403, "Access denied."));
    }

    # ignore invalid requests
    if (req.method != "GET" &&
        req.method != "HEAD" &&
        req.method != "POST" &&
        req.method != "PUT" &&
        req.method != "TRACE" &&
        req.method != "OPTIONS" &&
        req.method != "PATCH" &&
        req.method != "DELETE") {
        return (synth(403, "Invalid HTTP method."));
    }

    # pipe websockets
    if (req.http.Upgrade ~ "(?i)websocket") {
        return (pipe);
    }

    # clear cache for given url after POST request
    if (req.method == "POST") {
        #ban("obj.http.Url ~ " + req.url);
        set req.hash_always_miss = true;

        return (pass);
    }

    # cache only GET and HEAD requests
    if (req.method != "GET" && req.method != "HEAD") {
        return (pass);
    }

    # pass real client ip
    #if (req.restarts == 0) {
    #    if (req.http.X-Forwarded-For) {
    #        set req.http.X-Forwarded-For = req.http.X-Forwarded-For + ", " + client.ip;
    #    } else {
    #        set req.http.X-Forwaded-For = client.ip;
    #    }
    #}

    # normalize encoding header
    if (req.restarts == 0) {
        if (req.http.Accept-Encoding) {
            if (req.http.Accept-Encoding ~ "gzip") {
                set req.http.Accept-Encoding = "gzip";
            } elseif (req.http.Accept-Encoding ~ "deflate") {
                set req.http.Accept-Encoding = "deflate";
            } else {
                unset req.http.Accept-Encoding;
            }
        }
    }

    # we don't need this
    unset req.http.User-Agent;

    # clear headers received from client (possible header injection)
    if (req.http.X-sessionid) {
        unset req.http.X-sessionid;
    }

    if (req.http.X-ssrftoken) {
        unset req.http.X-csrftoken;
    }

    # copy cookie session token to headers
    if (req.http.Cookie ~ "sessionid") {
        set req.http.X-sessionid = regsub(req.http.Cookie,"^.*?sessionid=([^;]*);*.*$" , "\1");
        #set req.http.Cookie = regsub(req.http.Cookie,"^.*?sessionid=([^;]*);*.*$" , "");
    }

    # copy cookie csrf token to headers
    if (req.http.Cookie ~ "csrftoken") {
        set req.http.X-csrftoken = regsub(req.http.Cookie,"^.*?csrftoken=([^;]*);*.*$" , "\1");
        #set req.http.Cookie = regsub(req.http.Cookie,"^.*?csrftoken=([^;]*);*.*$" , "");
    }

    # remove DoubleClick offensive cookies
    set req.http.Cookie = regsuball(req.http.Cookie, "__gads=[^;]+(; )?", "");

    # remove the Quant Capital cookies (added by some plugin, all __qca)
    set req.http.Cookie = regsuball(req.http.Cookie, "__qc.=[^;]+(; )?", "");

    # remove the AddThis cookies
    set req.http.Cookie = regsuball(req.http.Cookie, "__atuv.=[^;]+(; )?", "");

    # remove any Google Analytics based cookies
    set req.http.Cookie = regsuball(req.http.Cookie, "__utm.=[^;]+(; )?", "");
    set req.http.Cookie = regsuball(req.http.Cookie, "_ga=[^;]+(; )?", "");
    set req.http.Cookie = regsuball(req.http.Cookie, "_gat=[^;]+(; )?", "");
    set req.http.Cookie = regsuball(req.http.Cookie, "utmctr=[^;]+(; )?", "");
    set req.http.Cookie = regsuball(req.http.Cookie, "utmcmd.=[^;]+(; )?", "");
    set req.http.Cookie = regsuball(req.http.Cookie, "utmccn.=[^;]+(; )?", "");

    # remove ';' prefix from cookies
    set req.http.Cookie = regsuball(req.http.Cookie, "^;\s*$", "");

    if (req.http.Cookie ~ "^\s*$") {
        unset req.http.Cookie;
    }

    # hit cache
    return (hash);
}

sub vcl_hash {
    hash_data(req.url);
    if (req.http.Host) {
        hash_data(req.http.Host); 
    } else {
        hash_data(server.ip);
    }

    if (req.url ~ "^/esi/$" && req.http.X-sessionid) {
        hash_data(req.http.X-sessionid);
    }

    return (lookup);
}

sub vcl_purge {
    return (synth(200, "Purged."));
}

sub vcl_pipe {
    # websockets support
    if (req.http.Upgrade) {
        set bereq.http.Upgrade = req.http.Upgrade;
    }

    set bereq.http.Connection = "close";

    return (pipe);
}

sub vcl_pass {
    return (fetch);
}

sub vcl_miss {
    return (fetch);
}

sub vcl_hit {
    if (obj.ttl > 0s) {
        # direct hit, send it
        return (deliver);
    }

    if (std.healthy(req.backend_hint)) {
        if (obj.ttl + obj.grace > 0s) {
            # page is in grace time, send it
            return (deliver);
        } else {
            # page expired, fetch from backend
            return (fetch);
        }
    } else {
        if (obj.ttl + obj.grace > 0s) {
            # deliver cached version
            return (deliver);
        } else {
            # page expired and backend is unhealthy

            # deliver old cached page anyways
            #return (deliver);

            # try fetching from unhealthy backend
            return (fetch);
        }
    }

    return (miss);
}

sub vcl_deliver {
    # remove internal headers before sending response
    unset resp.http.X-sessionid;
    unset resp.http.X-csrftoken;

    unset resp.http.Server;

    # heheh
    set resp.http.X-Never-Gonna = "Give-You-Up";

    return (deliver);
}

sub vcl_synth {
    set resp.http.Content-Type = "text/html; charset=utf-8";
    set resp.http.Retry-After = "5";

    # custom synth for redirections - ex. synth(302, "http://url.to.redirect.com/")
    if (resp.status == 301 || resp.status == 302) {
        set resp.http.Location = resp.reason;
        set resp.reason = "Moved";
    }

    # if backend is broken
    if (resp.status >= 500 && resp.status <= 504) {
        synthetic(std.fileread("/etc/varnish/error.html"));
    }

    return (deliver);
}

sub vcl_backend_fetch {
    return (fetch);
}

sub vcl_backend_response {
    # this will help in serving old pages if backend goes down
    set beresp.grace = 24h;

    if (bereq.uncacheable) {
        return (deliver);
    }

    # remove User-Agent from Vary header
    if (beresp.http.Vary ~ "User-Agent") {
	set beresp.http.Vary = regsub(beresp.http.Vary, ",? *User-Agent *", "");
	set beresp.http.Vary = regsub(beresp.http.Vary, "^, *", "");
	if (beresp.http.Vary == "") {
            unset beresp.http.Vary;
        }
    }

    # backend says that we shouldn't cache so we don't
    if (beresp.ttl <= 0s || 
        beresp.http.Set-Cookie || 
        beresp.http.Surrogate-control ~ "no-store" ||
        (!beresp.http.Surrogate-Control && 
        beresp.http.Cache-Control ~ "no-cache|no-store|private|must-revalidate") ||
        beresp.http.Vary == "*") {

        set beresp.ttl = 60s;
        set beresp.uncacheable = true;
    }

    # fix redirects with port number
    if (beresp.status == 301 || beresp.status == 302) {
      set beresp.http.Location = regsub(beresp.http.Location, ":[0-9]+", "");
    }

    # set expire header for client
    set beresp.http.Expires = "" + (now + beresp.ttl);

    if (bereq.url ~ "^/esi/" && bereq.http.X-sessionid) {
        set beresp.do_esi = true;
    }

    return (deliver);
}

sub vcl_backend_error {
    # retry fetching (and call synth if failed)
    #return (retry);

    # send response from backend
    return (deliver);
}
