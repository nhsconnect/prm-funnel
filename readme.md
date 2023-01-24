## Deprecated - 24 January 2023
This site is no longer published and only for historical purposes

# PRM Data Funnel

This is a github pages site used for displaying various meaningful data related to Patient Record Migrations.

The hosted site can be found [here](https://nhsconnect.github.io/prm-funnel/).

## Adding data for an additional month

**Pre-requisites**
Ensure you have access to the `gp2gp-mi` index in the NMS Trends instance of Splunk.  

**Process**
1. Copy _template folder (located inside ‘month’ folder), paste it in the same location and rename it to match the pattern YYYY-MM 
2. Change the name of markdown file (inside the newly created folder) to match the pattern YYYY-MM 
3. Change title and date fields inside root markdown file (see previous months for reference) - timestamp determines link order on site 
4. Open requester view ‘rr-funnel’: 
   1. Change ‘date’ field in rr-funnel.md (see previous months for reference) 
   2. Change items’ ‘link’ property to match the current directory in rr-funnel.md 
   3. Change “Data is sourced from” to match current month and year in rr-funnel.md 
   4. Open Splunk 
   5. Set the date range in Splunk for target month (e.g. from 1st to 31st January) 
   6. Run query for Registrations in Splunk (found in registrations.md) 
   7. Copy total value into ‘Registrations’ section of rr-funnel.md (use total in ‘total’ column of statistics NOT the number of events) 
   8. Open registrations.md and fill in values from count column in Splunk query statistics 
   9. Change date, timeframe fields, links and “The data was collected from...” to match the target month in registrations.md 
   10. Repeat steps *vi.-ix.* for transfers 
   11. Repeat steps *vi.-ix.* for gp2gp/gp2gp.md 
   12. Repeat steps *vi.-ix.* for integrations/ integrations.md (integrations total value is ‘Integrated’ count + ‘Suppressed’ count) 
5. For gp2gp folder there are several subfolders to update 
   1. In errors.md the same will need to be done for JDIE entries (this section can be copied from previous month but take care to add/remove any new/missing errors from current month and ensure all values are changed to the new month) 
   2. errors-pathways.md requires the ‘timestamp’ field to be updated as usual but has a Python helper script to fill the other fields. To use this script: 
      1. Run the query in Splunk 
      2. Export the result as json and name error_pathways.json 
      3. Move error_pathways.json file to the same directory as helper script 
      4. Transform the content of json file to a valid json format (add commas, wrap with curly braces and change data property to be an array) 
      5. Run error_pathways.py with python3 
   3. Copy the output from the terminal (excluding the last object in the array as it contains totals) and paste into ‘items’ in errors-pathways.md 
   4. In pathways.md template object in ‘items’ array will need to be duplicated for each category in ‘pathways’ Splunk query output 
6. Next run the query for integrations 
   1. Use the output to fill filing-by-requestor.md as in *5.iv.* 
7. Open sender view ‘sr-funnel’: 
   1. Run Splunk query from sr-funnel.md, fill the values in markdown file and fix dates 
   2. Run Splunk query from failure-points.md, fill the values and fix dates 
   3. This is the total for each column in the query output 
   4. Run Splunk query from success-vs-failure.md and fill the values 
   5. Run Splunk query from pathways.md and fill the values using Python script as in *5.ii.*  
   6. Run Splunk query from failure-pathways.md and fill the values using failure-pathways.py script as in *5.ii.* 

## How to run the site locally

 - clone the repo
 - `cd` into the repo root folder
 - install [homebrew](https://brew.sh)
 - remove RVM, if you have it installed
   - `rvm implode`
   - rvm doesn't play nice with rbenv. You could use just rvm instead, but rbenv is cleaner for managing ruby versions.
 - install [rbenv](https://github.com/rbenv/rbenv) ruby version manager
   - `brew install rbenv`
 - install ruby 2.6.3
   - `rbenv install 2.6.3`
 - set local ruby version
   - `rbenv local 2.6.3`
 - install bundler
   - `rbenv exec gem install bundler`
 - install the gems for the website
   - `rbenv exec bundle`
 - run the site locally
   - `rbenv exec bundle exec jekyll serve`
 - browse to [locally running site](http://127.0.0.1:4000/)

## How to update the site
The site is built with Jekyll, so their [site](https://jekyllrb.com/) is a great resource for assistance.

## How to add data graphs
 - copy one of the existing markdown files in the *funnel* directory
 - change the metadata accordingly (the content between the ---)
 - the *items* field takes an array in which each element has a label for the funnel slice and a value that will inform the width of the funnel slice. It takes an optional *link* key-value pair where the link value maps to a document in the *_charts* folder. This page will be the one that is linked to by the funnel *item* at the same array index.
 - confirm that the changes made show up correctly in your local environment and push to the repository to release the change

