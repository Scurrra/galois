"""
A pytest module to test the functions relating to integer factorization.

Sage:
    N = 50

    print(f"FACTORS_SMALL = [")
    for _ in range(N):
        n = randint(2, 1_000_000)
        f, m = zip(*factor(n)[:])
        print(f"    ({n}, {list(f)}, {list(m)}),")
    print("]\n")

    print(f"FACTORS_MEDIUM = [")
    for _ in range(N):
        n = randint(1_000_000, 1_000_000_000_000)
        f, m = zip(*factor(n)[:])
        print(f"    ({n}, {list(f)}, {list(m)}),")
    print("]\n")
"""
import random

import pytest
import numpy as np

import galois

FACTORS_SMALL = [
    (311633, [7, 44519], [1, 1]),
    (557246, [2, 278623], [1, 1]),
    (250995, [3, 5, 29, 577], [1, 1, 1, 1]),
    (896659, [71, 73, 173], [1, 1, 1]),
    (800640, [2, 3, 5, 139], [7, 2, 1, 1]),
    (569290, [2, 5, 56929], [1, 1, 1]),
    (181169, [17, 10657], [1, 1]),
    (689006, [2, 31, 11113], [1, 1, 1]),
    (737562, [2, 3, 7, 17, 1033], [1, 1, 1, 1, 1]),
    (99318, [2, 3, 16553], [1, 1, 1]),
    (180307, [180307], [1]),
    (425651, [67, 6353], [1, 1]),
    (387363, [3, 129121], [1, 1]),
    (580403, [47, 53, 233], [1, 1, 1]),
    (603661, [223, 2707], [1, 1]),
    (391304, [2, 41, 1193], [3, 1, 1]),
    (370987, [349, 1063], [1, 1]),
    (737214, [2, 3, 122869], [1, 1, 1]),
    (393649, [393649], [1]),
    (558339, [3, 186113], [1, 1]),
    (742312, [2, 92789], [3, 1]),
    (265963, [317, 839], [1, 1]),
    (210970, [2, 5, 17, 73], [1, 1, 2, 1]),
    (169788, [2, 3, 14149], [2, 1, 1]),
    (565630, [2, 5, 13, 19, 229], [1, 1, 1, 1, 1]),
    (701456, [2, 7, 6263], [4, 1, 1]),
    (452606, [2, 7, 11, 2939], [1, 1, 1, 1]),
    (220202, [2, 23, 4787], [1, 1, 1]),
    (977688, [2, 3, 37, 367], [3, 2, 1, 1]),
    (140195, [5, 11, 2549], [1, 1, 1]),
    (647702, [2, 11, 59, 499], [1, 1, 1, 1]),
    (31971, [3, 10657], [1, 1]),
    (306659, [23, 67, 199], [1, 1, 1]),
    (521087, [7, 74441], [1, 1]),
    (684333, [3, 13, 5849], [2, 1, 1]),
    (352892, [2, 88223], [2, 1]),
    (206240, [2, 5, 1289], [5, 1, 1]),
    (840130, [2, 5, 29, 2897], [1, 1, 1, 1]),
    (46036, [2, 17, 677], [2, 1, 1]),
    (811502, [2, 47, 89, 97], [1, 1, 1, 1]),
    (107620, [2, 5, 5381], [2, 1, 1]),
    (258387, [3, 43, 2003], [1, 1, 1]),
    (671122, [2, 61, 5501], [1, 1, 1]),
    (702320, [2, 5, 8779], [4, 1, 1]),
    (888111, [3, 7, 37, 127], [3, 1, 1, 1]),
    (212801, [212801], [1]),
    (277578, [2, 3, 7, 2203], [1, 2, 1, 1]),
    (928254, [2, 3, 71, 2179], [1, 1, 1, 1]),
    (714366, [2, 3, 13229], [1, 3, 1]),
    (651499, [449, 1451], [1, 1]),
]

