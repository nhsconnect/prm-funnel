# PRM Data Funnel

This is a github pages site used for displaying various meaningful data related to Patient Record Migrations.

The hosted site can be found [here](https://nhsconnect.github.io/prm-funnel/).

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
