import string
class Cipher:
    def __init__(self, key):
        self.table = key.lower()
        for i in string.ascii_lowercase:
            if i in self.table:
                continue
            else:
                self.table += i

    def encode(self, data):
        new_data = ""
        for i in data:
            if i.isalpha():
                idx = list(string.ascii_lowercase).index(i.lower())
                new_data += self.table[idx].lower() if i.islower() else self.table[idx].upper()
            else:
                new_data += i
        return new_data


    def decode(self, data):
        new_data = ""
        for i in data:
            if i.isalpha():
                idx = list(self.table).index(i.lower())
                new_data += string.ascii_lowercase[idx].lower() if i.islower() else string.ascii_lowercase[idx].upper()
            else:
                new_data += i
        return new_data
