"""
A pytest module to test the Fibonacci LFSR implementation.
"""
import pytest
import numpy as np

import galois


def test_exceptions():
    c = galois.primitive_poly(7, 4)

    with pytest.raises(TypeError):
        galois.FLFSR(c.reverse().coeffs)
    with pytest.raises(TypeError):
        galois.FLFSR(c.reverse(), state=1)


def test_repr():
    c = galois.primitive_poly(7, 4)
    lfsr = galois.FLFSR(c.reverse())
    assert repr(lfsr) == "<Fibonacci LFSR: f(x) = 5x^4 + 3x^3 + x^2 + 1 over GF(7)>"


def test_str():
    c = galois.primitive_poly(7, 4)
    lfsr = galois.FLFSR(c.reverse())
    assert str(lfsr) == "Fibonacci LFSR:\n  field: GF(7)\n  feedback_poly: 5x^4 + 3x^3 + x^2 + 1\n  characteristic_poly: x^4 + x^2 + 3x + 5\n  taps: [0, 6, 4, 2]\n  order: 4\n  state: [1, 1, 1, 1]\n  initial_state: [1, 1, 1, 1]"


def test_initial_state():
    c = galois.primitive_poly(7, 4)

    default_state = [1, 1, 1, 1]
    lfsr = galois.FLFSR(c.reverse())
    assert np.array_equal(lfsr.initial_state, default_state)
    assert np.array_equal(lfsr.state, default_state)

    state = [1, 2, 3, 4]
    lfsr = galois.FLFSR(c.reverse(), state=state)
    assert np.array_equal(lfsr.initial_state, state)
    assert np.array_equal(lfsr.state, state)


def test_feedback_and_characteristic_poly():
    c = galois.primitive_poly(7, 4)
    f = c.reverse()
    lfsr = galois.FLFSR(f)
    assert lfsr.feedback_poly == f
    assert lfsr.characteristic_poly == c
    assert lfsr.feedback_poly == lfsr.characteristic_poly.reverse()


def test_reset_exceptions():
    c = galois.primitive_poly(7, 4)
    lfsr = galois.FLFSR(c.reverse())

    with pytest.raises(TypeError):
        lfsr.reset(1)


def test_reset_initial_state():
    c = galois.primitive_poly(7, 4)
    lfsr = galois.FLFSR(c.reverse())

    assert np.array_equal(lfsr.state, lfsr.initial_state)
    lfsr.step(10)
    assert not np.array_equal(lfsr.state, lfsr.initial_state)
    lfsr.reset()
    assert np.array_equal(lfsr.state, lfsr.initial_state)


def test_reset_specific_state():
    c = galois.primitive_poly(7, 4)
    lfsr = galois.FLFSR(c.reverse())
    state = [1, 2, 3, 4]

    assert not np.array_equal(lfsr.state, state)
    lfsr.reset(state)
    assert np.array_equal(lfsr.state, state)


def test_step_exceptions():
    c = galois.primitive_poly(7, 4)
    lfsr = galois.FLFSR(c.reverse())

    with pytest.raises(TypeError):
        lfsr.step(10.0)


def test_step_zero():
    c = galois.primitive_poly(7, 4)
    lfsr = galois.FLFSR(c.reverse())

    y = lfsr.step(0)
    assert y.size == 0
    assert type(y) is lfsr.field


def test_step_forwards_backwards():
    c = galois.primitive_poly(7, 4)
    lfsr = galois.FLFSR(c.reverse())

    y_forward = lfsr.step(10)
    y_reverse = lfsr.step(-10)

    assert np.array_equal(y_forward, y_reverse[::-1])
    assert np.array_equal(lfsr.state, lfsr.initial_state)


def test_step_backwards_forwards():
    c = galois.primitive_poly(7, 4)
    lfsr = galois.FLFSR(c.reverse())

    y_reverse = lfsr.step(-10)
    y_forward = lfsr.step(10)

    assert np.array_equal(y_reverse, y_forward[::-1])
    assert np.array_equal(lfsr.state, lfsr.initial_state)


