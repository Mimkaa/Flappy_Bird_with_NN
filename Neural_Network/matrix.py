import random
class Matrix:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.data = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    @staticmethod
    def map_static(mat, fn):
        # apply a func to every element of a matrix
        result = Matrix(mat.rows, mat.columns)
        for row in range(result.rows):
                for column in range(result.columns):
                    val = mat.data[row][column]
                    result.data[row][column] = fn(val)
        return result

    def map(self, fn):
        # apply a func to every element of a matrix
        for row in range(self.rows):
                for column in range(self.columns):
                    val = self.data[row][column]
                    self.data[row][column] = fn(val)

    def add(self,n):
        if isinstance(n, Matrix):
            for row in range(self.rows):
                for column in range(self.columns):
                    self.data[row][column] += n.data[row][column]
        else:
            for row in range(self.rows):
                for column in range(self.columns):
                    self.data[row][column] += n
    @staticmethod
    def multiply_mats(a, b):

        if a.columns != b.rows:
            return None
        result = Matrix(a.rows, b.columns)
        for row in range(result.rows):
            for column in range(result.columns):
                sum = 0
                for k in range(b.rows):
                    sum += a.data[row][k] * b.data[k][column]
                result.data[row][column] = sum
        return result

    @staticmethod
    def subtract(a, b):
        result = Matrix(a.rows,a.columns)
        for row in range(result.rows):
            for column in range(result.columns):
                result.data[row][column] = a.data[row][column] - b.data[row][column]
        return result

    @staticmethod
    def from_Array(arr):
        m = Matrix(len(arr), 1)
        for i in range(len(arr)):
            m.data[i][0] = arr[i]
        return m

    def to_Array(self):
        arr = []
        for row in range(self.rows):
            for column in range(self.columns):
                arr.append(self.data[row][column])
        return arr



    def multiply(self,n):
        if isinstance(n, Matrix):
            for row in range(self.rows):
                for column in range(self.columns):
                    self.data[row][column] *= n.data[row][column]
        else:
            for row in range(self.rows):
                for column in range(self.columns):
                    self.data[row][column] *= n

    @staticmethod
    def transpose(matrix):
        result = Matrix(matrix.columns, matrix.rows)
        for row in range(matrix.rows):
                for column in range(matrix.columns):
                    result.data[column][row] = matrix.data[row][column]
        return result


    def randomize(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.data[row][column] += random.uniform(-1, 1)

    def show(self):
        for r in self.data:
            print(r)
        print()

# m = Matrix(3,3)
# m2 = Matrix(3,1)
# m.randomize()
# m.show()
# m.multiply(2)
# m2.randomize()
# m.show()
# m2.show()
# Matrix.multiply_mats(m, m2).show()
# m.transpose().show()
#
# def div(x):
#     return x/4
#
# m.map(div)
# m.show()
#
# Matrix.from_Array([1,2,3]).show()
