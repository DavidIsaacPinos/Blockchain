from Block_class import Block
import select
import struct
import hashlib      #Library for hashing obvious
import json         #Library to format data
from time import time
import socket       #TCP connectivity library
import sys          #i dont really know why
import select       #To wait for a network packet efficiently
import winsound     # audio lybrary
frequency = 2500    # Set Frequency To 2500 Hertz
duration = 500      # Set Duration To "x" ms
#auxiliar variables do not touch
string_difficulty='0000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
string_offset=3
index=0

#communication port: 31445    #Because there is no known service runing in this port 

blockchain = [] #function to update the chain asking other nodes goes here
prev_hash_hex="Genesis block no previous hash"  #This will be used just for the very first block
difficulty=22   #number of zeros after the 'string offset that will be necesary to consider as proof of work (24 is a good number)
my_wallet = "0105594451"
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def hash_block(block_to_hash):
    string_object = json.dumps(block_to_hash, sort_keys=True)           #dumps the string
    block_string = string_object.encode()                               #formating the string
    raw_hash = hashlib.sha256(block_string)                             #getting the SHA256 of the block (argument)
    hex_hash = raw_hash.hexdigest()                                     #formatting as Hexadecimal
    decimal_hash=(int("0x"+hex_hash,0))
    binary_hash=bin(decimal_hash)
    return hex_hash, binary_hash

def send_nudes(nude):   #function to send nudes 7u7 as a UDP message
    REMOTE_IP = '192.168.10.255'
    UDP_PORT = 31445
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP message
    s.sendto(bytes(nude, "utf-8"), (REMOTE_IP, UDP_PORT))
    s.close()

def receive_nudes(connection):
    inputs = [connection]
    outputs = []
    readable, writable, exceptional = select.select(inputs, outputs, inputs, 0)
    if (len(readable)):
        data = connection.recv(1024)
        
        hash2 = str(data[0:64], 'utf-8')
        proof_of_work2=str(data[64:74], 'utf-8')
        wallet=str(data[74:len(data)], 'utf-8')
        return hash2, proof_of_work2, wallet
    else:
        return "", "", ""
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




    


#Main while for program starts:
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   #iniciates the socket
server.bind(('', 31445))
main_sentinel=1
while (main_sentinel==1):
    print("New Block? Enter 1")
    print("Verify a block? Enter 2")
    print("Print the whole BlockChain? Enter 3")
    print("Exit? Enter 4")
    choice = int(input("Your choise: "))


    if (choice == 1):
        if (len(blockchain)!=0):
            prev_hash_hex, prev_hash_bin=hash_block(blockchain[index -1])
        index=index+1
        #Section to get the data from web server
        block_data=input("Enter the data of block number " + str(index)+": ")
        block_signature=input("Enter the signature of the oferer: ")
        #Function to validate a signature will go here
        #End section to get the data from web server
        print("Calculating, please wait...")
        tic=time()
        sentinel1=10
        while sentinel1!=0:
            block = Block(index,prev_hash_hex,block_data,block_signature,str(my_wallet),"")   #creates the block using those variable as arguments
            block_hash, block_hash_binary = hash_block(block.constructed_block)          #calculate the hash of the given block
            binary_extr=block_hash_binary[string_offset+0:string_offset+difficulty]                #extract the first "difficulty" bits of binary version of the hash so it can be compared

            if (binary_extr==string_difficulty[0:difficulty]):          #if the first "difficulty" bits are zero it found the correct chash
                proof_of_work = block.proof_of_work
                send_nudes(block_hash + proof_of_work + my_wallet)
                break                                             #ends the while loop

            rcv_hash, rcv_proof_of_work, rcv_wallet = receive_nudes(server)
            if (len(rcv_hash)>0 and rcv_wallet != my_wallet): #This sentence is for not printing my own bradcaster message
                print("\n \n \n RECIBIDO!********************************************")
                print(rcv_hash)
                print(rcv_proof_of_work)
                print(rcv_wallet)

                block = Block(index,prev_hash_hex,block_data,block_signature,rcv_wallet,rcv_proof_of_work)  #Createsblock with recieved data from remote node
                block_hash, block_hash_binary = hash_block(block.constructed_block)                         #Calculate the hash of the given block
                binary_extr=block_hash_binary[string_offset+0:string_offset+difficulty]                     #Extract the first "difficulty" bits of binary version of the hash so it can be compared
                if (binary_extr==string_difficulty[0:difficulty] and rcv_hash==block_hash):                 #If the first "difficulty" bits are zero it found the correct chash
                    print("\n***************************************************")
                    print("Block successfully verified. \nAdding Block to Chain")
                    print("***************************************************\n")
                    break
                else:
                    print("Error! Block is not valid")
                       
                
        toc=time()
        time2=toc-tic                                           #calculate how much time was used to calculate this hash
        winsound.Beep(frequency, duration)                      #produces a sound when the new block is ready
        if (time2>180):difficulty=difficulty-1                  #decreases the difficulty if the time is too long
        if (time2<120):difficulty=difficulty+1                  #increases the difficulty if the time is too short
        blockchain.append(block.constructed_block)
        print(block.constructed_block + ' Block HASH: ' + block_hash + '\n')
        print("Used time: " + str(time2) + " seconds\n")
        print("Difficult is: " + str(difficulty))  

    if (choice==3):
        print("\nPrinting Full BlockChain: \n")
        print("******************************************************************************************************")
        print(blockchain)
        print("\n******************************************************************************************************\n")
    if (choice==4):
        main_sentinel=2 #Ends the main while loop

print ("End of program")






