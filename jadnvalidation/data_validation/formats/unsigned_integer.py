class UnsignedInteger:
    
    data: any = None
    bits: int = None

    def __init__(self, data: any = None, bits: int = None):
        self.data = data
        self.bits = bits
    
    def validate(self):

    
        signed_value = int(self.bits)
        #print("iN value for "+format+" between 0 and + 2^("+str(self.bits)+"-1)-1")
        unsig_min = 0
        unsig_max = pow(2,signed_value) -1
        if unsig_min <= self.data <= unsig_max:
            pass
        else:
            raise ValueError(f"Data {self.data} is out of range for a signed integer of {self.bits} bits.")