FACTORS_MEDIUM = [
    (424989547392, [2, 3, 16477, 67169], [7, 1, 1, 1]),
    (14255939943, [3, 7, 9059, 24979], [2, 1, 1, 1]),
    (500346285756, [2, 3, 37, 1126906049], [2, 1, 1, 1]),
    (743648733368, [2, 883, 105273037], [3, 1, 1]),
    (17443833839, [317, 55027867], [1, 1]),
    (323108387646, [2, 3, 11, 2777, 1762903], [1, 1, 1, 1, 1]),
    (381046806754, [2, 173, 17539, 62791], [1, 1, 1, 1]),
    (540050334387, [3, 113, 1593068833], [1, 1, 1]),
    (543172795718, [2, 7, 47, 463, 1782917], [1, 1, 1, 1, 1]),
    (870799330923, [3, 1459, 1483, 134153], [1, 1, 1, 1]),
    (348759549718, [2, 317, 550093927], [1, 1, 1]),
    (157258429452, [2, 3, 18253, 26591], [2, 4, 1, 1]),
    (115142777889, [3, 227, 169078969], [1, 1, 1]),
    (682648197441, [3, 7, 379, 1759, 48761], [1, 1, 1, 1, 1]),
    (557386573448, [2, 69673321681], [3, 1]),
    (176165965619, [7, 25166566517], [1, 1]),
    (211882558828, [2, 29, 37, 5741, 8599], [2, 1, 1, 1, 1]),
    (302897392260, [2, 3, 5, 1289, 3916439], [2, 1, 1, 1, 1]),
    (444313645725, [3, 5, 151, 293, 457], [1, 2, 1, 2, 1]),
    (781920595265, [5, 21767, 7184459], [1, 1, 1]),
    (651663849046, [2, 7, 157813, 294953], [1, 1, 1, 1]),
    (837306698342, [2, 37, 11314955383], [1, 1, 1]),
    (955762656818, [2, 17, 211, 317, 420271], [1, 1, 1, 1, 1]),
    (219491720231, [7, 41, 83, 9214211], [1, 1, 1, 1]),
    (964963234083, [3, 23, 163, 85797389], [1, 1, 1, 1]),
    (383295961124, [2, 23, 83, 50195909], [2, 1, 1, 1]),
    (949594363725, [3, 5, 7, 4481, 403649], [1, 2, 1, 1, 1]),
    (240996927946, [2, 23, 59, 88797689], [1, 1, 1, 1]),
    (877419240314, [2, 37, 11857016761], [1, 1, 1]),
    (901203408598, [2, 450601704299], [1, 1]),
    (995044028445, [3, 5, 787, 9365561], [3, 1, 1, 1]),
    (857650782612, [2, 3, 13, 17, 509, 635359], [2, 1, 1, 1, 1, 1]),
    (892133775786, [2, 3, 11, 59, 2111, 108529], [1, 1, 1, 1, 1, 1]),
    (268679263504, [2, 127, 132224047], [4, 1, 1]),
    (826928341477, [7, 1493, 1987, 39821], [1, 1, 1, 1]),
    (477136801822, [2, 223, 1069813457], [1, 1, 1]),
    (204194656725, [3, 5, 307, 8868389], [1, 2, 1, 1]),
    (158413967748, [2, 3, 29, 157, 966481], [2, 2, 1, 1, 1]),
    (299667379846, [2, 3407, 43978189], [1, 1, 1]),
    (892119232889, [892119232889], [1]),
    (406185311073, [3, 19, 29, 13477, 18233], [1, 1, 1, 1, 1]),
    (622036637108, [2, 263, 1931, 306209], [2, 1, 1, 1]),
    (359219830815, [3, 5, 19, 420140153], [2, 1, 1, 1]),
    (155069427776, [2, 2422959809], [6, 1]),
    (340336847001, [3, 3049, 37207483], [1, 1, 1]),
    (724208717020, [2, 5, 29, 1248635719], [2, 1, 1, 1]),
    (564236859303, [3, 13, 23, 209675533], [2, 1, 1, 1]),
    (395581390550, [2, 5, 83, 1307, 72931], [1, 2, 1, 1, 1]),
    (880686661576, [2, 13309, 8271533], [3, 1, 1]),
    (165263155482, [2, 3, 199, 239, 271, 2137], [1, 1, 1, 1, 1, 1]),
]


def test_factors_small():
    for n, factors, multiplicities in FACTORS_SMALL:
        assert galois.factors(n) == (factors, multiplicities)


def test_factors_medium():
    for n, factors, multiplicities in FACTORS_MEDIUM:
        assert galois.factors(n) == (factors, multiplicities)


def test_factors_large():
    assert galois.factors(3015341941) == ([46021, 65521], [1, 1])
    assert galois.factors(12345678) == ([2, 3, 47, 14593], [1, 2, 1, 1])


def test_factors_extremely_large():
    assert galois.factors(1000000000000000035000061) == ([1000000000000000035000061], [1])
    assert galois.factors(1000000000000000035000061 - 1) == ([2, 3, 5, 17, 19, 112850813, 457237177399], [2, 1, 1, 1, 1, 1, 1])


