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