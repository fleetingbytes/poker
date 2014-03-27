# pyRndOrg v0.1
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
# === Usage <rndseq.py> ===
# Gets a sequence of integers
#
# get(min, max)
# min : The lower bound of the interval (inclusive)
# max : The upper bound of the interval (inclusive)
#
# For more information on usage and restrictions, 
# read the README file or http://www.random.org/clients/http/
#
# Fixed for Python 3
# by Babarix <info(at)bsoft.at> 2014

import urllib.request
from string import Template

def get(min, max):

    # Check quota
    quotachk = urllib.request.urlopen("http://www.random.org/quota/?format=plain")
    if int(quotachk.read()) <= 0:
        return ("ERROR: Your Quota limit is below zero. Try again later\n"
                "ERROR: or buy new random numbers @ random.org")

    # Get and return sequence
    urltmp = Template("http://www.random.org/sequences/?"
                      "min=${min}&max=${max}&col=1&format=plain&rnd=new")
    url = urltmp.substitute(min=min, max=max)

    dice = urllib.request.urlopen(url)
    strresult = dice.read()
    convstr = str(strresult, encoding='utf8')
    numlist = convstr.split("\n")
    numlist.pop()

    return numlist

if __name__ == "__main__":
    pass
