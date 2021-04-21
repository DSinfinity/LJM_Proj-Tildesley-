import os

while True:
    directory = input("Direcotry: ")
    try:
        os.scandir(directory)
        print ("Success")
        os.chdir(directory)
        break
    except FileNotFoundError:
        print("Not a valid directory!")
        continue

fileList = []

for file in os.listdir(directory):
    filename = os.fsdecode(file)

    
    if filename.endswith(".dat"):
        with open (filename,"r") as f:
            ls = f.readlines()
            
            
            for x in range(0,6):  
                del ls[0]
            
            ls1 = [z.strip().split() for z in ls]
            success = []
            
            for i in range (len(ls1)-1):
                if float(ls1[i][11]) >= 2:
                    print("Good Data")
                    print (i)
                    print (ls1[i][11])
                    #print (filename)
                    fileList.append(filename)
                    success.append(i)
                    break
                
                else:
                    
                    continue
            if not success:
                print ("not found")
            else:
                print ("found at " + str(success))   

    else:
        continue

print ("Files of interest: "+str(fileList))
