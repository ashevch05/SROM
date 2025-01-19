import time

def to_base_2_32(num):
    base = 2 ** 32
    result = []
    while num > 0:
        digit = num % base
        num //= base
        result.append(digit)
        if num == 0:
            break
    return result

def hex_to_blocks(hex_value, base=2**32):
    r = int(hex_value, 16)
    blocks = []
    while r > 0:
        blocks.append(r % base)
        r //= base
    return blocks

def blocks_to_number(blocks, base=2**32):
    num = 0
    for i, block in enumerate(blocks):
        num = num + block * (base ** i)
    return hex(num)

def LongAdd(A, B, w = 32):
    n = max(len(A), len(B))
    C = [0] * n
    carry = 0
    for i in range(n):
        a_i = A[i] if i < len(A) else 0
        b_i = B[i] if i < len(B) else 0
        temp = a_i + b_i + carry
        C[i] = temp & (2**w - 1)
        carry = temp >> w
    return C

def LongSub(A, B, w=32):
    n = max(len(A), len(B))
    C = [0] * n
    borrow = 0
    for i in range(n):
        a_i = A[i] if i < len(A) else 0
        b_i = B[i] if i < len(B) else 0
        temp = a_i - b_i - borrow
        if temp >= 0:
            C[i] = temp
            borrow = 0
        else:
            C[i] = (1 << w) + temp
            borrow = 1
    return C

def LongCmp(A, B):
    n = max(len(A), len(B))
    A = A + [0] * (n - len(A))
    B = B + [0] * (n - len(B))
    i = n - 1
    while i >= 0:
        if A[i] > B[i]:
            return 1
        elif A[i] < B[i]:
            return -1
        i -= 1
    return 0

def LongMulOneDigit(A, b):
    n = len(A)
    C = [0] * (n + 1)
    carry = 0
    for i in range(n):
        temp = A[i] * b + carry
        C[i] = temp & (2 ** 32 - 1)
        carry = temp >> 32
    C[n] = carry
    while C and C[-1] == 0:
        C.pop()
    return C

def LongShiftDigitsToHigh(A, shift):
    n = len(A)
    C = [0] * (n + shift)

    for i in range(n):
        C[i + shift] = A[i]
    return C

def LongMul(A, B):
    n = len(B)
    C = [0] * (2 * n)
    for i in range(n):
        temp = LongMulOneDigit(A, B[i])
        temp = LongShiftDigitsToHigh(temp, i)
        C = LongAdd(C, temp)
    return C

def BitLength(n):
    if n == 0:
        return 0
    return len(bin(n)) - 2

def LongShiftBitsToHigh(num, shift):
    return num << shift

def LongDivMod(A, B):
    if B == 0:
        raise ValueError("Division by zero")
    k = BitLength(B)
    R = A
    Q = 0
    while R >= B:
        t = BitLength(R)
        C = LongShiftBitsToHigh(B, t - k)
        if R < C:
            t = t - 1
            C = LongShiftBitsToHigh(B, t - k)
        R = R - C
        Q = Q + (1 << (t - k))
    return Q, R

