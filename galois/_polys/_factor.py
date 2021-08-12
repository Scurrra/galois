"""
A module containing routines for polynomial factorization.
"""
import random

import numpy as np

from .._overrides import set_module

from ._checks import is_monic
from ._functions import poly_gcd, poly_pow
from ._poly import Poly

__all__ = ["poly_factors", "square_free_factorization", "distinct_degree_factorization", "equal_degree_factorization"]


@set_module("galois")
def poly_factors(poly):
    r"""
    Factors the polynomial :math:`f(x)` into a product of irreducible factors :math:`f(x) = g_1(x)^{e_1} g_2(x)^{e_2} \dots g_k(x)^{e_k}`.

    This function implements the Square-Free Factorization algorithm.

    Parameters
    ----------
    poly : galois.Poly
        The polynomial :math:`f(x)` over :math:`\mathrm{GF}(p^m)` to be factored.

    Returns
    -------
    list
        The list of :math:`k` polynomial factors :math:`\{g_1(x), g_2(x), \dots, g_k(x)\}` sorted in increasing lexicographic order.
    list
        The list of corresponding multiplicities :math:`\{e_1, e_2, \dots, e_k\}`.

    References
    ----------
    * D. Hachenberger, D. Jungnickel. Topics in Galois Fields. Algorithm 6.1.7.

    Examples
    --------
    .. ipython:: python

        GF = galois.GF2
        # Ensure the factors are irreducible by using Conway polynomials
        g1, g2, g3 = galois.conway_poly(2, 3), galois.conway_poly(2, 4), galois.conway_poly(2, 5)
        g1, g2, g3
        e1, e2, e3 = 4, 3, 2
        # Construct the composite polynomial
        f = g1**e1 * g2**e2 * g3**e3
        galois.poly_factors(f)

    .. ipython:: python

        GF = galois.GF(3)
        # Ensure the factors are irreducible by using Conway polynomials
        g1, g2, g3 = galois.conway_poly(3, 3), galois.conway_poly(3, 4), galois.conway_poly(3, 5)
        g1, g2, g3
        e1, e2, e3 = 5, 4, 3
        # Construct the composite polynomial
        f = g1**e1 * g2**e2 * g3**e3
        galois.poly_factors(f)
    """
    if not isinstance(poly, Poly):
        raise TypeError(f"Argument `poly` must be a galois.Poly, not {type(poly)}.")

    field = poly.field
    p = field.characteristic
    one = Poly.One(field=field)

    L = Poly.One(field=field)
    r = 0
    factors_ = []
    multiplicities = []

    if not is_monic(poly):
        factors_.append(Poly(poly.coeffs[0], field=field))
        multiplicities.append(1)
        poly /= poly.coeffs[0]

    def SFF(c, r):
        nonlocal L, factors_, multiplicities
        i = 1
        a = c.copy()
        b = c.derivative()
        d = poly_gcd(a, b)
        w = a / d

        while w != one:
            y = poly_gcd(w, d)
            z = w / y
            if z != one and i % p != 0:
                L *= z**(i * p**r)
                factors_.append(z)
                multiplicities.append(i * p**r)
            i = i + 1
            w = y
            d = d / y

        return d

    d = SFF(poly, r)

    while d != one:
        degrees = [degree // p for degree in d.degrees]
        coeffs = d.coeffs
        delta = Poly.Degrees(degrees, coeffs=coeffs, field=field)  # The p-th root of d(x)
        r += 1
        d = SFF(delta, r)

    # Sort the factor in lexicographically-increasing order
    factors_, multiplicities = zip(*sorted(zip(factors_, multiplicities), key=lambda item: item[0].integer))

    return list(factors_), list(multiplicities)


@set_module("galois")
def square_free_factorization(poly):
    r"""
    Factors the monic polynomial :math:`f(x)` into a product of square-free polynomials.

    Parameters
    ----------
    poly : galois.Poly
        A non-constant, monic polynomial :math:`f(x)` over :math:`\mathrm{GF}(p^m)`.

    Returns
    -------
    list
        The list of non-constant, square-free polynomials :math:`h_i(x)` in the factorization.
    list
        The list of corresponding multiplicities :math:`i`.

    Notes
    -----
    The Square-Free Factorization algorithm factors :math:`f(x)` into a product of :math:`m` square-free polynomials :math:`h_j(x)`
    with multiplicity :math:`j`.

    .. math::
        f(x) = \prod_{j=1}^{m} h_j(x)^j

    Some :math:`h_j(x) = 1`, but those polynomials are not returned by this function.

    A complete polynomial factorization is implemented in :func:`galois.poly_factors`.

    References
    ----------
    * D. Hachenberger, D. Jungnickel. Topics in Galois Fields. Algorithm 6.1.7.
    * Section 2.1 from https://people.csail.mit.edu/dmoshkov/courses/codes/poly-factorization.pdf

    Examples
    --------
    Suppose :math:`f(x) = x(x^3 + 2x + 4)(x^2 + 4x + 1)^3` over :math:`\mathrm{GF}(5)`. Each polynomial :math:`x`, :math:`x^3 + 2x + 4`,
    and :math:`x^2 + 4x + 1` are all irreducible over :math:`\mathrm{GF}(5)`.

    .. ipython:: python

        GF = galois.GF(5)
        a = galois.Poly([1,0], field=GF); a, galois.is_irreducible(a)
        b = galois.Poly([1,0,2,4], field=GF); b, galois.is_irreducible(b)
        c = galois.Poly([1,4,1], field=GF); c, galois.is_irreducible(c)
        f = a * b * c**3; f

    The square-free factorization is :math:`\{x(x^3 + 2x + 4), x^2 + 4x + 1\}` with multiplicities :math:`\{1, 3\}`.

    .. ipython:: python

        galois.square_free_factorization(f)
        [a*b, c], [1, 3]
    """
    if not isinstance(poly, Poly):
        raise TypeError(f"Argument `poly` must be a galois.Poly, not {type(poly)}.")
    if not poly.degree >= 1:
        raise ValueError(f"Argument `poly` must be non-constant, not {poly}.")
    if not is_monic(poly):
        raise ValueError(f"Argument `poly` must be monic, not {poly}.")

    field = poly.field
    p = field.characteristic
    one = Poly.One(field=field)

    factors_ = []
    multiplicities = []

    # w is the product (without multiplicity) of all factors of f that have multiplicity not divisible by p
    d = poly_gcd(poly, poly.derivative())
    w = poly / d

    # Step 1: Find all factors in w
    i = 1
    while w != one:
        y = poly_gcd(w, d)
        z = w / y
        if z != one and i % p != 0:
            factors_.append(z)
            multiplicities.append(i)
        w = y
        d = d / y
        i = i + 1
    # d is now the product (with multiplicity) of the remaining factors of f

    # Step 2: Find all remaining factors (their multiplicities are divisible by p)
    if d != one:
        degrees = [degree // p for degree in d.degrees]
        coeffs = d.coeffs
        delta = Poly.Degrees(degrees, coeffs=coeffs, field=field)  # The p-th root of d(x)
        f, m = square_free_factorization(delta)
        factors_.extend(f)
        multiplicities.extend([mi*p for mi in m])

    # Sort the factors in increasing-multiplicity order
    factors_, multiplicities = zip(*sorted(zip(factors_, multiplicities), key=lambda item: item[1]))

    return list(factors_), list(multiplicities)


@set_module("galois")
def distinct_degree_factorization(poly):
    r"""
    Factors the monic, square-free polynomial :math:`f(x)` into a product of polynomials whose irreducible factors all have
    the same degree.

    Parameters
    ----------
    poly : galois.Poly
        A monic, square-free polynomial :math:`f(x)` over :math:`\mathrm{GF}(p^m)`.

    Returns
    -------
    list
        The list of polynomials :math:`f_i(x)` whose irreducible factors all have degree :math:`i`.
    list
        The list of corresponding distinct degrees :math:`i`.

    Notes
    -----
    The Distinct-Degree Factorization algorithm factors a square-free polynomial :math:`f(x)` with degree :math:`d` into a product of :math:`d` polynomials
    :math:`f_i(x)`, where :math:`f_i(x)` is the product of all irreducible factors of :math:`f(x)` with degree :math:`i`.

    .. math::
        f(x) = \prod_{i=1}^{d} f_i(x)

    For example, suppose :math:`f(x) = x(x + 1)(x^2 + x + 1)(x^3 + x + 1)(x^3 + x^2 + 1)` over :math:`\mathrm{GF}(2)`. Then the distinct-degree
    factorization is

    .. math::
        f_1(x) &= x(x + 1) = x^2 + x

        f_2(x) &= x^2 + x + 1

        f_3(x) &= (x^3 + x + 1)(x^3 + x^2 + 1) = x^6 + x^5 + x^4 + x^3 + x^2 + x + 1

        f_i(x) &= 1\ \textrm{for}\ i = 4, \dots, 10.

    Some :math:`f_i(x) = 1`, but those polynomials are not returned by this function. In this example, the function returns
    :math:`\{f_1(x), f_2(x), f_3(x)\}` and :math:`\{1, 2, 3\}`.

    The Distinct-Degree Factorization algorithm is often applied after the Square-Free Factorization algorithm, see :func:`galois.square_free_factorization`.
    A complete polynomial factorization is implemented in :func:`galois.poly_factors`.

    References
    ----------
    * D. Hachenberger, D. Jungnickel. Topics in Galois Fields. Algorithm 6.2.2.
    * Section 2.2 from https://people.csail.mit.edu/dmoshkov/courses/codes/poly-factorization.pdf

    Examples
    --------
    From the example in the notes, suppose :math:`f(x) = x(x + 1)(x^2 + x + 1)(x^3 + x + 1)(x^3 + x^2 + 1)` over :math:`\mathrm{GF}(2)`.

    .. ipython:: python

        a = galois.Poly([1,0]); a, galois.is_irreducible(a)
        b = galois.Poly([1,1]); b, galois.is_irreducible(b)
        c = galois.Poly([1,1,1]); c, galois.is_irreducible(c)
        d = galois.Poly([1,0,1,1]); d, galois.is_irreducible(d)
        e = galois.Poly([1,1,0,1]); e, galois.is_irreducible(e)
        f = a * b * c * d * e; f

    The distinct-degree factorization is :math:`\{x(x + 1), x^2 + x + 1, (x^3 + x + 1)(x^3 + x^2 + 1)\}` whose irreducible factors
    have degrees :math:`\{1, 2, 3\}`.

    .. ipython:: python

        galois.distinct_degree_factorization(f)
        [a*b, c, d*e], [1, 2, 3]
    """
    if not isinstance(poly, Poly):
        raise TypeError(f"Argument `poly` must be a galois.Poly, not {type(poly)}.")
    if not poly.degree >= 1:
        raise ValueError(f"Argument `poly` must be non-constant, not {poly}.")
    if not is_monic(poly):
        raise ValueError(f"Argument `poly` must be monic, not {poly}.")
    # TODO: Add check if the polynomial is square-free

    field = poly.field
    q = field.order
    n = poly.degree
    one = Poly.One(field=field)
    x = Poly.Identity(field=field)

    factors_ = []
    degrees = []

    a = poly.copy()
    h = x.copy()

    l = 1
    while l <= n // 2 and a != one:
        h = poly_pow(h, q, a)
        z = poly_gcd(a, h - x)
        if z != one:
            factors_.append(z)
            degrees.append(l)
            a = a / z
            h = h % a
        l += 1

    if a != one:
        factors_.append(a)
        degrees.append(a.degree)

    return factors_, degrees


@set_module("galois")
def equal_degree_factorization(poly, d):
    r"""
    Factors the monic, square-free polynomial :math:`f(x)` of degree :math:`rd` into a product of :math:`r` irreducible factors with
    degree :math:`d`.

    Parameters
    ----------
    poly : galois.Poly
        A monic, square-free polynomial :math:`f(x)` over :math:`\mathrm{GF}(p^m)`.
    d : int
        The degree :math:`d` of each irreducible factor of :math:`f(x)`.

    Returns
    -------
    list
        The list of :math:`r` irreducible factors :math:`\{g_1(x), \dots, g_r(x)\}` in lexicographically-increasing order.

    Notes
    -----
    The Equal-Degree Factorization algorithm factors a square-free polynomial :math:`f(x)` with degree :math:`rd` into a product of :math:`r`
    irreducible polynomials each with degree :math:`d`. This function implements the Cantor-Zassenhaus algorithm, which is probabilistic.

    The Equal-Degree Factorization algorithm is often applied after the Distinct-Degree Factorization algorithm, see :func:`galois.distinct_degree_factorization`.
    A complete polynomial factorization is implemented in :func:`galois.poly_factors`.

    References
    ----------
    * Section 2.3 from https://people.csail.mit.edu/dmoshkov/courses/codes/poly-factorization.pdf

    Examples
    --------
    Factor a product of degree-:math:`1` irreducible polynomials over :math:`\mathrm{GF}(2)`.

    .. ipython:: python

        a = galois.Poly([1,0]); a, galois.is_irreducible(a)
        b = galois.Poly([1,1]); b, galois.is_irreducible(b)
        f = a * b; f
        galois.equal_degree_factorization(f, 1)

    Factor a product of degree-:math:`3` irreducible polynomials over :math:`\mathrm{GF}(5)`.

    .. ipython:: python

        GF = galois.GF(5)
        a = galois.Poly([1,0,2,1], field=GF); a, galois.is_irreducible(a)
        b = galois.Poly([1,4,4,4], field=GF); b, galois.is_irreducible(b)
        f = a * b; f
        galois.equal_degree_factorization(f, 3)
    """
    if not isinstance(poly, Poly):
        raise TypeError(f"Argument `poly` must be a galois.Poly, not {type(poly)}.")
    if not isinstance(d, (int, np.integer)):
        raise TypeError(f"Argument `d` must be an integer, not {type(d)}.")
    if not poly.degree >= 1:
        raise ValueError(f"Argument `poly` must be non-constant, not {poly}.")
    if not is_monic(poly):
        raise ValueError(f"Argument `poly` must be monic, not {poly}.")
    if not poly.degree % d == 0:
        raise ValueError(f"Argument `d` must be divide the degree of the polynomial, {d} does not divide {poly.degree}.")
    # TODO: Add check if the polynomial is square-free

    field = poly.field
    q = field.order
    n = poly.degree
    r = poly.degree // d
    one = Poly.One(field=field)

    factors_ = [poly]
    while len(factors_) < r:
        h = Poly.Random(random.randint(1, n - 1), field=field)
        g = poly_gcd(poly, h)
        if g == one:
            g = poly_pow(h, (q**d - 1)//2, poly) - one
        for u in factors_:
            gcd = poly_gcd(g, u)
            if gcd not in [one, u]:
                factors_.remove(u)
                factors_.append(gcd)
                factors_.append(u / gcd)

    # Sort the factors in lexicographically-increasing order
    factors_ = sorted(factors_, key=lambda item: item.integer)

    return factors_