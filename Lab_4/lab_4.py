import numpy as np
class GaloisFieldONB:
    def __init__(self, m):
        if m <= 0:
            raise ValueError("Степінь розширення має бути додатнім")
        self.m = m
        self.p = 2 * m + 1
        self.powers_of_2 = [pow(2, i, self.p) for i in range(self.m)]
        self.matrix = self._compute_matrix()


    def is_prime(self, n):
        '''Перевірка числа на простоту'''
        if n <= 1:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        d = 5
        while d * d <= n:
            if n % d == 0 or n % (d + 2) == 0:
                return False
            d += 6
        return True

    def find_k(self, p):
        """Знайдемо найменше k, таке що 2^k ≡ 1 (mod p)"""
        value = 2
        k = 1
        while value != 1:
            value = (value * 2) % p
            k += 1
        return k

    def check_ONB(self):
        """Перевірка існування оптимального нормального базису"""
        p = self.p
        if not self.is_prime(p):
            return False, None
        k = self.find_k(p)
        if k == 2 * self.m:
            return True, k
        elif p % 4 == 3 and k == self.m:
            return True, k
        else:
            return False, k

    def _compute_matrix(self):
        """Обчислення мультиплікативної матриці"""
        matrix = [[0] * self.m for _ in range(self.m)]
        for i in range(self.m):
            for j in range(self.m):
                if (self.powers_of_2[i] + self.powers_of_2[j]) % self.p == 1:
                    matrix[i][j] = 1
                elif (self.powers_of_2[i] - self.powers_of_2[j]) % self.p == 1:
                    matrix[i][j] = 1
                elif (-self.powers_of_2[i] + self.powers_of_2[j]) % self.p == 1:
                    matrix[i][j] = 1
                elif (-self.powers_of_2[i] - self.powers_of_2[j]) % self.p == 1:
                    matrix[i][j] = 1
        return matrix

    def add(self, a, b):
        return a ^ b

    def _rotate_left(self, val, positions):
        """Циклічний зсув вліво"""
        positions = positions % self.m
        return ((val << positions) | (val >> (self.m - positions))) & (2**m - 1)

    def _rotate_right(self, val, positions):
        """Циклічний зсув вправо"""
        positions = positions % self.m
        return ((val >> positions) | (val << (self.m - positions))) & (2**m - 1)

    def square(self, a):
        '''Піднесення до квадрата через циклічний зсув вправо'''
        return self._rotate_right(a, 1)

    def sum(self, value):
        """Обчислення суми коефіцієнтів елемента"""
        sum_coeffs = 0
        for i in range(self.m):
            if (value >> i) & 1:
                sum_coeffs += 1
        return sum_coeffs

    def trace(self, value):
        """Обчислення сліду елемента (суму коефіцієнтів за модулем 2)."""
        return self.sum(value) % 2

    def mul(self, a, b):
        """Множення"""
        C = [0] * self.m
        a_bits = [int(x) for x in f'{a:0{self.m}b}']
        b_bits = [int(x) for x in f'{b:0{self.m}b}']
        a_shift = np.zeros((self.m, self.m), dtype=int)
        b_shift = np.zeros((self.m, self.m), dtype=int)
        for i in range(self.m):
            a_shift[i] = np.roll(a_bits, -i)
            b_shift[i] = np.roll(b_bits, -i)
        res = (a_shift @ self.matrix @ b_shift.T).diagonal() % 2
        return res.tolist()

    def power_n(self, num, n):
        """Піднесення елемента до довільного степеня"""
        result = 1
        base = num
        n_bin = bin(n)[2:]
        for bit in n_bin:
            if bit == '1':
                result = self.mul(result, base)
            base = self.square(base)
        return ''.join(map(str, result))

    def inverse(self, a):
        """Обернений"""
        p_minus_2 = self.p - 2
        return self.power_n(a, p_minus_2)


m = 173
irreducible_poly = (1 << 173) | (1 << 10) | (1 << 2) | (1 << 1) | 1  # x^173 + x^10 + x^2 + x + 1
field = GaloisFieldONB(m)

a = '00100010110000100001011000000100100001001111110001001010100111101001111011101111001000000101110011010101011111100100111101000001101010000001010001000000011110001011000101001'
b = '11001111111111101001100111010110011101100000100100000001010100110011011100000100111111010101011100111111101111111101100001001110010001000100011111101111110111001001000111010'
n = '01001001110101110001011101000100000111001011010111101100100011101111010010011111110001011011000000110111001000110101000101000000100000011011110101100011011001010011000010110'

addition = field.add(int(a, 2), int(b, 2))
square_a = field.square(int(a, 2))
trace_a = field.trace(int(a, 2))
multiplication = field.mul(int(a, 2), int(b, 2))
#power_n = field.power_n(int(a, 2), int(n, 2))
#inverse_a = field.inverse(a)


print(f"A + B: {format(addition, f'0{m}b')}")
print(f"A^2: {format(square_a, f'0{m}b')}")
print(f"Trace A: {trace_a}")
print(f"A * B: {''.join(map(str, multiplication))}")
#print(f"A^N: {square_a}")
#print(f"Обертний елемент для {a}: {format(inverse_a, f'0{m}b')}")