def test_step_output_reversed_state():
    c = galois.primitive_poly(7, 4)
    state = [1, 2, 3, 4]
    lfsr = galois.FLFSR(c.reverse(), state=state)

    y = lfsr.step(4)
    assert np.array_equal(y, state[::-1])


def test_step_gf2_primitive():
    """
    Python:
        c = galois.primitive_poly(2, 4); c
        key = -c.coeffs[1:][::-1]; key

    Sage:
        F = GF(2)
        key = [1, 1, 0, 0]  # c(x) = x^4 + x + 1
        fill = [1, 1, 1, 1]
        key = [F(k) for k in key]
        fill = [F(f) for f in fill]
        s = lfsr_sequence(key, fill, 50)
        print(s)
    """
    GF = galois.GF(2)
    key = GF([1, 1, 0, 0])
    key = -key[::-1]; key = np.insert(key, 0, 1)  # Convert to c(x)
    c = galois.Poly(key)
    state = GF([1, 1, 1, 1])
    y_truth = GF([1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0])

    lfsr = galois.FLFSR(c.reverse(), state=state)
    y = lfsr.step(50)

    assert np.array_equal(y, y_truth)
    assert type(y) is lfsr.field


def test_step_gf3_primitive():
    """
    Python:
        c = galois.primitive_poly(3, 4); c
        key = -c.coeffs[1:][::-1]; key

    Sage:
        F = GF(3)
        key = [1, 2, 0, 0]  # c(x) = x^4 + x + 2
        fill = [1, 1, 1, 1]
        key = [F(k) for k in key]
        fill = [F(f) for f in fill]
        s = lfsr_sequence(key, fill, 50)
        print(s)
    """
    GF = galois.GF(3)
    key = GF([1, 2, 0, 0])
    key = -key[::-1]; key = np.insert(key, 0, 1)  # Convert to c(x)
    c = galois.Poly(key)
    state = GF([1, 1, 1, 1])
    y_truth = GF([1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 2, 1, 0, 1, 1, 1, 2, 0, 0, 2, 2, 0, 1, 0, 2, 2, 1, 1, 0, 1, 0, 1, 2, 1, 2, 2, 1, 2, 0, 1, 2, 2, 2, 2, 0, 0, 0, 2, 0, 0])

    lfsr = galois.FLFSR(c.reverse(), state=state)
    y = lfsr.step(50)

    assert np.array_equal(y, y_truth)
    assert type(y) is lfsr.field


def test_step_gf2_3_primitive():
    """
    Python:
        c = galois.primitive_poly(2**3, 4); c
        key = -c.coeffs[1:][::-1]; key

    Sage:
        F = GF(2^3, repr="int")
        key = [3, 1, 0, 0]  # c(x) = x^4 + x + 3
        fill = [1, 1, 1, 1]
        key = [F.fetch_int(k) for k in key]
        fill = [F.fetch_int(f) for f in fill]
        s = lfsr_sequence(key, fill, 50)
        print(s)
    """
    GF = galois.GF(2**3)
    key = GF([3, 1, 0, 0])
    key = -key[::-1]; key = np.insert(key, 0, 1)  # Convert to c(x)
    c = galois.Poly(key)
    state = GF([1, 1, 1, 1])
    y_truth = GF([1, 1, 1, 1, 2, 2, 2, 1, 4, 4, 7, 7, 3, 0, 5, 1, 5, 5, 5, 6, 1, 1, 2, 0, 2, 1, 6, 2, 7, 5, 3, 1, 7, 7, 4, 4, 5, 6, 3, 2, 2, 2, 7, 4, 4, 1, 6, 3, 6, 5])

    lfsr = galois.FLFSR(c.reverse(), state=state)
    y = lfsr.step(50)

    assert np.array_equal(y, y_truth)
    assert type(y) is lfsr.field


