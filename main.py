import hashlib
import random
import time
# ElGamal Signature implementation

def generate_keys():
    p = 23 # example prime number, in practice this should be very large
    g = 5  # primitive root modulo p
    x = random.randint(1, p-2) # private key
    y = pow(g, x, p)           # public key

    return (p, g, y), x

def elgamal_sign(M, p, g, x):
    k = random.randint(1, p-2)
    while gcd(k, p-1) != 1:
        k = random.randint(1, p-2)
    r = pow(g, k, p)
    k_inv = pow(k, -1, p-1)
    s = (M - x*r) * k_inv % (p-1)
    return r, s

def elgamal_verify(M, r, s, p, g, y):
    print("Verification using Elgamal:")
    print(pow(g, M, p) == (pow(y, r, p) * pow(r, s, p)) %p)
    return pow(g, M, p) == (pow(y, r, p) * pow(r, s, p)) % p

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Simple Blockchain Implementation

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        block_string = "{}{}{}{}{}".format(self.index, self.transactions, self.timestamp, self.previous_hash, self.nonce)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        print("This is the genesis block's hash:")
        print(genesis_block.hash)
        self.chain.append(genesis_block)

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash or not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.endswith('000') and block_hash == block.compute_hash())

    def proof_of_work(self, block):

        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.endswith('000'):
            block.nonce += 1
            computed_hash = block.compute_hash()

        print("This is the last nonce number:")
        print(block.nonce)
        print("And this is the resulting computed_hash:")
        print(computed_hash)
        print("We thank miner Tigran and give him a reward of 0.0000000001 BTC")
        return computed_hash

    @property
    def last_block(self):
        return self.chain[-1]

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index


# Generate keys for a user
public_key, private_key = generate_keys()

# Create a blockchain
blockchain = Blockchain()

# Add a transaction
transaction = "Sergey sends 100 dollars to Susanna"
print("The message is:" )
print(transaction)
# Assuming public_key = (p, g, y)
p, g, y = public_key


print("The private key is:")
print(private_key)
print("The public key is:")
print(public_key)

hashed_message = hashlib.sha256(transaction.encode()).hexdigest()
print("The hash of a message is:")
print(hashed_message)
r, s = elgamal_sign(int(hashed_message, 16), p, g, private_key)
signed_transaction = {"transaction": transaction, "signature": (r, s)}
print("The signed hash message is:")
print(signed_transaction)
blockchain.add_new_transaction(signed_transaction)

# Mine a block
blockchain.mine()

# Verify the signature in the block
block = blockchain.chain[-1]
for tx in block.transactions:
    hashed_message = hashlib.sha256(tx["transaction"].encode()).hexdigest()
    M = int(hashed_message, 16)  # Convert hexadecimal hash to integer
    assert elgamal_verify(M, *tx["signature"], *public_key)



#New Transaction
new_transaction = "Susanna sends 5000 bitcoins to Naruto Uzumaki"

#Hash the Transaction
hashed_new_transaction = hashlib.sha256(new_transaction.encode()).hexdigest()

# Sign the Transaction
# Assuming public_key = (p, g, y)
p, g, y = public_key
r, s = elgamal_sign(int(hashed_new_transaction, 16), p, g, private_key)

# Create Signed Transaction Object
signed_new_transaction = {"transaction": new_transaction, "signature": (r, s)}

# Add to Unconfirmed Transactions
blockchain.add_new_transaction(signed_new_transaction)

# Mine a New Block (Optional)
blockchain.mine()
block = blockchain.chain[-1]
for tx in block.transactions:
    hashed_message = hashlib.sha256(tx["transaction"].encode()).hexdigest()
    M = int(hashed_message, 16)  # Convert hexadecimal hash to integer
    assert elgamal_verify(M, *tx["signature"], *public_key)