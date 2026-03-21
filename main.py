import math
import copy

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
    def zero(cls, m: int, n: int=-1):
        if n == -1: n = m
        return cls(m=m, n=n, content=[0]*m*n)
        
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
    
    def __sub__(self, other: type["Matrix"]):
        return self.add(self, -1*other)
    
    # scalar mutliplication
    @classmethod
    def scalar_mul(cls, m: type["Matrix"], c: float):
        if isinstance(m, Matrix) and isinstance(c, (int, float)):
            return cls(m=m.m, n=m.n, content=[c*a for a in m.content])
        else:
            raise TypeError("can only multiply matrix by int or float.")
        
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
        raise TypeError(f"cannot multiply matrix by type {type(other)}.")

    def __truediv__(self, other: float):
        if isinstance(other, (int, float)):
            return self.scalar_mul(self, 1/other)
        # else
        raise TypeError(f"cannot divide matrix by type {type(other)}.")

    def __floordiv__(self, other: float):
        if isinstance(other, (int, float)):
            m = self.scalar_mul(self, 1/other)
            m.content = [math.floor(val) for val in m.content]
            return m
        # else
        raise TypeError(f"cannot divide matrix by type {type(other)}.")

    # matrix equality
    @staticmethod
    def is_equal(m1: type["Matrix"], m2: type["Matrix"]):
        return isinstance(m1, Matrix) and isinstance(m2, Matrix) and (
            m1.m == m2.m and m1.n == m2.n and m1.content == m2.content)

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

    def reduced_row_echelon_form(self):
        matrix = copy.copy(self)
        # 1. check if equals zero matrix
        if matrix == Matrix.zero(matrix.m, matrix.n):
            return matrix
        # 2. determine leftmost nonzero column
        depth = 0
        leading_ones: list[tuple[int, int]] = []
        while depth < matrix.m:
            i = depth # row index
            j = depth # col index
            e = -1 # current entry
            while i < matrix.m and j < matrix.n:
                e = matrix.get_entry(i, j)
                if e != 0:
                    break
                else:
                    if i == matrix.m-1:
                        i = depth
                        j += 1
                    else:
                        i += 1
            # 5. return if no more nonzero column
            if e == 0:
                break
            # jth column is the leftmost nonzero column now
            # 3. put one to the topmost position of this col
            matrix.row_swap(depth, i)
            matrix.row_mul(depth, 1/e)
            # (depth, j) is pivot now
            leading_ones.append((depth, j))
            # 4. put zeros below the pivot
            for r in range(1+depth, matrix.m):
                # for each row
                re = matrix.get_entry(r, j) # row leftmost
                rm = -1*re # multiplier to make re zero
                matrix.row_add(r, depth, rm)

            # 6. repeat for submatrix
            depth += 1

        # 7. matrix is in row-echelon form now
        # 8. we have determined all leading ones
        leading_ones = leading_ones[::-1]
        # 9. determine rightmost leading one
        # 11. repeat for submatrix
        for k in range(len(leading_ones)):
            one = leading_ones[k]
            # 10. delete entries in column above leading one
            # 12. repeat for submatrix
            for r in range(one[0]):
                # for each row
                re = matrix.get_entry(r, one[1]) # entry above
                rm = -1*re # multiplier to make re zero
                matrix.row_add(r, one[0], rm)
        # 13. matrix is in reduced row-echelon form now
        return matrix

    def __repr__(self):
        content_format = ""
        i = 0
        for _ in range(self.m):
            content_format += "\n"
            content_format += str(self.content[i:i+self.n])
            # content_format += str(self.content[i:i+self.n])[1:-1].replace(",", "")
            i += self.n
        return f"Matrix({self.m}x{self.n}{content_format})"
