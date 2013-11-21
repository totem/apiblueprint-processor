#!/usr/bin/python

import argparse
import os.path
import re
import sys
import StringIO

content_types = {}

MATCH_TYPE = "Content Type"
MATCH_FILE = "Schema"

COL_TYPE = 0
COL_FILE = 1

TABLE_FOUND = False
IN_TABLE = False

R_CONTENT_TYPE = '^\|.*Content Type'

R_BLOCK = '^\s*\+\s*(Response|Request)\s*(.*)'
R_RES_TYPE = '.*\((.*)\)'
R_SCHEMA = '^\s*\+\s*Schema'
R_SCHEMA_BLOCK_START = '^(\s*)```js$'
R_SCHEMA_BLOCK_END = '^\s*```$'
R_EMPTY = '^\s*$'

SCHEMA_START = False
SCHEMA_IN = False
SCHMEA_WHITESPACE = ''

CURRENT_TYPE = None


parser = argparse.ArgumentParser(
    description="Inject data into a markdown file")

parser.add_argument('filename', help='filename')

parser.add_argument('-d', '--dry-run', default=False, action='store_true',
                    help='print to stdout instead of the file')

args = parser.parse_args()

if not os.path.isfile(args.filename):
    print "%s doesn't exist" % args.filename
    sys.exit(1)


# helper to check for the content type and the json file
def exists(ctype):
    if ctype not in content_types:
        return False

    return os.path.isfile(content_types[ctype])


# process the markdown file
output = StringIO.StringIO()
with open(args.filename) as f:
    for l in f.readlines():

        # is this a table with the content types declared
        if not TABLE_FOUND and re.match(R_CONTENT_TYPE, l):
            # allow processing rows
            IN_TABLE = True
            # don't repeat the regex later
            TABLE_FOUND = True

            # get the header columns
            headers = l.split('|')

            # assign the correct column numbers
            for x in range(len(headers)):
                if headers[x].strip() == MATCH_TYPE:
                    COL_TYPE = x
                if headers[x].strip() == MATCH_FILE:
                    COL_FILE = x

            output.write(l)
            continue

        # if left the table, mark it
        if IN_TABLE and not re.match('^\|', l):
            IN_TABLE = False

        # make sure its not a header separator
        if IN_TABLE and not re.match('^\|-', l):
            headers = l.split('|')

            content_types[headers[COL_TYPE].strip()] = \
                headers[COL_FILE].strip()

        if not IN_TABLE:
            # look for a request/response block
            m = re.match(R_BLOCK, l)
            ctype = None

            # if this is a request or response, check for the content type
            if m:
                raw = m.groups()[1]

                # see what response/request we "currently" are
                m2 = re.match(R_RES_TYPE, raw)
                if m2:
                    ctype = m2.groups()[0]
                else:
                    # if we don't have one, set to None
                    CURRENT_TYPE = None

            # only set the current type if it's been defined and the json
            # file exists
            if ctype is not None and exists(ctype):
                CURRENT_TYPE = ctype
                output.write(l)
                continue

            # check for lines with a + Schema when we have a current type
            if CURRENT_TYPE is not None and re.match(R_SCHEMA, l):
                SCHEMA_START = True
                output.write(l)
                continue

            # What to do "in" a schema block
            if SCHEMA_START:
                # are we at the bottom?
                if re.match(R_SCHEMA_BLOCK_END, l):
                    # add the json file here
                    with open(content_types[CURRENT_TYPE]) as j:
                        for jl in j.readlines():
                            output.write('%s%s' % (SCHMEA_WHITESPACE, jl))

                    output.write(l)

                    # reset all values at the end of a schema
                    SCHEMA_START = False
                    SCHEMA_IN = False
                    SCHMEA_WHITESPACE = ''

                    CURRENT_TYPE = None
                    continue

                # if we are in the middle of the ```js block, skip output
                if SCHEMA_IN:
                    continue

                # look for the start of the ```js block
                m = re.match(R_SCHEMA_BLOCK_START, l)

                if m:
                    SCHMEA_WHITESPACE = m.groups()[0]
                    SCHEMA_IN = True
                    output.write(l)
                    continue

                # have we left the block?
                if not re.match(R_EMPTY, l):
                    # reset all values if we leave the block
                    SCHEMA_START = False
                    SCHEMA_IN = False
                    SCHMEA_WHITESPACE = ''

                    CURRENT_TYPE = None
                    ##

        # fell through, so add the line
        output.write(l)


contents = output.getvalue()
output.close()

if args.dry_run:
    print contents
else:
    with open(args.filename, 'w') as f:
        f.write(contents)
