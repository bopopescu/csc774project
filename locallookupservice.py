#!/usr/bin/python
# coding:utf8

from flask import Flask, request, abort, jsonify
from ipwhois import IPWhois
from ipaddress import ip_network
from time import clock

app = Flask("Local lookup Server")

@app.route('/origin/<prefix>', methods=["GET"])
def origin(prefix):
    prefix=prefix.replace("nm",'/')
    app.logger.debug("Lookup request for prefix"+prefix)
    try:
        ipn=ip_network(unicode(prefix))
        start=clock()
        rr=IPWhois(ipn.hosts().next()).lookup_whois()
        end=clock()
        response={"querytime":end-start,"rr":rr}
    except ValueError as ve:
        return abort(400,ve)
    except Exception as e:
        return abort(404,e)
    return jsonify(response)