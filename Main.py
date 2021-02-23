import hashlib
import json
from time import time
from Block_class import Block
#auxiliar variables do not touch
string_difficulty='0000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
string_offset=4
index=0

blockchain = [] #function to update the chain asking other nodes goes here
prev_hash_hex="Genesis block no previous hash"  #This will be used just for the very first block
difficulty=9   #number of zeros after the 'string offset that will be necesary to consider as proof of work (24 is a good number)

def hash_block(block_to_hash):
    string_object = json.dumps(block_to_hash, sort_keys=True)           #dumps the string
    block_string = string_object.encode()                               #formating the string
    raw_hash = hashlib.sha256(block_string)                             #getting the SHA256 of the block (argument)
    hex_hash = raw_hash.hexdigest()                                     #formatting as Hexadecimal
    decimal_hash=(int("0x"+hex_hash,0))
    binary_hash=bin(decimal_hash)
    return hex_hash, binary_hash

main_sentinel=1
while (main_sentinel==1):
    print("New Block? Enter 1")
    print("Verify a block? Enter 2")
    print("Print the whole BlockChain? Enter 3")
    print("Exit? Enter 4")
    choise = int(input("Your choise: "))


    if (choise == 1):
        print("Calculating, please wait...")
        
        if (len(blockchain)!=0):
            prev_hash_hex, prev_hash_bin=hash_block(blockchain[index -1])
        index=index+1
        #Section to get the data from web server
        block_data=input("Enter the data of block number " + str(index)+": ")
        block_signature=input("Enter the signature of the oferer: ")
        #Function to validate a signature will go here
        block_worker_incentive=input("How much will the miner wearn for hashing this block? ")  #There should be a function to extract how mucho money this user has in his wallet
        #End section to get the data from web server
        tic=time()
        sentinel1=10
        while sentinel1!=0:
            block = Block(index,prev_hash_hex,block_data,block_signature,block_worker_incentive,"")   #creates the block using those variable as arguments
            block_hash, block_hash_binary = hash_block(block.constructed_block)          #calculate the hash of the given block
            binary_extr=block_hash_binary[string_offset+0:string_offset+difficulty]                #extract the first "difficulty" bits of binary version of the hash so it can be compared
            if (binary_extr==string_difficulty[0:difficulty]):          #if the first "difficulty" bits are zero it found the correct chash
                sentinel1=0                                             #ends the while loop
        toc=time()
        time2=toc-tic
        blockchain.append(block.constructed_block)
        print(block.constructed_block + '\n')
        print('This block HASH:' + block_hash + '\n')
        print("Used time: " + str(time2) + " seconds\n")
    if (choise == 2):
        index_aux=int(input("Enter the index of the block you want to verify: "))
        if (index_aux>=2 and index_aux<=index):
            block_hash_aux=input("Enter the HEX hash of the already done block: ")
            block_data=input("Enter the data of block number " + str(index)+": ")
            block_signature=input("Enter the signature of the oferer: ")
            block_worker_incentive=input("How much will the miner wearn for hashing this block? ")
            proof_of_work=input("Please enter your proof of work: ")

            prev_hash_hex, prev_hash_bin=hash_block(blockchain[index -2])
            block = Block(index_aux,prev_hash_hex,block_data,block_signature,block_worker_incentive,proof_of_work)
            block_hash, block_hash_binary = hash_block(block.constructed_block)          #calculate the hash of the given block
            binary_extr=block_hash_binary[string_offset+0:string_offset+difficulty]                #extract the first "difficulty" bits of binary version of the hash so it can be compared
            if (binary_extr==string_difficulty[0:difficulty] and block_hash_aux==block_hash):          #if the first "difficulty" bits are zero it found the correct chash
                print("\n***************************************************")
                print("Block verified successfully.")# \nAdding Block to Chain")
                print("***************************************************\n")
            else:
                print("Error! Block is not valid")
        else:
            print("\n\nWARNING: Index range is: 2<=Index<=Blockchain_lenght\n\n")
    if (choise==3):
        print("\nPrinting Full BlockChain: \n")
        print("******************************************************************************************************")
        print(blockchain)
        print("\n******************************************************************************************************\n")
    if (choise==4):
        main_sentinel=2 #Ends the main while loop

print ("End of program")






