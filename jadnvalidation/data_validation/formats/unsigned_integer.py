class UnsignedInteger:
    
    data: any = None
    bits: int = None

    def __init__(self, data: any = None, bits: int = None):
        self.data = data
        self.bits = bits

    def validate(self):
        # Check if self.data is an integer and non-negative
        if not isinstance(self.data, int):
            raise ValueError(f"Data {self.data} is not an integer.")
        if self.data < 0:
            raise ValueError(f"Data {self.data} is negative; unsigned integers must be >= 0.")

        # Check if self.bits is a valid positive integer
        if not isinstance(self.bits, int) or self.bits <= 0:
            raise ValueError(f"Bits value {self.bits} is not a valid positive integer.")

        unsig_min = 0
        unsig_max = pow(2, self.bits) - 1
        if unsig_min <= self.data <= unsig_max:
            pass
        else:
            raise ValueError(f"Data {self.data} is out of range for an unsigned integer of {self.bits} bits.")
