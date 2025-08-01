import hashlib

def file_hash(fname):
    with open(fname, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()