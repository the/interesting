Interesting
===========

The idea behind _interesting_ is to collect tech news articles and tweets in one place and tag them as either interesting or not in order to filter out the content one is actually interested in.

Installation
------------

Ensure you have Python 3 installed. The application is tested with Python 3.6.1 on macOS Sierra.

If you are on macOS and use homebrew:

    brew install python3

Create virual environment and activate it:

    python3 -m venv env
    source env/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

Configuration
-------------

You can activate different data sources in `config.yml`. If you want to activate Twitter you need to create a Twitter application with your own account on https://dev.twitter.com. Copy the required keys and secrets into the config.

The application will automatically collect data from all the sources that are configured in the config under source.

Running the application
-----------------------

Execute `run.sh` (or see its content how to do it manually).

Point your browser to http://localhost:5000.

Content of the enabled sources will appear in the corresponding sections. By up- and downvoting items the systems learns the user's interests. For items to appear in the _interesting_ section one needs to have at least one upvote and one downvote (predicted interestingness, not upvoted). The more data is gathered the more accurate the prediction becomes (200+ tagged items for a data source is a good start).
