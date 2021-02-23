import hashlib
import json
from time import time
import random
import string

letters = string.ascii_letters

class Block:
    def __init__(self, index, previous_hash, data, signature, worker_incentive, proof_of_work):
        if (index == "" or index<1):
            return -1
        self.index = index
        if (previous_hash == ""):
            return -1
        self.previous_has = previous_hash
        if (data == ""):
            return -1
        self.data = data
        if (signature == ""):
            return -1
        self.signature = signature
        if (worker_incentive == ""):
            worker_incentive = "0"
        self.worker_incentive = worker_incentive
        if (proof_of_work == ""):
            proof_of_work = ''.join(random.choice(letters) for i in range(10))
        self.proof_of_work = proof_of_work
        string_actual_block = 'Index of block: ' + str(index) +' - Previous HASH: ' + previous_hash + " - Data of contract: " +self.data +' - Signature: '+ signature+' - Worker incentive: $' + worker_incentive + ' - Proof of work: ' +proof_of_work
        #string_actual_block = {'Previous HASH: ', previous_hash, " Data of contract: ", self.data, ' Signature: ', signature,' Worker incentive: $' , worker_incentive , ' Proof of work: ' ,proof_of_work}
        self.constructed_block = string_actual_block