def test_perfect_power():
    assert galois.perfect_power(5) is None
    assert galois.perfect_power(6) is None
    assert galois.perfect_power(6*16) is None
    assert galois.perfect_power(16*125) is None

    assert galois.perfect_power(9) == (3, 2)
    assert galois.perfect_power(36) == (6, 2)
    assert galois.perfect_power(125) == (5, 3)
    assert galois.perfect_power(216) == (6, 3)


def test_trial_division():
    n = 2**4 * 17**3 * 113 * 15013
    assert galois.trial_division(n) == ([2, 17, 113, 15013], [4, 3, 1, 1], 1)
    assert galois.trial_division(n, B=500) == ([2, 17, 113], [4, 3, 1], 15013)
    assert galois.trial_division(n, B=100) == ([2, 17], [4, 3], 113*15013)


def test_pollard_p1():
    p = 1458757  # p - 1 factors: [2, 3, 13, 1039], [2, 3, 1, 1]
    q = 1326001  # q - 1 factors: [2, 3, 5, 13, 17], [4, 1, 3, 1, 1]
    assert galois.pollard_p1(p*q, 15) is None
    assert galois.pollard_p1(p*q, 19) == q
    assert galois.pollard_p1(p*q, 15, B2=100) == q

    p = 1598442007  # p - 1 factors: [2, 3, 7, 38058143], [1, 1, 1, 1]
    q = 1316659213  # q - 1 factors: [2, 3, 11, 83, 4451], [2, 4, 1, 1, 1]
    assert galois.pollard_p1(p*q, 31) is None
    assert galois.pollard_p1(p*q, 31, B2=5000) == q

    p = 1636344139  # p - 1 factors: [2, 3, 11, 13, 1381], [1, 1, 1, 1, 2]
    q = 1476638609  # q - 1 factors: [2, 137, 673649], [4, 1, 1]
    assert galois.pollard_p1(p*q, 100) is None
    assert galois.pollard_p1(p*q, 100, B2=10_000) is None

    n = 2133861346249  # n factors: [37, 41, 5471, 257107], [1, 1, 1, 1]
    assert galois.pollard_p1(n, 10) == 1517


def test_pollard_rho():
    p = 1458757
    q = 1326001
    assert galois.pollard_rho(p*q) == p
    assert galois.pollard_rho(p*q, c=4) == q

    p = 1598442007
    q = 1316659213
    assert galois.pollard_rho(p*q) == p
    assert galois.pollard_rho(p*q, c=3) == q

    p = 1636344139
    q = 1476638609
    assert galois.pollard_rho(p*q) == q
    assert galois.pollard_rho(p*q, c=6) == p


@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 5, 31, 13*7, 120, 120*7])
def test_divisors(n):
    assert galois.divisors(n) == [d for d in range(1, n + 1) if n % d == 0]
    assert galois.divisors(-n) == [d for d in range(1, abs(n) + 1) if n % d == 0]


def test_divisors_random():
    for _ in range(10):
        n = random.randint(2, 10_000)
        assert galois.divisors(n) == [d for d in range(1, n + 1) if n % d == 0]
        assert galois.divisors(-n) == [d for d in range(1, abs(n) + 1) if n % d == 0]


def test_divisors_number():
    # https://oeis.org/A000005
    d_n = [1,2,2,3,2,4,2,4,3,4,2,6,2,4,4,5,2,6,2,6,4,4,2,8,3,4,4,6,2,8,2,6,4,4,4,9,2,4,4,8,2,8,2,6,6,4,2,10,3,6,4,6,2,8,4,8,4,4,2,12,2,4,6,7,4,8,2,6,4,8,2,12,2,4,6,6,4,8,2,10,5,4,2,12,4,4,4,8,2,12,4,6,4,4,4,12,2,6,6,9,2,8,2,8]
    assert [len(galois.divisors(n)) for n in range(1, 105)] == d_n


