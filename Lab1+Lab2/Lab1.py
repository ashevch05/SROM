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
    return C

def LongShiftDigitsToHigh(A, shift):
    n = len(A)
    C = [0] * (n + shift)

    for i in range(n):
        C[i + shift] = A[i]
    return C

def LongMul(A, B):
    n = len(A)
    C = [0] * (2 * n)

    for i in range(n):
        temp = LongMulOneDigit(A, B[i])
        temp = LongShiftDigitsToHigh(temp, i)
        C = LongAdd(C, temp)

    return C

def BitLength(A):
    for i in range(len(A) - 1, -1, -1):
        if A[i] != 0:
            return (len(A) - i) * 32
    return 0


def LongDivMod(A, B):
    l = len(A)
    k = BitLength(B)
    R = A[:]
    Q = [0] * l

    while len(R) > 0 and LongCmp(R, B) >= 0:
        t = BitLength(R)
        C = LongShiftDigitsToHigh(B, t - k)
        if LongCmp(R, C) < 0:
            t -= 1
            C = LongShiftDigitsToHigh(B, t - k)
        R = LongAdd(R, [-x for x in C])
        if len(R) > 0 and R[-1] == 0:
            R.pop()
        Q_bit = [0] * ((t - k) // 32) + [1 << ((t - k) % 32)]
        Q = LongAdd(Q, Q_bit)
    return Q, R

def LongPowerWindow(A, B):
    C = [1]
    D = [[1], A]

    beta = 2**3
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



print('------------------------Test_1------------------------')

num1 = 0x8757f99544f43491b665a551f57eaf5b03941e9f708a4c1082cd47f3aae8d32e65d862a0611df5e764d6289467bc2ae3229feadce4a2ab20fff0882b77e96ae5940094ce2c5237826e3716f2389be8b90123686d879e52c698f956d7bb995f9ecd573fee352927ed1c3f5b33fae4dd2ba84ec7fd49e5acfd5565f869ef170615d4b77fe6e529aceb28f965348b9d499a60e113a32b4310a8aac859109cd42b55fe094a80ff0949a98e6a38d90c1173941c17867121da5d18a00b54c20f32423b09ed89a7392d5ebc19eaa0d60c8a62ffe4802de933a961b15e8220d648985e125fdceb335069bbcdf7f6d558faa92338b8b3fa6efbeb3ef635142f52a987d75f
num2 = 0x419c6d4cf942e5eea174cbc10402340b68dd708b2d4f589e6afb1b4d5b2480090c65609ebce49462cc582f11b33e13fec483de80d608dbbc4375cd6217a27af7dce22d2109048da4bebd4780e8e169b6cf457228a5741a1fc6b85bc97a5d48e0c8a4eb29f5a051daaf3eec89ac9cd64d150c1e1fcd9cb733efa92d98da0b186ce6469d80b786204e8afa00994d955be08a9b621a31e06cf965a0dce8e3635b8b40473eec13ddce685f413ee133672ee77139eae0caa70847a21e609bb28f5d4bac43a3821788a7ab2c7cbc33b380654722e0745943bb369d74ce9b9c5cc40a582676bd5b8c89ef86cae3758a5ef2bac35aace86e82674c02e0b67554b0dbcc3


a = to_base_2_32(num1)
b = to_base_2_32(num2)

resAdd = LongAdd(a, b, w = 32)
resHexAdd = blocks_to_number(resAdd)

resSub = LongSub(a, b, w = 32)
resHexSub = blocks_to_number(resSub)

resMult = LongMul(a, b)
resHexMul = blocks_to_number(resMult)

resDiv = LongDivMod(a, b)
q = LongDivMod(a, b)[0]
r = LongDivMod(a, b)[1]

print('A + B:', resHexAdd)
print('A - B:',resHexSub)
print('A х B:',resHexMul)
print('Ціла частка Q від A / B:',blocks_to_number(q))
print('Остача R від A / B:', blocks_to_number(r))



print('------------------------Test_2------------------------')

num1 = 0x64f2f304f9dc8c27eb8fb1ae60a48e908c5a093ea94550ed833ba190aa0ce727be42b
num2 = 0x4f89d34fe242dc2290022ae1697c9111311b6cd07e67e6192da1c689a571c981f3747

a = to_base_2_32(num1)
b = to_base_2_32(num2)

resAdd = LongAdd(a, b, w = 32)
resHexAdd = blocks_to_number(resAdd)

resSub = LongSub(a, b, w = 32)
resHexSub = blocks_to_number(resSub)

resMult = LongMul(a, b)
resHexMul = blocks_to_number(resMult)

resDiv = LongDivMod(a, b)
q = LongDivMod(a, b)[0]
r = LongDivMod(a, b)[1]

print('A + B:', resHexAdd)
print('A - B:',resHexSub)
print('A х B:',resHexMul)
print('Ціла частка Q від A / B:',blocks_to_number(q))
print('Остача R від A / B:', blocks_to_number(r))



print('------------------------Test_3------------------------')

def test_associativity():
    num_a = 0xa7d4e8f1b2c3d9e5f6a8b7c4d2e3f5a6b8c9d7e4f1a2b3c5d6e8f9a7b4c2d3e5f6a8
    num_b = 0xf1e2d3c4b5a6987654321fedcba9876543210abcdef123456789abcdef0123456789
    num_c = 0x123456789abcdef0fedcba98765432100123456789abcdeffedcba9876543210fedc

    a = to_base_2_32(num_a)
    b = to_base_2_32(num_b)
    c = to_base_2_32(num_c)

    ab = LongAdd(a, b)
    left_1 = LongMul(ab, c)
    left_2 = LongMul(c, ab)

    ac = LongMul(a, c)
    bc = LongMul(b, c)
    right = LongAdd(ac, bc)

    assert left_1 == left_2 == right, "Associativity failed!"
    print("Associativity test passed.")

test_associativity()



print('------------------------Time_Testing------------------------')


def measure_time(func, *args):
    start_time = time.time() 
    result = func(*args)     
    end_time = time.time()    
    execution_time = end_time - start_time  
    return result, execution_time


num1 = 0x8757f99544f43491b665a551f57eaf5b03941e9f708a4c1082cd47f3aae8d32e65d862a0611df5e764d6289467bc2ae3229feadce4a2ab20fff0882b77e96ae5940094ce2c5237826e3716f2389be8b90123686d879e52c698f956d7bb995f9ecd573fee352927ed1c3f5b33fae4dd2ba84ec7fd49e5acfd5565f869ef170615d4b77fe6e529aceb28f965348b9d499a60e113a32b4310a8aac859109cd42b55fe094a80ff0949a98e6a38d90c1173941c17867121da5d18a00b54c20f32423b09ed89a7392d5ebc19eaa0d60c8a62ffe4802de933a961b15e8220d648985e125fdceb335069bbcdf7f6d558faa92338b8b3fa6efbeb3ef635142f52a987d75f
num2 = 0x419c6d4cf942e5eea174cbc10402340b68dd708b2d4f589e6afb1b4d5b2480090c65609ebce49462cc582f11b33e13fec483de80d608dbbc4375cd6217a27af7dce22d2109048da4bebd4780e8e169b6cf457228a5741a1fc6b85bc97a5d48e0c8a4eb29f5a051daaf3eec89ac9cd64d150c1e1fcd9cb733efa92d98da0b186ce6469d80b786204e8afa00994d955be08a9b621a31e06cf965a0dce8e3635b8b40473eec13ddce685f413ee133672ee77139eae0caa70847a21e609bb28f5d4bac43a3821788a7ab2c7cbc33b380654722e0745943bb369d74ce9b9c5cc40a582676bd5b8c89ef86cae3758a5ef2bac35aace86e82674c02e0b67554b0dbcc3

a = to_base_2_32(num1)
b = to_base_2_32(num2)

resAdd, timeAdd = measure_time(LongAdd, a, b)
resHexAdd = blocks_to_number(resAdd)

resSub, timeSub = measure_time(LongSub, a, b)
resHexSub = blocks_to_number(resSub)

resMult, timeMult = measure_time(LongMul, a, b)
resHexMul = blocks_to_number(resMult)

q, r = LongDivMod(a, b)
resDiv, timeDiv = measure_time(LongDivMod, a, b)

print('A + B:', resHexAdd)
print('Час виконання A + B:', timeAdd)

print('A - B:', resHexSub)
print('Час виконання A - B:', timeSub)

print('A х B:', resHexMul)
print('Час виконання A х B:', timeMult)

print('Ціла частка Q від A / B:', blocks_to_number(q))
print('Остача R від A / B:', blocks_to_number(r))
print('Час виконання A / B:', timeDiv)
