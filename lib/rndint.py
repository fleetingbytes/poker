<<<<<<< HEAD
# pyRndOrg v0.2
# random.org Python API
#
# Copyright 2009 Felix Rauch <toastwaffel(at)gmail.com>
# released under the GNU Lesser General Public License 3
# 	http://www.gnu.org/licenses/lgpl.html
#
# === Brief introduction ===
# The pyRndOrg library consists of four modules:
#	rndint  -  Get a number of integers
#	rndseq  -  Get a sequence of integers
#	rndstr  -  Get a number of strings
#	rndorgQ -  Get your current quota
# You can import either the whole package or only the needed
# modules. Every module has one public function get([args]),
# whose possible arguments are explained in the README file
# aswell as in each module.
#
# === Usage <rndint.py> ===
# Gets a number of random integers
#
# get(min, max, [[num], [base]])
# min : Minimum value
# max : Maximum value
# num : Number of integers to get (default: 1)
# base: Mathematical base to be used (2/8/10/16) (default: 10)
#
# For more information on usage and restrictions, 
# read the README file or http://www.random.org/clients/http/
#
# Fixed for Python 3
# by Babarix <info(at)bsoft.at> 2014

import urllib.request
from string import Template

def get (min, max, num = 1, base = 10):

    # Check quota
    quotachk = urllib.request.urlopen("http://www.random.org/quota/?format=plain")
    if int(quotachk.read()) <= 0:
        return ("ERROR: Your Quota limit is below zero. Try again later\n"
                "ERROR: or buy new random numbers @ random.org")

    # Get and return integers
    urltmp = Template("http://www.random.org/integers/"
                      "?num=${num}&min=${min}&max=${max}&"
                      "col=1&base=${base}&format=plain&rnd=new")
    url = urltmp.substitute(num=num, min=min, max=max, base=base)

    dice = urllib.request.urlopen(url)
    strresult = dice.read()
    convstr = str(strresult, encoding='utf8')
    numlist = convstr.split("\n")
    numlist.pop()

    return numlist
=======
﻿# pyRndOrg v0.2
# random.org Python API
#
# Copyright 2009 Felix Rauch <toastwaffel(at)gmail.com>
# released under the GNU Lesser General Public License 3
# 	http://www.gnu.org/licenses/lgpl.html
#
# === Brief introduction ===
# The pyRndOrg library consists of four modules:
#	rndint  -  Get a number of integers
#	rndseq  -  Get a sequence of integers
#	rndstr  -  Get a number of strings
#	rndorgQ -  Get your current quota
# You can import either the whole package or only the needed
# modules. Every module has one public function get([args]),
# whose possible arguments are explained in the README file
# aswell as in each module.
#
# === Usage <rndint.py> ===
# Gets a number of random integers
#
# get(min, max, [[num], [base]])
# min : Minimum value
# max : Maximum value
# num : Number of integers to get (default: 1)
# base: Mathematical base to be used (2/8/10/16) (default: 10)
#
# For more information on usage and restrictions, 
# read the README file or http://www.random.org/clients/http/
#
# Fixed for Python 3
# by Babarix <info(at)bsoft.at> 2014

import urllib.request
from string import Template

def get(min, max, num = 1, base = 10):
    # Check quota
    quotachk = urllib.request.urlopen("http://www.random.org/quota/?format=plain")
    if int(quotachk.read()) <= 0:
        return ("ERROR: Your Quota limit is below zero. Try again later\n"
                "ERROR: or buy new random numbers @ random.org")
    # Get and return integers
    urltmp = Template("http://www.random.org/integers/"
                      "?num=${num}&min=${min}&max=${max}&"
                      "col=1&base=${base}&format=plain&rnd=new")
    url = urltmp.substitute(num=num, min=min, max=max, base=base)
    dice = urllib.request.urlopen(url)
    strresult = dice.read()
    convstr = str(strresult, encoding='utf8')
    numlist = convstr.split("\n")
    numlist.pop()
    return numlist

if __name__ == "__main__":
    pass
>>>>>>> remotes/upstream/master
