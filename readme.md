# PRM Data Funnel

This is a github pages site used for displaying various meaningful data related to Patient Record Migrations.

The hosted site can be found [here](https://nhsconnect.github.io/prm-funnel/).

## Adding data for an additional month

**Pre-requisites**
Ensure you have access to the `gp2gp-mi` index in the NMS Trends instance of Splunk.  

**Process**
1. Import the `_splunk/splunk-rr-view-dashboard.xml` file into Splunk
2. Set the date range for the month you wish to produce statistics for.
3. Duplicate the previous month's directory from the `month` directory
4. Update the `title` and `date` and where present `timeframe` fields in all the markdown files
5. Update the date range referenced in the text 
6. Update any links to reference the correct month
7. Create the RR funnel
   1. For the `rr-funnel.md` file: copy the following data from splunk 
      * Registrations: Total from high level registration category
      * Transfers: Total from Transfer category
      * GP2GP : Total from GP2GP category
      * Integrations: GP2GP success and integrated from GP2GP category
   2. Create layers
      1. Update data in `items` in `rr-funnel/gp2gp/gp2gp.md` from GP2GP category
      2. Update data in `items` in `rr-funnel/gp2gp/errors/errors.md` from GP2GP failures
      3. Update data in `items` in `rr-funnel/gp2gp/errors-pathway/errors-pathways.md` from errors by pathway
      4. Update data in `items` in `rr-funnel/gp2gp/pathways/pathways.md` from GP2GP category by pathway
      5. Update data in `items` in `rr-funnel/integrations/integrations.md` from Filing status
      6. Update data in `items` in `rr-funnel/integrations/filing-by-requestor/filing-by-requestor.md` from Filing details by requestor
      7. Update data in `items` in `rr-funnel/registrations/registrations.md` from High level registration category
      8. Update data in `items` in `rr-funnel/transfers/transfers.md` from Transfer category
 
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
