import time
class GaloisField:
    def __init__(self, m, irreducible_poly):
        self.m = m
        self.irreducible_poly = irreducible_poly
        self.modulus = 1 << m  

    def to_bitstring(self, a):
        """Перетворення елемента у m-бітний рядок"""
        if isinstance(a, str):
            a = int(a, 2)
        return format(a, f'0{self.m}b')

    def from_bitstring(self, bitstring):
        """Перетворити m-бітний рядок в елемент"""
        return int(bitstring, 2)

    def add(self, a, b):
        """Додавання у поліноміальному базисі"""
        if isinstance(a, str):
            a = int(a, 2)
        if isinstance(b, str):
            b = int(b, 2)
        result = a ^ b
        return self.to_bitstring(result)

    def module(self, result):
        """Редукція числа по поліному в полі"""
        t = result
        while t.bit_length() >= self.irreducible_poly.bit_length():
            shift = t.bit_length() - self.irreducible_poly.bit_length()
            t ^= self.irreducible_poly << shift
        return t
    def multiply(self, a, b):
        """Множення у GF(2^m)"""
        if isinstance(a, str):
            a = int(a, 2)
        if isinstance(b, str):
            b = int(b, 2)
        result = 0
        for i in range(b.bit_length()):
            if (b >> i) & 1:
                result ^= a
            a <<= 1
        return self.to_bitstring(self.module(result))

    def square(self, a):
        """Піднесення елементу до квадрата у GF(2^m)"""
        return self.multiply(a, a)

    def power(self, base, exp):
        """Піднесення елемента до степеня"""
        if isinstance(base, str):
            base = int(base, 2)
        result = 1
        for _ in range(exp.bit_length()):
            if exp & 1:
                result = self.multiply(result, base)
            base = self.multiply(base, base)
            exp >>= 1
        return result

    def power_n(self, a, n):
        """Піднесення елемента до степеня n"""
        if isinstance(n, str):
            n = int(n, 2)
        result = self.power(a, n)
        return self.to_bitstring(result)

    def inverse(self, a):
        """Знаходження оберненого елемента у поліноміальному базисі"""
        return self.to_bitstring(self.power(a, self.modulus - 2))

    def trace(self, a):
        """Compute the trace of an element in GF(2^m)."""
        if isinstance(a, str):
            a = int(a, 2)
        result = a
        current = a
        for _ in range(1, self.m):
            current = self.multiply(self.to_bitstring(current), self.to_bitstring(current))
            current = int(current, 2)
            result ^= current
        return result


m = 173
irreducible_poly = (1 << 173) | (1 << 10) | (1 << 2) | (1 << 1) | 1  # x^173 + x^10 + x^2 + x + 1
field = GaloisField(m, irreducible_poly)

a = '00011001010000111101100011100000111001110100011000110010101100111010110010010101101110000111110010101011001000101110110110011111010101111101110101000000110010010110011111101'
b = '01110000010011010011000001010000010100010011011011101000100010100000111101011101100000010001011101100010010001101000100010110111011001100101010010100010000101011100101100011'
n = '00000110110010100110001110101111001001000000000110100011000000011001111111010010000001111010010001111100000100001101011100100110110000100100010010000101100011110101010100111'

zero = '0' * m
one = '0' * (m - 1) + '1'
addition = field.add(a, b)
multiplication = field.multiply(a, b)
square_a = field.square(a)
inverse_a = field.inverse(a)
power_n = field.power_n(a, n)
trace_a = field.trace(a)

print(f"A + B: {addition}")
print(f"A * B: {multiplication}")
print(f"A^2: {square_a}")
print(f"A^(-1): {inverse_a}")
print(f"A^N: {power_n}")
print(f"Trace: {trace_a}")


print('------------------Testing------------------')

def verify_identities(field, a, b, c, d, m):
    zero = '0' * m
    one = '0' * (m - 1) + '1'

    # Тотожність 1: (a + b) * c = b * c + c * a
    left = field.multiply(field.add(a, b), c)
    right = field.add(field.multiply(b, c), field.multiply(c, a))
    identity_1 = (left == right)

    # Тотожність 2: d^(2^m - 1) = 1 (для d ≠ 0)
    if d != zero:
        power_exp = (1 << m) - 1  # 2^m - 1
        d_power = field.power(d, power_exp)
        identity_2 = (d_power == one)
    else:
        identity_2 = None

    return identity_1, identity_2

a = '01101010101101101001011010011111100001101101010111110100100001010000001100011000111001111001100011110111001100000100111011101000010101111010101000100101011110100111000111010'
b = '00010000000101110010010010110000110110100111011100111110110100011010100010001011000011110011111101110000000011000011010010110001100101001100100011001110001110000011000001011'
c = '010010110100110100101111111101110110010011110011110010100111000110110111011011011110010010010111000110111101011011110000100101110011010101101111010010100101101110001110000001100111010010'
d = '1010011110001000110111110101101100111001010100100110100001111000111001111000111111111101000000000001010101001011111001011011001001010101111101011001000111101011111111111111011011100100'

identity_1, identity_2 = verify_identities(field, a, b, c, d, m)

print(f"Тотожність 1 ((a + b) * c = b * c + c * a): {'Виконується' if identity_1 else 'Не виконується'}")
if identity_2 is not None:
    print(f"Тотожність 2 (d^(2^m - 1) = 1): {'Виконується' if identity_2 else 'Не виконується'}")
else:
    print("Тотожність 2 не перевіряється, оскільки d = 0.")


print('------------------Time Testing------------------')
def measure_time_for_operations(field, a, b, m, num_trials=1000):
    times = {
        "Addition": [],
        "Multiplication": [],
        "Square": [],
        "Inverse": [],
        "Power": [],
        "Trace": []
    }

    for _ in range(num_trials):
        start = time.perf_counter()
        field.add(a, b)
        end = time.perf_counter()
        times["Addition"].append(end - start)

    for _ in range(num_trials):
        start = time.perf_counter()
        field.multiply(a, b)
        end = time.perf_counter()
        times["Multiplication"].append(end - start)

    for _ in range(num_trials):
        start = time.perf_counter()
        field.square(a)
        end = time.perf_counter()
        times["Square"].append(end - start)

    for _ in range(num_trials):
        start = time.perf_counter()
        field.inverse(a)
        end = time.perf_counter()
        times["Inverse"].append(end - start)

    for _ in range(num_trials):
        start = time.perf_counter()
        field.power(a, int('1001', 2))  
        end = time.perf_counter()
        times["Power"].append(end - start)

    for _ in range(num_trials):
        start = time.perf_counter()
        field.trace(a)
        end = time.perf_counter()
        times["Trace"].append(end - start)

    avg_times = {operation: sum(times_list) / len(times_list) for operation, times_list in times.items()}

    return avg_times

m = 173
irreducible_poly = (1 << 173) | (1 << 10) | (1 << 2) | (1 << 1) | 1
field = GaloisField(m, irreducible_poly)

a = '01101010101101101001011010011111100001101101010111110100100001010000001100011000111001111001100011110111001100000100111011101000010101111010101000100101011110100111000111010'
b = '00010000000101110010010010110000110110100111011100111110110100011010100010001011000011110011111101110000000011000011010010110001100101001100100011001110001110000011000001011'

avg_times = measure_time_for_operations(field, a, b, m)

for operation, avg_time in avg_times.items():
    print(f"{operation}: {avg_time:.20f}")
