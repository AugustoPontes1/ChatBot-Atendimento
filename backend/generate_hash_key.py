import hashlib


hash_object = hashlib.sha256()
hash_hex = hash_object.hexdigest()
print(f"SHA-256 hash {hash_hex}")
