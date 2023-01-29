def readFile():
    with open('gps_log.txt', encoding='utf8') as f:
        # read all contents of a file
        content = f.readlines()[-1]

        # seperate content into data needed (each name and its value)
        data = content.split(',')
        name = []
        value = []

        # split the data further into a name array and value array
        for i in data:

            splited = i.split(':')

            name.append(splited[0])
            value.append(splited[1])
        
        # making sure value for fix # is just and integer and does not include characters 
        num = ""
        for c in value[13]:
            if c.isdigit():
                num = num + c
        value[13] = num

        # print each name and its value seperately
        specificData = [7,8,10,12,13]

        for j in specificData:
           print(eval(name[j]))
           print(eval(value[j]))

        # close file
        f.close()

readFile()
