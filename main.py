def err():
    print("ERROR")
    exit(1)

class Matrix:

    m: int
    n: int
    size: tuple[int, int]
    content: list[int]

    def __init__(self, m: int, n: int, content: list[int]):

        if type(m) != int or type(n) != int: err()
        self.m = m
        self.n = n
        self.size = (m, n)
        if m*n != len(content): err()
        self.content = content

    def get_row(self, i: int):
        if type(i) != int or not (0 <= i < self.m): err()
        return self.content[i*self.n:i*self.n+self.n]

    def get_col(self, j: int):
        if type(j) != int or not (0 <= j < self.n): err()
        return [self.content[k*self.n+j] for k in range(self.m)]

    def get_entry(self, i: int, j: int):
        if type(i) != int or type(j) != int or \
            not (0 <= i < self.m) or not (0 <= j < self.n): err()
        return self.content[i*self.n+j]
    
    @classmethod
    def identity(cls, n: int):
        if type(n) != int: err()
        content = [0]*n*n
        for i in range(n):
            content[i*(n+1)] = 1
        return cls(m=n, n=n, content=content)
        
    @classmethod
    def from_file(cls, source: str):
        with open(source) as f:
            m = -1
            n = -1
            content = []
            for l in f.readlines():
                if l.isspace(): continue # ignore prior whitespace
                if m == -1:
                    size = l.strip().split(" ") # parse size
                    if len(size) != 2: err()
                    m, n = size
                else:
                    content += [int(e) for e in l.strip().split(" ")] # parse matrix entries
            if int(m)*int(n) != len(content): err()
            return cls(m=int(m), n=int(n), content=content)
    
    # @classmethod
    # def from_string(cls, string: str):
    #     m = -1
    #     n = -1
    #     content = []
    #     for l in string.strip().split("\n"):
    #         if m == -1:
    #             size = l.strip().split(" ") # parse size
    #             if len(size) != 2: err()
    #             m, n = size
    #         else:
    #             content += [int(e) for e in l.strip().split(" ")] # parse matrix entries
    #     if int(m)*int(n) != len(content): err()
    #     return cls(m=int(m), n=int(n), content=content)
        
    # matrix addition
    @classmethod
    def add(cls, m1: type["Matrix"], m2: type["Matrix"]):
        if type(m1) != Matrix or type(m2) != Matrix: err()
        if m1.m != m2.m or m1.n != m2.n: err()
        return cls(m=m1.m, n=m1.n, content=[a+b for a,b in zip(m1.content, m2.content)])

    def __add__(self, other: type["Matrix"]):
        if type(other) != Matrix: err()
        return self.add(self, other)

    # scalar mutliplication
    # both c*M type and M*c type
    @classmethod
    def scalar_mul(cls, c: float|type["Matrix"], m1: type["Matrix"]|float):
        if type(c) == Matrix and type(m1) in (int, float):
            # M*c type
            c, m1 = m1, c # convert c*M type
        elif type(c) not in (int, float) or type(m1) != Matrix: err()
        # c*M type
        return cls(m=m1.m, n=m1.n, content=[c*a for a in m1.content])
        
    # scalar multiplicaiton c*M type
    # if it is a matrix multiplication, it is handled by the m1 matrix of m1*m2 type
    def __rmul__(self, other: float):
        if type(other) not in (int, float): err()
        return self.scalar_mul(other, self)

    # matrix multiplication
    @classmethod
    def multiply(cls, m1: type["Matrix"], m2: type["Matrix"]):
        if type(m1) != Matrix or type(m2) != Matrix: err()
        if m1.n != m2.m: err()

        product_content = []
        for i in range(m1.m*m2.n):
            ai=m1.get_row(i//m1.m)
            bj=m2.get_col(i%m2.n)
            product = sum([a*b for a, b in zip(ai, bj)])
            product_content.append(product)
    
        return cls(m=m1.m, n=m2.n, content=product_content)

    # either scalar M*c type or matrix multiplication
    def __mul__(self, other: float|type["Matrix"]):
        if type(other) in (int, float):
            # scalar multiplication M*c type
            return self.scalar_mul(other, self)
        if type(other) == Matrix:
            # matrix multiplication
            return self.multiply(self, other)
        err() # else

    # matrix equality
    @staticmethod
    def is_equal(m1: type["Matrix"], m2: type["Matrix"]):
        if type(m1) != Matrix or type(m2) != Matrix: err()
        return m1.m == m2.m and \
            m1.n == m2.n and \
            m1.content == m2.content

    def __eq__(self, other: type["Matrix"]):
        if type(other) != Matrix: err()
        return self.is_equal(self, other)

    def __repr__(self):
        content_format = ""
        i = 0
        for _ in range(self.m):
            content_format += "\n"
            content_format += str(self.content[i:i+self.n])
            # content_format += str(self.content[i:i+self.n])[1:-1].replace(",", "")
            i += self.n
        return f"{self.m} {self.n}{content_format}"
