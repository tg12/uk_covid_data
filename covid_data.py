# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, TITLE AND
# NON-INFRINGEMENT. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR ANYONE
# DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY DAMAGES OR OTHER LIABILITY,
# WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Any donations will be donated to the relief effort
# Bitcoin Cash (BCH)   qpz32c4lg7x7lnk9jg6qg7s4uavdce89myax5v5nuk
# Ether (ETH) -        0x843d3DEC2A4705BD4f45F674F641cE2D0022c9FB
# Litecoin (LTC) -     Lfk5y4F7KZa9oRxpazETwjQnHszEPvqPvu
# Bitcoin (BTC) -      34L8qWiQyKr8k4TnHDacfjbaSqQASbBtTd


import csv
import requests
from fake_useragent import UserAgent
import json
import numpy
import matplotlib.pyplot as plt
from scipy import stats

ua = UserAgent()
url = "https://api.thevirustracker.com/free-api?countryTimeline=GB"

response = requests.get(url, headers={'User-Agent': ua.random})
pretty_json = json.loads(response.text)
#print (json.dumps(pretty_json, indent=2))

date_data = []
tally_data = []


def peakdet(v, delta, x=None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html

    Returns two arrays

    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.

    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.

    """
    maxtab = []
    mintab = []

    if x is None:
        x = numpy.arange(len(v))

    v = numpy.asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not numpy.isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = numpy.Inf, -numpy.Inf
    mnpos, mxpos = numpy.NaN, numpy.NaN

    lookformax = True

    for i in numpy.arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx - delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn + delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return numpy.array(maxtab), numpy.array(mintab)


for day in pretty_json["timelineitems"]:
    try:
        for each in day.keys():
            # print(each) #debug
            # print(day[each]['new_daily_deaths']) #debug
            if int(day[each]['new_daily_deaths']) > 0:
                tally_data.append(day[each]['new_daily_deaths'])
                date_data.append(each)
                # print("#############") #debug
    except BaseException:
        pass

# write this data to a file for use in the LTSM script.
# write this data to a file for use in the LTSM script.
# write this data to a file for use in the LTSM script.
with open('data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(date_data, tally_data))

##################################################################
# This graph shows if we are indeed "flattening the curve",
# it shows a trajectory and prediction of how steep the curve is
################################################################

_high, _low = peakdet(tally_data, .3)
res = stats.theilslopes(tally_data, numpy.arange(len(date_data)), 0.99)
# https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.mstats.theilslopes.html
print("[+]debug, medslope " + str(res[0]))
print("[+]debug, medintercept " + str(res[1]))
print("[+]debug, lo_slope " + str(res[2]))
print("[+]debug, up_slope " + str(res[3]))
plt.plot(date_data, tally_data, 'b.')
index = numpy.arange(len(date_data))
plt.plot(index, res[1] + res[0] * index, 'r-')
plt.plot(index, res[1] + res[2] * index, 'r--')
plt.plot(index, res[1] + res[3] * index, 'r--')
plt.xticks(rotation=90)
plt.show()

# Peaks and Low's Graph

plt.scatter(numpy.array(_high)[:, 0], numpy.array(_high)[:, 1], color='blue')
plt.scatter(numpy.array(_low)[:, 0], numpy.array(_low)[:, 1], color='red')
plt.plot(date_data, tally_data)
plt.ylabel('Number')
plt.xticks(rotation=90)
plt.show()