def test_step_gf3_3_primitive():
    """
    Python:
        c = galois.primitive_poly(3**3, 4); c
        key = -c.coeffs[1:][::-1]; key

    Sage:
        F = GF(3^3, repr="int")
        key = [20, 2, 0, 0]  # c(x) = x^4 + x + 10
        fill = [1, 1, 1, 1]
        key = [F.fetch_int(k) for k in key]
        fill = [F.fetch_int(f) for f in fill]
        s = lfsr_sequence(key, fill, 50)
        print(s)
    """
    GF = galois.GF(3**3)
    key = GF([20, 2, 0, 0])
    key = -key[::-1]; key = np.insert(key, 0, 1)  # Convert to c(x)
    c = galois.Poly(key)
    state = GF([1, 1, 1, 1])
    y_truth = GF([1, 1, 1, 1, 19, 19, 19, 1, 25, 25, 16, 4, 24, 6, 6, 6, 26, 2, 2, 9, 4, 11, 1, 11, 13, 21, 9, 9, 12, 10, 3, 0, 6, 2, 4, 3, 6, 15, 18, 7, 20, 20, 20, 8, 17, 17, 2, 1, 13, 19])

    lfsr = galois.FLFSR(c.reverse(), state=state)
    y = lfsr.step(50)

    assert np.array_equal(y, y_truth)
    assert type(y) is lfsr.field


