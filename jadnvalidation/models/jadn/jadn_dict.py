'''
JADN Dictionary class exists to provide a dictionary that will raise an error if a key already exists in the dictionary.
Python dictionaries do not raise an error when a key is added to a dictionary that already exists, they silently overwrite the value.
'''
class Jadn_Dict(dict):
    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(f"Key '{key}' already exists in the dictionary.")
        super().__setitem__(key, value)