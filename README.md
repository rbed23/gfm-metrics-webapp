# GoFundMe Campaign Donataions Metrics and Analysis Tool

The GoFundMe (GFM) Campaign Management tool does not currently provide enough features or campaign analysis tools that are important for sharing with the community of supporters.

_For instance, I found it very difficult to quickly and easily see how many unique individuals donated, given some persons donating multiple times_

This simple tool provides a means for identifying and better understanding the quantitative and qualitative metrics associated with a GFM campaign.

## Please note the following list of assumptions
* ~~Must be a manager of an existing GFM campaign with proper login credentials~~
* ~~requires user to copy/paste list of entries into a TXT file~~
* requires user to have basic understanding of UNIX CLI and URL usage

## Instructions for finding and copying list of Campaign donation entries
1. go to [GoFundMe page](www.gofundme.com)
    1. search for a GoFundMe Campaign (GFMC)
    OR
    1. find a specific GoFundMe Campaign
1. find the URL path of the GFMC
1. highlight and copy the URL path
1. run the following command in the UNIX CLI:
    * python3 PATH/TO/SCRIPT/py-gfm-donations-analysis.py [**paste GFMC URL**]

## Constraints 
* env: Python3
* imports: 
    * sys
    * statistics
    * json
    * requests