def test_step_gf2_reducible():
    """
    Python:
        GF = galois.GF(2)
        coeffs = GF.Random(5)
        coeffs[0] = 1
        coeffs[-1] = GF.Random(low=1)
        c = galois.Poly(coeffs)
        assert not galois.is_irreducible(c)
        key = -coeffs[1:][::-1]
        c
        key

    Sage:
        F = GF(2)
        key = [1, 0, 0, 0]  # c(x) = x^4 + 1
        fill = [1, 1, 1, 1]
        key = [F(k) for k in key]
        fill = [F(f) for f in fill]
        s = lfsr_sequence(key, fill, 50)
        print(s)
    """
    GF = galois.GF(2)
    key = GF([1, 0, 0, 0])
    key = -key[::-1]; key = np.insert(key, 0, 1)  # Convert to c(x)
    c = galois.Poly(key)
    state = GF([1, 1, 1, 1])
    y_truth = GF([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    lfsr = galois.FLFSR(c.reverse(), state=state)
    y = lfsr.step(50)

    assert np.array_equal(y, y_truth)
    assert type(y) is lfsr.field


def test_step_gf3_reducible():
    """
    Python:
        GF = galois.GF(3)
        coeffs = GF.Random(5)
        coeffs[0] = 1
        coeffs[-1] = GF.Random(low=1)
        c = galois.Poly(coeffs)
        assert not galois.is_irreducible(c)
        key = -coeffs[1:][::-1]
        c
        key

    Sage:
        F = GF(3)
        key = [1, 2, 2, 1]  # c(x) = x^4 + x^3 + 2x^2 + 2x + 1
        fill = [1, 1, 1, 1]
        key = [F(k) for k in key]
        fill = [F(f) for f in fill]
        s = lfsr_sequence(key, fill, 50)
        print(s)
    """
    GF = galois.GF(3)
    key = GF([1, 2, 2, 1])
    key = -key[::-1]; key = np.insert(key, 0, 1)  # Convert to c(x)
    c = galois.Poly(key)
    state = GF([1, 1, 1, 1])
    y_truth = GF([1, 1, 1, 1, 0, 2, 2, 1, 0, 2, 0, 2, 0, 0, 1, 0, 2, 1, 0, 0, 1, 2, 1, 1, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 2, 1, 2, 1, 0, 1, 2, 2, 2, 2, 0, 1, 1, 2, 0, 1])

    lfsr = galois.FLFSR(c.reverse(), state=state)
    y = lfsr.step(50)

    assert np.array_equal(y, y_truth)
    assert type(y) is lfsr.field


def test_step_gf2_3_reducible():
    """
    Python:
        GF = galois.GF(2**3)
        coeffs = GF.Random(5)
        coeffs[0] = 1
        coeffs[-1] = GF.Random(low=1)
        c = galois.Poly(coeffs)
        assert not galois.is_irreducible(c)
        key = -coeffs[1:][::-1]
        c
        key

    Sage:
        F = GF(2^3, repr="int")
        key = [4, 1, 1, 5]  # c(x) = x^4 + 5x^3 + x^2 + x + 4
        fill = [1, 1, 1, 1]
        key = [F.fetch_int(k) for k in key]
        fill = [F.fetch_int(f) for f in fill]
        s = lfsr_sequence(key, fill, 50)
        print(s)
    """
    GF = galois.GF(2**3)
    key = GF([4, 1, 1, 5])
    key = -key[::-1]; key = np.insert(key, 0, 1)  # Convert to c(x)
    c = galois.Poly(key)
    state = GF([1, 1, 1, 1])
    y_truth = GF([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    lfsr = galois.FLFSR(c.reverse(), state=state)
    y = lfsr.step(50)

    assert np.array_equal(y, y_truth)
    assert type(y) is lfsr.field


def test_step_gf3_3_reducible():
    """
    Python:
        GF = galois.GF(3**3)
        coeffs = GF.Random(5)
        coeffs[0] = 1
        coeffs[-1] = GF.Random(low=1)
        c = galois.Poly(coeffs)
        assert not galois.is_irreducible(c)
        key = -coeffs[1:][::-1]
        c
        key

    Sage:
        F = GF(3^3, repr="int")
        key = [5, 20, 23, 5]  # c(x) = x^4 + 5x^3 + 23x^2 + 20x + 5
        fill = [1, 1, 1, 1]
        key = [F.fetch_int(k) for k in key]
        fill = [F.fetch_int(f) for f in fill]
        s = lfsr_sequence(key, fill, 50)
        print(s)
    """
    GF = galois.GF(3**3)
    key = GF([5, 20, 23, 5])
    key = -key[::-1]; key = np.insert(key, 0, 1)  # Convert to c(x)
    c = galois.Poly(key)
    state = GF([1, 1, 1, 1])
    y_truth = GF([1, 1, 1, 1, 11, 6, 1, 16, 20, 13, 6, 13, 2, 9, 18, 8, 21, 6, 12, 6, 3, 3, 26, 7, 22, 16, 23, 13, 5, 6, 1, 7, 19, 3, 12, 16, 14, 16, 17, 6, 0, 24, 9, 26, 6, 23, 3, 22, 21, 8])

    lfsr = galois.FLFSR(c.reverse(), state=state)
    y = lfsr.step(50)

    assert np.array_equal(y, y_truth)
    assert type(y) is lfsr.field


@pytest.mark.parametrize("order", [2, 3, 2**3, 3**3])
def test_to_galois_lfsr_primitive(order):
    c = galois.primitive_poly(order, 4)

    fibonacci_lfsr = galois.FLFSR(c.reverse())
    galois_lfsr = fibonacci_lfsr.to_galois_lfsr()

    y1 = fibonacci_lfsr.step(100)
    y2 = galois_lfsr.step(100)

    assert np.array_equal(y1, y2)


@pytest.mark.parametrize("order", [2, 3, 2**3, 3**3])
def test_to_galois_lfsr_reducible(order):
    GF = galois.GF(order)
    while True:
        coeffs = GF.Random(5)
        coeffs[0] = 1
        coeffs[-1] = GF.Random(low=1)
        c = galois.Poly(coeffs)
        if not galois.is_irreducible(c):
            break

    fibonacci_lfsr = galois.FLFSR(c.reverse())
    galois_lfsr = fibonacci_lfsr.to_galois_lfsr()

    y1 = fibonacci_lfsr.step(100)
    y2 = galois_lfsr.step(100)

    assert np.array_equal(y1, y2)