def test_divisor_sigma():
    # https://oeis.org/A000005
    sigma_0 = [1,2,2,3,2,4,2,4,3,4,2,6,2,4,4,5,2,6,2,6,4,4,2,8,3,4,4,6,2,8,2,6,4,4,4,9,2,4,4,8,2,8,2,6,6,4,2,10,3,6,4,6,2,8,4,8,4,4,2,12,2,4,6,7,4,8,2,6,4,8,2,12,2,4,6,6,4,8,2,10,5,4,2,12,4,4,4,8,2,12,4,6,4,4,4,12,2,6,6,9,2,8,2,8]
    assert [galois.divisor_sigma(n, k=0) for n in range(1, 105)] == sigma_0

    # https://oeis.org/A000203
    sigma_1 = [1,3,4,7,6,12,8,15,13,18,12,28,14,24,24,31,18,39,20,42,32,36,24,60,31,42,40,56,30,72,32,63,48,54,48,91,38,60,56,90,42,96,44,84,78,72,48,124,57,93,72,98,54,120,72,120,80,90,60,168,62,96,104,127,84,144,68,126,96,144]
    assert [galois.divisor_sigma(n, k=1) for n in range(1, 71)] == sigma_1

    # https://oeis.org/A001157
    sigma_2 = [1,5,10,21,26,50,50,85,91,130,122,210,170,250,260,341,290,455,362,546,500,610,530,850,651,850,820,1050,842,1300,962,1365,1220,1450,1300,1911,1370,1810,1700,2210,1682,2500,1850,2562,2366,2650,2210,3410,2451,3255]
    assert [galois.divisor_sigma(n, k=2) for n in range(1, 51)] == sigma_2

    # https://oeis.org/A001158
    sigma_3 = [1,9,28,73,126,252,344,585,757,1134,1332,2044,2198,3096,3528,4681,4914,6813,6860,9198,9632,11988,12168,16380,15751,19782,20440,25112,24390,31752,29792,37449,37296,44226,43344,55261,50654,61740,61544,73710,68922,86688]
    assert [galois.divisor_sigma(n, k=3) for n in range(1, 43)] == sigma_3


def test_is_prime_power():
    # https://oeis.org/A246655
    prime_powers = np.array([2,3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31,32,37,41,43,47,49,53,59,61,64,67,71,73,79,81,83,89,97,101,103,107,109,113,121,125,127,128,131,137,139,149,151,157,163,167,169,173,179,181,191,193,197,199,211])
    n = np.arange(1, prime_powers[-1] + 1)
    is_prime_power = np.zeros(n.size, dtype=bool)
    is_prime_power[prime_powers - 1] = True  # -1 for 1-indexed
    assert [galois.is_prime_power(ni) for ni in n] == is_prime_power.tolist()


def test_is_perfect_power():
    # https://oeis.org/A001597
    perfect_powers = np.array([1,4,8,9,16,25,27,32,36,49,64,81,100,121,125,128,144,169,196,216,225,243,256,289,324,343,361,400,441,484,512,529,576,625,676,729,784,841,900,961,1000,1024,1089,1156,1225,1296,1331,1369,1444,1521,1600,1681,1728,1764])
    n = np.arange(1, perfect_powers[-1] + 1)
    is_perfect_power = np.zeros(n.size, dtype=bool)
    is_perfect_power[perfect_powers - 1] = True  # -1 for 1-indexed
    assert [galois.is_perfect_power(ni) for ni in n] == is_perfect_power.tolist()


def test_is_square_free():
    # https://oeis.org/A005117
    square_frees = np.array([1,2,3,5,6,7,10,11,13,14,15,17,19,21,22,23,26,29,30,31,33,34,35,37,38,39,41,42,43,46,47,51,53,55,57,58,59,61,62,65,66,67,69,70,71,73,74,77,78,79,82,83,85,86,87,89,91,93,94,95,97,101,102,103,105,106,107,109,110,111,113])
    n = np.arange(1, square_frees[-1] + 1)
    is_square_free = np.zeros(n.size, dtype=bool)
    is_square_free[square_frees - 1] = True  # -1 for 1-indexed
    assert [galois.is_square_free(ni) for ni in n] == is_square_free.tolist()