def LongPowerWindow(A, B):
    C = [1]
    D = [[1], A]

    beta = 2**32
    for i in range(2, beta):
        D.append(LongMul(D[i - 1], A))
    m = len(B) * 32
    for i in range(m - 1, -1, -1):
        b_i = (B[i // 32] >> (i % 32)) & 1
        if b_i:
            C = LongMul(C, D[b_i])
        if i != 0:
            for j in range(beta):
                C = LongMul(C, C)
    return C

def gcd_and_lcm(A, B):
    original_A, original_B = A, B
    d = 1
    while A % 2 == 0 and B % 2 == 0:
        A //= 2
        B //= 2
        d *= 2
    while A % 2 == 0:
        A //= 2
    while B != 0:
        while B % 2 == 0:
            B //= 2
        A, B = min(A, B), abs(A - B)
    gcd = d * A
    lcm = (original_A // gcd) * original_B
    return gcd, lcm

def KillLastDigits(x, counter):
    k = len(x)
    if k < counter:
        return [0]
    return x[counter:]

def ComputeMU(n):
    """Обчислює μ для алгоритму Барретта"""
    k = len(n)
    beta_2k = [0] * (2 * k) + [1]
    beta_2k_as_number = int(blocks_to_number(beta_2k), 16)
    n_as_number = int(blocks_to_number(n), 16)
    mu = beta_2k_as_number // n_as_number
    return to_base_2_32(mu)

def BarrettReduction(x, n, mu):
    k = len(n)
    #print(f'k = {k}')
    q = KillLastDigits(x, k - 1)
    #print(f'q1 = {q}')
    q = LongMul(q, mu)
    #print(f'q2 = {q}')
    q = KillLastDigits(q, k + 1)
    #print(f'q3 = {q}')
    qn = LongMul(q, n)
    #print(f'qn = {qn}')
    if len(qn) > len(x):
        qn = qn[:len(x)]
    r = LongSub(x, qn)
    #print(f'r1 = {r}')
    while LongCmp(r, n) >= 0:
        r = LongSub(r, n)
    return r

def LongAddMod(A, B, n, mu):
    C = LongAdd(A, B)
    C_mod_n = BarrettReduction(C, n, mu)
    return C_mod_n

def LongSubMod(A, B, n, mu):
    C = LongSub(A, B)
    if LongCmp(C, [0]) < 0:
        C = LongAdd(C, n)
    C_mod_n = BarrettReduction(C, n, mu)
    return C_mod_n

def LongMulMod(A, B, n, mu):
    C = LongMul(A, B)
    C_mod_n = BarrettReduction(C, n, mu)
    return C_mod_n

def LongMulSquareMod(A, n, mu):
    C = LongMul(A, A)
    C_mod_n = BarrettReduction(C, n, mu)
    return C_mod_n


def LongModPowerBarrett1(A, B, N):
    c = [1]
    counter = 0
    if LongCmp(A, N) > 0:
        A = BarrettReduction(A, N, mu)
    for i in B:
        if i == 1:
            c = BarrettReduction(c*A, N, mu)
        A = BarrettReduction(A*A, N, mu)
        counter += 1
        print(counter)
    return c


def LongModPowerBarrett(A, B, N):
    if isinstance(N, int):
        N = to_base_2_32(N)
    if isinstance(B, int):
        B = [int(bit) for bit in bin(B)[2:]]
    mu = ComputeMU(N)
    c = [1]
    if LongCmp(A, N) > 0:
        A = BarrettReduction(A, N, mu)
    for bit in reversed(B):
        if bit == 1:
            c = LongMulMod(c, A, N, mu)
        A = LongMulSquareMod(A, N, mu)
    return c


print('------------------------Test_2------------------------')

num1 = 0x64f2f304f9dc8c27eb8fb1ae60a48e908c5a093ea94550ed833ba190aa0ce727be42b
num2 = 0x4f89d34fe242dc2290022ae1697c9111311b6cd07e67e6192da1c689a571c981f3747
mod = 0x2176e5552a5da631a626eacee24d370a898a05eaea461bdfb5f8d127d1672c4078a95



a = to_base_2_32(num1)
b = to_base_2_32(num2)
b1 = [int(bit) for bit in bin(num2)[2:]]
n = to_base_2_32(mod)
mu = ComputeMU(n)

#print(f'a = {a}')
#print(f'b = {b}')
#print(f'n = {n}')
#print(f'mu = {mu}')

#resAdd = LongAdd(a, b, w = 32)
#resHexAdd = blocks_to_number(resAdd)

#resSub = LongSub(a, b, w = 32)
#resHexSub = blocks_to_number(resSub)

#resMult = LongMul(a, b)
#resHexMul = blocks_to_number(resMult)

#resDiv = LongDivMod(a, b)
#q = LongDivMod(a, b)[0]
#r = LongDivMod(a, b)[1]

gcd, lcm = gcd_and_lcm(num1, num2)

gcd_blocks = to_base_2_32(gcd)
lcm_blocks = to_base_2_32(lcm)
gcd_from_blocks = blocks_to_number(gcd_blocks)
lcm_from_blocks = blocks_to_number(lcm_blocks)

#print('A + B:', resHexAdd)
#print('A - B:', resHexSub)
#print('A х B:', resHexMul)
#print('Ціла частка Q від A / B:', blocks_to_number(q))
#print('Остача R від A / B:', blocks_to_number(r))

print(f"НСД: {gcd_from_blocks}")
print(f"НСК: {lcm_from_blocks}")

result_add = LongAddMod(a, b, n, mu)
result_add_number = blocks_to_number(result_add)
print("Результат додавання за модулем:")
print(f"(num1 + num2) mod n: {result_add_number}\n")

result_sub = LongSubMod(a, b, n, mu)
result_sub_number = blocks_to_number(result_sub)
print("Результат віднімання за модулем:")
print(f"(num1 - num2) mod n: {result_sub_number}\n")

result_mul = LongMulMod(a, b, n, mu)
result_mul_number = blocks_to_number(result_mul)
print("Результат множення за модулем:")
print(f"(num1 * num2) mod n: {result_mul_number}\n")

result_square = LongMulSquareMod(a, n, mu)
result_square_number = blocks_to_number(result_square)
print("Результат піднесення до квадрату за модулем:")
print(f"(num1^2) mod n: {result_square_number}\n")

#result_power = LongModPowerBarrett(a, b1, n)
#result_power_hex = blocks_to_number(result_power)
#print("Результат піднесення до степеня за модулем:")
#print(f"(num1^num2) mod n: {result_power_hex}\n")

def measure_time(func, *args):
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    return end - start

def benchmark_operations(a, b, n, mu, num_trials=10):
    times = {
        "Addition": [],
        "Subtraction": [],
        "Multiplication": [],
        "Square": [],
        #"Power": [],
        "GCD": [],
        "LCM": []
    }

    for _ in range(num_trials):
        time_add = measure_time(LongAddMod, a, b, n, mu)
        times["Addition"].append(time_add)

    for _ in range(num_trials):
        time_sub = measure_time(LongSubMod, a, b, n, mu)
        times["Subtraction"].append(time_sub)

    for _ in range(num_trials):
        time_mul = measure_time(LongMulMod, a, b, n, mu)
        times["Multiplication"].append(time_mul)

    for _ in range(num_trials):
        time_square = measure_time(LongMulSquareMod, a, n, mu)
        times["Square"].append(time_square)

    #for _ in range(num_trials):
    #    time_power = measure_time(LongModPowerBarrett, a, [int(bit) for bit in bin(int('1001', 2))[2:]], n)
    #    times["Power"].append(time_power)

    for _ in range(num_trials):
        start = time.perf_counter()
        gcd, _ = gcd_and_lcm(int(blocks_to_number(a), 16), int(blocks_to_number(b), 16))
        end = time.perf_counter()
        times["GCD"].append(end - start)

    for _ in range(num_trials):
        start = time.perf_counter()
        _, _ = gcd_and_lcm(int(blocks_to_number(a), 16), int(blocks_to_number(b), 16))
        end = time.perf_counter()
        times["LCM"].append(end - start)

    avg_times = {operation: sum(times_list) / len(times_list) for operation, times_list in times.items()}

    return avg_times

avg_times = benchmark_operations(a, b, n, mu, num_trials=10)

for operation, avg_time in avg_times.items():
    print(f"Середній час для {operation}: {avg_time:.6f} секунд")

