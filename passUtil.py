import hashlib

class passUtil():

    def __init__(self, algorithm):
        self.algorithm = algorithm

    def hash(self, password, salt, pepper):
        h = hashlib.new(self.algorithm)
        h.update((salt + password + pepper).encode('utf-8'))
        return h.hexdigest()
    
    def verify(self, password, salt, pepper, hashed):
        return self.hash(password, salt, pepper) == hashed