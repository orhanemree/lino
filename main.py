class Matrix:

    m: int
    n: int
    size: tuple[int, int]
    content: list[int]

    def __init__(self, m: int, n: int, content: list[int]):

        if m*n != len(content):
            raise ValueError("matrix size and content length must match.")
        
        self.m = m
        self.n = n
        self.size = (m, n)
        self.content = content

    def get_row(self, i: int):
        if not (0 <= i < self.m):
            raise IndexError(f"row {i} is out of matrix range {self.m}.")
        return self.content[i*self.n:i*self.n+self.n]

    def get_col(self, j: int):
        if not (0 <= j < self.n):
            raise IndexError(f"column {j} is out of matrix range {self.n}.")
        return [self.content[k*self.n+j] for k in range(self.m)]

    def get_entry(self, i: int, j: int):
        if not (0 <= i < self.m and 0 <= j < self.n):
            raise IndexError(f"index {i}, {j} is out of matrix range {self.m}, {self.n}.")
        return self.content[i*self.n+j]
    
    @classmethod
    def identity(cls, n: int):
        content = [0]*n*n
        for i in range(n):
            content[i*(n+1)] = 1
        return cls(m=n, n=n, content=content)
        
    @classmethod
    def from_file(cls, source: str):
        with open(source) as f:
            m = n = -1
            content = []
            for l in f.readlines():
                if l.isspace(): continue # ignore prior whitespace
                if m == -1:
                    size = l.strip().split(" ") # parse size
                    if len(size) != 2:
                        raise ValueError("matrix size must be specified in the first line.")
                    m = int(size[0])
                    n = int(size[1])
                else:
                    content += [int(e) for e in l.strip().split(" ")] # parse matrix entries
            if m*n != len(content):
                raise ValueError("matrix size and content length must match.")
            return cls(m=m, n=n, content=content)
        
    # matrix addition
    @classmethod
    def add(cls, m1: type["Matrix"], m2: type["Matrix"]):
        if isinstance(m1, Matrix) and isinstance(m2, Matrix):
            if m1.m != m2.m or m1.n != m2.n:
                raise ValueError("matrix sizes must match.")
            return cls(m=m1.m, n=m1.n, content=[a+b for a,b in zip(m1.content, m2.content)])
        else:
            raise TypeError("can only add matrix to matrix.")

    def __add__(self, other: type["Matrix"]):
        return self.add(self, other)
    
    def __sub__(self, other):
        return self.add(self, -1*other)

    # scalar mutliplication
    @classmethod
    def scalar_mul(cls, m: type["Matrix"], c: float):
        if isinstance(m, Matrix) and isinstance(c, (int, float)):
            return cls(m=m.m, n=m.n, content=[c*a for a in m.content])
        else:
            raise TypeError("can only multiply matrix with int or float.")
        
    def __rmul__(self, other: float):
        return self.scalar_mul(self, other)

    # matrix multiplication
    @classmethod
    def multiply(cls, m1: type["Matrix"], m2: type["Matrix"]):
        if isinstance(m1, Matrix) and isinstance(m2, Matrix):
            if m1.n != m2.m:
                raise ValueError("matrix_1 column size and matrix_2 row size must match.")
            product_content = []
            for i in range(m1.m*m2.n):
                ai=m1.get_row(i//m1.m)
                bj=m2.get_col(i%m2.n)
                product = sum([a*b for a, b in zip(ai, bj)])
                product_content.append(product)
            return cls(m=m1.m, n=m2.n, content=product_content)
        else:
            raise TypeError("can only multiply matrix by matrix.")

    def __mul__(self, other: float|type["Matrix"]):
        if isinstance(other, (int, float)):
            # scalar multiplication
            return self.scalar_mul(self, other)
        if isinstance(other, Matrix):
            # matrix multiplication
            return self.multiply(self, other)
        # else
        raise TypeError(f"cannot multiply type {type(other)} with matrix.")

    # matrix equality
    @staticmethod
    def is_equal(m1: type["Matrix"], m2: type["Matrix"]):
        return type(m1) == type(m2) and m1.m == m2.m and (
            m1.n == m2.n and m1.content == m2.content)

    def __eq__(self, other: type["Matrix"]):
        return self.is_equal(self, other)
    
    # in-place row swap
    def row_swap(self, r1: int, r2: int):
        if not (0 <= r1 < self.m and 0 <= r2 < self.m):
            raise IndexError(f"rows {r1} and {r2} are out of matrix row range {self.m}.")
        k1 = r1*self.n
        k2 = r2*self.n
        (self.content[k1:k1+self.n], self.content[k2:k2+self.n]) = (
            self.content[k2:k2+self.n], self.content[k1:k1+self.n])
        
    # in-place row multiplication
    def row_mul(self, r: int, c: float):
        if not (0 <= r < self.m):
            raise IndexError(f"row {r} is out of matrix row range {self.m}.")
        k = r*self.n
        row = self.content[k:k+self.n]
        row = [val * c for val in row]
        self.content[k:k+self.n] = row
        
    # in-place row addition
    def row_add(self, r1: int, r2: int, c: float):
        if not (0 <= r1 < self.m and 0 <= r2 < self.m):
            raise IndexError(f"rows {r1} and {r2} are out of matrix row range {self.m}.")
        k1 = r1*self.n
        row1 = self.content[k1:k1+self.n]
        k2 = r2*self.n
        row2 = self.content[k2:k2+self.n]
        row1 = [val1+val2*c for val1, val2 in zip(row1, row2)]
        self.content[k1:k1+self.n] = row1

    def __repr__(self):
        content_format = ""
        i = 0
        for _ in range(self.m):
            content_format += "\n"
            content_format += str(self.content[i:i+self.n])
            # content_format += str(self.content[i:i+self.n])[1:-1].replace(",", "")
            i += self.n
        return f"{self.m} {self.n}{content_format}"