def test_is_smooth():
    # https://oeis.org/A000079
    smooths = np.array([1,2,4,8,16,32,64,128,256,512,1024])
    n = np.arange(1, smooths[-1] + 1)
    is_smooth = np.zeros(n.size, dtype=bool)
    is_smooth[smooths - 1] = True  # -1 for 1-indexed
    assert [galois.is_smooth(ni, 2) for ni in n] == is_smooth.tolist()

    # https://oeis.org/A003586
    smooths = np.array([1,2,3,4,6,8,9,12,16,18,24,27,32,36,48,54,64,72,81,96,108,128,144,162,192,216,243,256,288,324,384,432,486,512,576,648,729,768,864,972,1024])
    n = np.arange(1, smooths[-1] + 1)
    is_smooth = np.zeros(n.size, dtype=bool)
    is_smooth[smooths - 1] = True  # -1 for 1-indexed
    assert [galois.is_smooth(ni, 3) for ni in n] == is_smooth.tolist()

    # https://oeis.org/A051037
    smooths = np.array([1,2,3,4,5,6,8,9,10,12,15,16,18,20,24,25,27,30,32,36,40,45,48,50,54,60,64,72,75,80,81,90,96,100,108,120,125,128,135,144,150,160,162,180,192,200,216,225,240,243,250,256,270,288,300,320,324,360,375,384,400,405])
    n = np.arange(1, smooths[-1] + 1)
    is_smooth = np.zeros(n.size, dtype=bool)
    is_smooth[smooths - 1] = True  # -1 for 1-indexed
    assert [galois.is_smooth(ni, 5) for ni in n] == is_smooth.tolist()

    # https://oeis.org/A002473
    smooths = np.array([1,2,3,4,5,6,7,8,9,10,12,14,15,16,18,20,21,24,25,27,28,30,32,35,36,40,42,45,48,49,50,54,56,60,63,64,70,72,75,80,81,84,90,96,98,100,105,108,112,120,125,126,128,135,140,144,147,150,160,162,168,175,180,189,192])
    n = np.arange(1, smooths[-1] + 1)
    is_smooth = np.zeros(n.size, dtype=bool)
    is_smooth[smooths - 1] = True  # -1 for 1-indexed
    assert [galois.is_smooth(ni, 7) for ni in n] == is_smooth.tolist()

    # https://oeis.org/A018336
    smooths = np.array([1,2,3,5,6,7,10,14,15,21,30,35,42,70,105,210])
    n = np.arange(1, smooths[-1] + 1)
    is_smooth = np.zeros(n.size, dtype=bool)
    is_smooth[smooths - 1] = True  # -1 for 1-indexed
    assert [galois.is_smooth(ni, 7) and galois.is_square_free(ni) for ni in n] == is_smooth.tolist()

    # https://oeis.org/A051038
    smooths = np.array([1,2,3,4,5,6,7,8,9,10,11,12,14,15,16,18,20,21,22,24,25,27,28,30,32,33,35,36,40,42,44,45,48,49,50,54,55,56,60,63,64,66,70,72,75,77,80,81,84,88,90,96,98,99,100,105,108,110,112,120,121,125,126,128,132,135,140])
    n = np.arange(1, smooths[-1] + 1)
    is_smooth = np.zeros(n.size, dtype=bool)
    is_smooth[smooths - 1] = True  # -1 for 1-indexed
    assert [galois.is_smooth(ni, 11) for ni in n] == is_smooth.tolist()

    # https://oeis.org/A051038
    smooths = np.array([1,2,3,4,5,6,7,8,9,10,11,12,14,15,16,18,20,21,22,24,25,27,28,30,32,33,35,36,40,42,44,45,48,49,50,54,55,56,60,63,64,66,70,72,75,77,80,81,84,88,90,96,98,99,100,105,108,110,112,120,121,125,126,128,132,135,140])
    n = np.arange(1, smooths[-1] + 1)
    is_smooth = np.zeros(n.size, dtype=bool)
    is_smooth[smooths - 1] = True  # -1 for 1-indexed
    assert [galois.is_smooth(ni, 11) for ni in n] == is_smooth.tolist()

    # https://oeis.org/A087005
    smooths = np.array([1,2,3,5,6,7,10,11,14,15,21,22,30,33,35,42,55,66,70,77,105,110,154,165,210,231,330,385,462,770,1155,2310])
    n = np.arange(1, smooths[-1] + 1)
    is_smooth = np.zeros(n.size, dtype=bool)
    is_smooth[smooths - 1] = True  # -1 for 1-indexed
    assert [galois.is_smooth(ni, 11) and galois.is_square_free(ni) for ni in n] == is_smooth.tolist()


def test_is_powersmooth():
    assert galois.is_powersmooth(2**4 * 3**2 * 5, 5) == False
    assert galois.is_powersmooth(2**4 * 3**2 * 5, 9) == False
    assert galois.is_powersmooth(2**4 * 3**2 * 5, 16) == True

    assert galois.is_powersmooth(2**4 * 3**2 * 5*3, 5) == False
    assert galois.is_powersmooth(2**4 * 3**2 * 5*3, 25) == False
    assert galois.is_powersmooth(2**4 * 3**2 * 5*3, 125) == True

    assert galois.is_powersmooth(13 * 23, 4) == False

    for n in range(2, 1_000):
        p, e = galois.factors(n)
        assert all([pi**ei <= 50 for pi, ei in zip(p, e)]) == galois.is_powersmooth(n, 50)
