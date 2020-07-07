# GoFundMe Campaign Donataions Metrics and Analysis Tool

GoFundMe (GFM) Campaigns does not currently provide enough features or analysis tools that are important for sharing with the community of supporters, donors, and followers; especially for the managers of a campaign.

_For instance, I found it very difficult to quickly and easily see how many unique individuals donated, given some persons donating multiple times_

This simple tool provides a means for identifying and better understanding the quantitative and qualitative metrics associated with a GFM campaign.

## Staged WebApp Prototype

Please visit the app to test and provide comments and recommendations.

[GFM Campaign Metrics App](https://gfm-metrics-app-stage.herokuapp.com)

[Example GFM Metrics Page Image](docs/gfm-page-ex.png)

## Please note the following list of assumptions
* user must be able to navigate and find an existing GoFundMe campaign
* user must have basic knowledge and understanding of URLs

## Instructions for finding and copying list of Campaign donation entries
1. go to [GoFundMe page](www.gofundme.com)
    1. search for a GoFundMe Campaign (GFMC)
    OR
    1. find a specific GoFundMe Campaign
1. copy the URL path of the campaign
1. paste the URL into the [GFM Analysis App](https://gfm-metrics-app-stage.herokuapp.com)
1. wait for the results

## Constraints 
* valid GoFundMe Campaign URL
    * URLs outside of GFM return error
        * ">>> Not a valid URL"
    * non-valid GFM campaign URLs return error
        * ">>> Request Exception Error: 404 Client Error"
