# PRM Data Funnel

This is a github pages site used for displaying various meaningful data related to Patient Record Migrations.

The hosted site can be found [here](https://nhsconnect.github.io/prm-funnel/).

## Adding data for an additional month

**Pre-requisites**
Ensure you have access to the `gp2gp-mi` index in the NMS Trends instance of Splunk.  

**Process**
1. Import the `splunk-dashboard.xml` file into Splunk
2. Set the date range for the month you wish to produce statistics for.
3. Create the funnel
   1. Duplicate a file from the `_funnels` directory
   2. Update the `title` and `date` fields
   3. Update the date range referenced in the text 
   4. Update the `EHR Requests sent` field using the `total` from the `EHR Requests sent grouped by sending and receiving system type` query
   5. Update the `EHR Extracts sent` field using the `total` from the `EHR extracts grouped by message type` query
   6. Update the file names in the `donuts` section to reference the new layer details created below
4. Update the EHR Requests sent details
   1. Duplicate an instance of the `supplier-to-supplier` file from the `_charts` directory
   2. Update the `date` and `timeframe` fields
   3. Update the date range referenced in the text
   4. Update the `total` field using the `total` from the `EHR Requests sent grouped by sending and receiving system type` query
   5. Ensure the order of the `labels` field corresponds to the order of results in the `EHR Requests sent grouped by sending and receiving system type` query
   6. Update the values in the `items` field with the values from the `EHR Requests sent grouped by sending and receiving system type` query
5. Update the EHR Extracts sent details
   1. Duplicate an instance of the `message-types` file from the `_charts` directory
   2. Update the `date` and `timeframe` fields
   3. Update the date range referenced in the text
   4. Update the `total` field using the `total` from the `EHR extracts grouped by message type` query
   5. Update the values in the `items` field with the values from the `EHR extracts grouped by message type` query
   6. Update the file names in the `donuts` section to reference the new layer details created below
6. Update the Large Message details
   1. Duplicate an instance of the `large-message-details` file from the `_charts` directory
   2. Update the `date` and `timeframe` fields
   3. Update the date range referenced in the text
   4. Update the `total` field using the `total` from the `Large Message details` query
   5. Ensure that order of the `labels` field corresponds to the order of results in the `Large message details` query: error descriptions are from the `GP2GP Response Codes` document
   6. Update the values in the `items` field with the values from the `Large Message Details` query
7. Update the Standard Message details
   1. Duplicate an instance of the `standard-message-details` file from the `_charts` directory
   2. Update the `date` and `timeframe` fields
   3. Update the date range referenced in the text
   4. Update the `total` field using the `total` from the `Standard Message details` query
   5. Ensure that order of the `labels` field corresponds to the order of results in the `Standard message details` query: error descriptions are from the `GP2GP Response Codes` document
   6. Update the values in the `items` field with the values from the `Standard Message Details` query

## How to run the site locally

 - clone the repo
 - `cd` into the repo root folder
 - install [homebrew](https://brew.sh)
 - install [rbenv](https://github.com/rbenv/rbenv) ruby version manager
   - `brew install rbenv`
 - install ruby 2.5.3
   - `rbenv install 2.5.3`
 - set local ruby version
   - `rbenv local 2.5.3`
 - install bundler
   - `gem install bundler`
 - install the gems for the website
   - `bundle`
 - run the site locally
   - `rbenv exec jekyll serve`
 - browse to [locally running site](http://127.0.0.1:4000/)

## How to update the site
The site is built with Jekyll, so their [site](https://jekyllrb.com/) is a great resource for assistance.

## How to add data graphs
 - copy one of the existing markdown files in the *funnel* directory
 - change the metadata accordingly (the content between the ---)
   - the *items* field takes an array in which each element has a label for the funnel slice and a value that will inform the width of the funnel slice
   donuts
   - the *donuts* field takes an array of elements that need a *document_name* value. The document provided needs to map to a document in the *donuts* folder. This donut page will be the one that is linked to by the funnel *item* at the same array index.
 - confirm that the changes made show up correctly in your local environment and push to the repository to release the change
