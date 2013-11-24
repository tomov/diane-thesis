f = open('svc.csv', 'r')
out = open('out.sql', 'w')

line = f.readline()
cols = line.split(',')

rescolleges = {'Butler' : 1, 'Forbes' : 2, 'Mathey' : 3, 'Rkefeller' : 4, 'Whitman' : 5, 'Wilson' : 6, 'Graduate College' : 7, '' : 8}


counter = 0
count = 0
allemails = ''
for line in f:
    vals = line.split(',')

    values = ''
    query = 'insert into Users ('
    netid = ''
    isap = ''
    international = 0
    for i in range(len(vals)): 
        col = cols[i].strip('"\n')
        val = vals[i].strip('"\n')
        col = '`' + col + '`'
        val = '"' + val + '"'
        if col == '`ResidentialCollegeID`':
            val = str(rescolleges[val.strip('"')])
        elif col == '`EmailAddress`':
            email = val.strip('"')
            isap = isap + val
            if len(allemails) >= 100:
                print allemails
                allemails = ''
            netid = (val.split('@')[0]).strip('"')
        if col == '`PermanentState`' and val.strip('" ') == '':
            count = count + 1
            international = 1
        if col == "`FirstName`" or col == "`LastName`" or col == "`ClassYear`":
            isap = isap + val + ', '
            
        query = query + col + ', '
        values = values + val + ', '
   
    if international == 1:
        print isap

    query = query + '`LogonID`) values (' + values + '"' + netid + '") on duplicate key update '
    for i in range(len(cols)):
        col = cols[i].strip('"\n')
        col = '`' + col + '`'
        if i > 0:
            query = query + ', '
        query = query + col + ' = values(' + col + ')'
    
    #print query + ';\n'

    counter = counter + 1

    #if counter > 10:
    #    break

