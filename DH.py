import hashlib
import ssl
import binascii
import os

global generator
global prime
global key_length

prime = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8E
#GLOBAL PRIMITIVE ROOT
generator = 2
key_length = 100
# Private Key generator method
def generate_private_key(length):
    _rand = 0
    _bytes = length // 8 + 8
    # Generate a random private key such that it's less than the prime number
    while _rand.bit_length() < length:
        # Generate random bytes
        rand_bytes = os.urandom(_bytes)
        # Convert bytes to hex string
        hex_key = binascii.hexlify(rand_bytes).decode('utf-8')
        # Convert hex string to integer
        _rand = int(hex_key, 16)
    return _rand

# Public key generator method
#Public key = primitive root ^ private key % prime
def generate_public_key(private_key):
	public_key = pow(generator, private_key, prime)
	return public_key

#Secret key = public key ^ private key % q
def generate_secret(private_key, public_key):
    # Formula
    secret = pow(int(public_key), int(private_key), prime)
    try:
        secret_bytes = secret.to_bytes(
            secret.bit_length() // 8 + 1, byteorder="big")
    except AttributeError:
        secret_bytes = str(secret)
    # Generate hash key using SHA256
    key = hashlib.sha256()
    key.update(bytes(secret_bytes))
    secretKey = key.hexdigest()
    return secretKey
	

   
