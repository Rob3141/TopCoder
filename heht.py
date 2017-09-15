# function which performs the hashing function
# it takes the key and returns the calculated index
def hashfunc(index):
    return ord(index)

# function which takes the key & value pair to be inserted and updates the
# hash table accordingly
def insert(item, hashtable):
    index = hashfunc(item[:1])
    entry = item[2:]
    hashtable.update({index:entry})

    return hashtable

# function which takes the key & hash table and returns the value
# from the hash table
def lookup(index, hashtable):
    hashedIndex = hashfunc(index)
    return hashtable[hashedIndex]

# create hashtable based on user input
def createTable():
    # take number of students from the user
    noStud = int(raw_input("Enter no students: "))

    # initialise hash table and array to take key & value pairs for students
    hashtable = {}
    StudRaw = []

    # prompt user for key and value pair
    for i in range(0,noStud):
        prompt = "Enter student " + str(i+1) + " "
        StudRaw.append(raw_input(prompt))

    # run each entry through insert function to create hash table
    for i in range(0,len(StudRaw)):
        insert(StudRaw[i],hashtable)

    return hashtable

def runQuery(hashtable):
    # have user enter enter size of query
    StudEnqSize = int(raw_input())

    # have user enter keys for students he wants to look up
    # store each one in a list
    StudEnq = []
    for i in range(0,StudEnqSize):
        StudEnq.append(raw_input())

    # lookup each key in hashtable using lookup function
    for i in range(0,StudEnqSize):
        print lookup(StudEnq[i],hashtable)


# main function
def main():
    hashtable = {}
    hashtable = createTable()

    runQuery(hashtable)

main()
