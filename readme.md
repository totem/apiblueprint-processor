# Markdown API Preprocessor

Enable keeping an [API Blueprint](http://apiblueprint.org) up to date.

Since the schemas in a blueprint are also stored with the project, this tool copies or replaces the schema in the api document with the schema data in the json files.

It uses a table declared at the top of the file to lookup the filename that points to the schema data for a Content Type.

## Installation

Download or copy the python script somewhere in your path.

    sudo curl -o /usr/local/bin/api-processor.py https://raw.github.com/totem/apiblueprint-processor/master/api-processor.py
    sudo chmod +x /usr/local/bin/api-processor.py

## Usage

Run the script with the filename to operate on.

    api-processor.py example.md

