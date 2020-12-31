from bloomfilter import Bloom

# open a file and test the bloom filter; i tested the bloom filter with this dataset 
# https://github.com/smashew/NameDatabases/blob/master/NamesDatabases/first%20names/us.txt
names = open("names.txt", "r")

bf = Bloom(n=5000)

# print(bf.bit_arr)

for line in names:
    string = line.replace("\n", "")
    bf.insert(string)

# print(bf.bit_arr)

names.seek(0)
for line in names:
    string = line.replace("\n", "") + "1"  # attempt to get a false positive
    if bf.check(string):
        print(string)
