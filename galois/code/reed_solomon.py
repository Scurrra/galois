import numba
from numba import int64
import numpy as np

from ..factor import prime_factors
from ..field import Field, Poly, matlab_primitive_poly
from ..field.meta_function import UNARY_CALCULATE_SIG, BINARY_CALCULATE_SIG, BERLEKAMP_MASSEY_CALCULATE_SIG, POLY_ROOTS_CALCULATE_SIG, POLY_EVALUATE_CALCULATE_SIG, CONVOLVE_CALCULATE_SIG
from ..overrides import set_module

from .common import generator_poly_to_matrix, roots_to_parity_check_matrix

__all__ = ["ReedSolomon", "rs_generator_poly", "rs_generator_matrix", "rs_parity_check_matrix"]


###############################################################################
# Reed-Solomon Functions
###############################################################################

def _check_and_compute_field(n, k, c, primitive_poly, primitive_element):
    if not isinstance(n, (int, np.integer)):
        raise TypeError(f"Argument `n` must be an integer, not {type(n)}.")
    if not isinstance(k, (int, np.integer)):
        raise TypeError(f"Argument `k` must be an integer, not {type(k)}.")
    if not isinstance(c, (int, np.integer)):
        raise TypeError(f"Argument `c` must be an integer, not {type(c)}.")
    if not isinstance(primitive_poly, (type(None), int, Poly)):
        raise TypeError(f"Argument `primitive_poly` must be None, an int, or galois.Poly, not {type(primitive_poly)}.")

    if not (n - k) % 2 == 0:
        raise ValueError("Arguments `n - k` must be even.")
    p, m = prime_factors(n + 1)
    if not (len(p) == 1 and len(m) == 1):
        raise ValueError(f"Argument `n` must have value `q - 1` for a prime power `q`, not {n}.")
    if not c >= 1:
        raise ValueError(f"Argument `c` must be at least 1, not {c}.")
    p, m = p[0], m[0]

    if primitive_poly is None and m > 1:
        primitive_poly = matlab_primitive_poly(p, m)

    GF = Field(p**m, irreducible_poly=primitive_poly, primitive_element=primitive_element)

    return GF


@set_module("galois")
def rs_generator_poly(n, k, c=1, primitive_poly=None, primitive_element=None, roots=False):
    """
    Returns the generator polynomial :math:`g(x)` for the :math:`\\textrm{RS}(n, k)` code.

    The Reed-Solomon generator polynomial :math:`g(x)` is defined as :math:`g(x) = (x - \\alpha^{c})(x - \\alpha^{c + 1}) \\dots (x - \\alpha^{c + 2t - 1})`,
    where :math:`\\alpha` is a primitive element of :math:`\\mathrm{GF}(q)` and :math:`q` is a prime power of the form :math:`q = n + 1`.

    Parameters
    ----------
    n : int
        The codeword size :math:`n`, must be :math:`n = q - 1`.
    k : int
        The message size :math:`k`. The error-correcting capability :math:`t` is defined by :math:`n - k = 2t`.
    c : int, optional
        The first consecutive power of :math:`\\alpha`. The default is 1.
    primitive_poly : galois.Poly, optional
        Optionally specify the primitive polynomial that defines the extension field :math:`\\mathrm{GF}(q)`. The default is
        `None` which uses Matlab's default, see :func:`galois.matlab_primitive_poly`. Matlab tends to use the lexicographically-smallest
        primitive polynomial as a default instead of the Conway polynomial.
    primitive_element : int, galois.Poly, optional
        Optionally specify the primitive element :math:`\\alpha` of :math:`\\mathrm{GF}(q)` whose powers are roots of the generator polynomial :math:`g(x)`.
        The default is `None` which uses the lexicographically-smallest primitive element in :math:`\\mathrm{GF}(q)`, i.e.
        `galois.primitive_element(p, m)`.
    roots : bool, optional
        Indicates to optionally return the :math:`2t` roots in :math:`\\mathrm{GF}(q)` of the generator polynomial. The default is `False`.

    Returns
    -------
    galois.Poly
        The generator polynomial :math:`g(x)` over :math:`\\mathrm{GF}(q)`.
    galois.FieldArray
        The :math:`2t` roots in :math:`\\mathrm{GF}(q)` of the generator polynomial. Only returned if `roots=True`.

    Examples
    --------
    .. ipython:: python

        galois.rs_generator_poly(63, 57)
        galois.rs_generator_poly(63, 57, roots=True)
    """
    GF = _check_and_compute_field(n, k, c, primitive_poly, primitive_element)
    alpha = GF.primitive_element
    t = (n - k) // 2
    roots_ = alpha**(c + np.arange(0, 2*t))
    g = Poly.Roots(roots_)

    if not roots:
        return g
    else:
        return g, roots_


@set_module("galois")
def rs_generator_matrix(n, k, c=1, primitive_poly=None, primitive_element=None, systematic=True):
    """
    Returns the generator matrix :math:`\\mathbf{G}` for the :math:`\\textrm{RS}(n, k)` code.

    Parameters
    ----------
    n : int
        The codeword size :math:`n`, must be :math:`n = q - 1`.
    k : int
        The message size :math:`k`. The error-correcting capability :math:`t` is defined by :math:`n - k = 2t`.
    c : int, optional
        The first consecutive power of :math:`\\alpha`. The default is 1.
    primitive_poly : galois.Poly, optional
        Optionally specify the primitive polynomial that defines the extension field :math:`\\mathrm{GF}(q)`. The default is
        `None` which uses Matlab's default, see :func:`galois.matlab_primitive_poly`. Matlab tends to use the lexicographically-smallest
        primitive polynomial as a default instead of the Conway polynomial.
    primitive_element : int, galois.Poly, optional
        Optionally specify the primitive element :math:`\\alpha` of :math:`\\mathrm{GF}(q)` whose powers are roots of the generator polynomial :math:`g(x)`.
        The default is `None` which uses the lexicographically-smallest primitive element in :math:`\\mathrm{GF}(q)`, i.e.
        `galois.primitive_element(p, m)`.
    systematic : bool, optional
        Optionally specify if the encoding should be systematic, meaning the codeword is the message with parity
        appended. The default is `True`.

    Returns
    -------
    galois.FieldArray
        The :math:`(k, n)` generator matrix :math:`\\mathbf{G}`, such that given a message :math:`\\mathbf{m}`, a codeword is defined by
        :math:`\\mathbf{c} = \\mathbf{m}\\mathbf{G}`.

    Examples
    --------
    .. ipython :: python

        galois.rs_generator_poly(15, 9)
        galois.rs_generator_matrix(15, 9, systematic=False)
        galois.rs_generator_matrix(15, 9)
    """
    g = rs_generator_poly(n, k, c=c, primitive_poly=primitive_poly, primitive_element=primitive_element)
    G = generator_poly_to_matrix(n, g, systematic=systematic)
    return G


@set_module("galois")
def rs_parity_check_matrix(n, k, c=1, primitive_poly=None, primitive_element=None):
    """
    Returns the parity-check matrix :math:`\\mathbf{H}` for the :math:`\\textrm{RS}(n, k)` code.

    Parameters
    ----------
    n : int
        The codeword size :math:`n`, must be :math:`n = q - 1`.
    k : int
        The message size :math:`k`. The error-correcting capability :math:`t` is defined by :math:`n - k = 2t`.
    c : int, optional
        The first consecutive power of :math:`\\alpha`. The default is 1.
    primitive_poly : galois.Poly, optional
        Optionally specify the primitive polynomial that defines the extension field :math:`\\mathrm{GF}(q)`. The default is
        `None` which uses Matlab's default, see :func:`galois.matlab_primitive_poly`. Matlab tends to use the lexicographically-smallest
        primitive polynomial as a default instead of the Conway polynomial.
    primitive_element : int, galois.Poly, optional
        Optionally specify the primitive element :math:`\\alpha` of :math:`\\mathrm{GF}(q)` whose powers are roots of the generator polynomial :math:`g(x)`.
        The default is `None` which uses the lexicographically-smallest primitive element in :math:`\\mathrm{GF}(q)`, i.e.
        `galois.primitive_element(p, m)`.

    Returns
    -------
    galois.FieldArray
        The :math:`(2t, n)` parity-check matrix :math:`\\mathbf{H}`, such that given a codeword :math:`\\mathbf{c}`, the syndrome is defined by
        :math:`\\mathbf{s} = \\mathbf{c}\\mathbf{H}^T`.

    Examples
    --------
    .. ipython :: python

        G = galois.rs_generator_matrix(15, 9); G
        H = galois.rs_parity_check_matrix(15, 9); H
        GF = type(G)
        # The message
        m = GF.Random(9); m
        # The codeword
        c = m @ G; c
        # Error pattern
        e = GF.Zeros(15); e[0] = GF.Random(low=1); e
        # c is a valid codeword, so the syndrome is 0
        s = c @ H.T; s
        # c + e is not a valid codeword, so the syndrome is not 0
        s = (c + e) @ H.T; s
    """
    _, roots = rs_generator_poly(n, k, c=c, primitive_poly=primitive_poly, primitive_element=primitive_element, roots=True)
    H = roots_to_parity_check_matrix(n, roots)
    return H


###############################################################################
# Reed-Solomon Class
###############################################################################

@set_module("galois")
class ReedSolomon:
    """
    Constructs a :math:`\\textrm{RS}(n, k)` code.

    Parameters
    ----------
    n : int
        The codeword size :math:`n`, must be :math:`n = q - 1`.
    k : int
        The message size :math:`k`. The error-correcting capability :math:`t` is defined by :math:`n - k = 2t`.
    c : int, optional
        The first consecutive power of :math:`\\alpha`. The default is 1.
    primitive_poly : galois.Poly, optional
        Optionally specify the primitive polynomial that defines the extension field :math:`\\mathrm{GF}(q)`. The default is
        `None` which uses Matlab's default, see :func:`galois.matlab_primitive_poly`. Matlab tends to use the lexicographically-smallest
        primitive polynomial as a default instead of the Conway polynomial.
    primitive_element : int, galois.Poly, optional
        Optionally specify the primitive element :math:`\\alpha` of :math:`\\mathrm{GF}(q)` whose powers are roots of the generator polynomial :math:`g(x)`.
        The default is `None` which uses the lexicographically-smallest primitive element in :math:`\\mathrm{GF}(q)`, i.e.
        `galois.primitive_element(p, m)`.
    systematic : bool, optional
        Optionally specify if the encoding should be systematic, meaning the codeword is the message with parity
        appended. The default is `True`.

    Examples
    --------
    .. ipython:: python

        rs = galois.ReedSolomon(15, 9)
        GF = rs.field
        m = GF.Random(rs.k); m
        c = rs.encode(m); c
        # Corrupt the first symbol in the codeword
        c[0] ^= 13
        dec_m = rs.decode(c); dec_m
        np.array_equal(dec_m, m)

        # Instruct the decoder to return the number of corrected symbol errors
        dec_m, N = rs.decode(c, errors=True); dec_m, N
        np.array_equal(dec_m, m)
    """
    # pylint: disable=no-member

    def __new__(cls, n, k, c=1, primitive_poly=None, primitive_element=None, systematic=True):
        if not isinstance(systematic, bool):
            raise TypeError(f"Argument `systematic` must be a bool, not {type(systematic)}.")

        obj = super().__new__(cls)

        obj._n = n
        obj._k = k
        obj._c = c
        obj._systematic = systematic

        obj._generator_poly, obj._roots = rs_generator_poly(n, k, c=c, primitive_poly=primitive_poly, primitive_element=primitive_element, roots=True)
        obj._field = type(obj.roots)
        obj._t = obj.roots.size // 2

        obj._G = generator_poly_to_matrix(n, obj.generator_poly, systematic)
        obj._H = roots_to_parity_check_matrix(n, obj.roots)

        obj._is_narrow_sense = c == 1

        return obj

    def __init__(self, *args, **kwargs):  # pylint: disable=unused-argument
        # Pre-compile the arithmetic methods
        self._add_jit = self.field._calculate_jit("add")
        self._subtract_jit = self.field._calculate_jit("subtract")
        self._multiply_jit = self.field._calculate_jit("multiply")
        self._reciprocal_jit = self.field._calculate_jit("reciprocal")
        self._power_jit = self.field._calculate_jit("power")

        # Pre-compile the JIT functions
        self._berlekamp_massey_jit = self.field._function("berlekamp_massey")
        self._poly_divmod_jit = self.field._function("poly_divmod")
        self._poly_roots_jit = self.field._function("poly_roots")
        self._poly_eval_jit = self.field._function("poly_evaluate")
        self._convolve_jit = self.field._function("convolve")

        # Pre-compile the JIT decoder
        self._decode_jit = numba.jit(DECODE_CALCULATE_SIG.signature, nopython=True, cache=True)(decode_calculate)

    def __str__(self):
        return f"<Reed-Solomon Code: n={self.n}, k={self.k}>"

    def __repr__(self):
        return str(self)

    def encode(self, message, parity_only=False):
        """
        Encodes the message :math:`\\mathbf{m}` into the Reed-Solomon codeword :math:`\\mathbf{c}`.

        The message vector :math:`\\mathbf{m}` is defined as :math:`\\mathbf{m} = [m_{k-1}, \\dots, m_1, m_0]`, which
        corresponds to the message polynomial :math:`m(x) = m_{k-1} x^{k-1} + \\dots + m_1 x + m_0`.

        The codeword vector :math:`\\mathbf{c}` is computed by :math:`\\mathbf{c} = \\mathbf{m}\\mathbf{G}`, where
        :math:`\\mathbf{G}` is the generator matrix. The equivalent polynomial operation is :math:`c(x) = m(x)g(x)`.

        For systematic codes, :math:`\\mathbf{G} = [\\mathbf{I}\\ |\\ \\mathbf{P}]` such that :math:`\\mathbf{c} = [\\mathbf{m}\\ |\\ \\mathbf{p}]`.
        And in polynomial form, :math:`p(x) = -(m(x) x^{n-k}\\ \\textrm{mod}\\ g(x))` and :math:`c(x) = m(x)x^{n-k} + p(x)`.

        Parameters
        ----------
        message : numpy.ndarray, galois.FieldArray
            The message as either a :math:`k`-length vector or :math:`(N, k)` matrix, where :math:`N` is the number
            of messages.
        parity_only : bool, optional
            Optionally specify whether to return only the parity symbols. This only applies to systematic codes.
            The default is `False`.

        Returns
        -------
        numpy.ndarray, galois.FieldArray
            The codeword as either a :math:`n`-length vector or :math:`(N, n)` matrix. The return type matches the
            message type. If `parity_only=True`, the parity symbols are returned as either a :math:`n - k`-length vector or
            :math:`(N, n-k)` matrix.

        Examples
        --------
        Encode a single codeword.

        .. ipython:: python

            rs = galois.ReedSolomon(15, 9)
            GF = rs.field
            m = GF.Random(rs.k); m
            c = rs.encode(m); c
            p = rs.encode(m, parity_only=True); p

        Encode a matrix of codewords.

        .. ipython:: python

            m = GF.Random((5, rs.k)); m
            c = rs.encode(m); c
            p = rs.encode(m, parity_only=True); p
        """
        if not isinstance(message, np.ndarray):
            raise TypeError(f"Argument `message` must be a subclass of np.ndarray (or a galois.GF2 array), not {type(message)}.")
        if parity_only and not self.systematic:
            raise ValueError("Argument `parity_only` only applies to systematic codes.")
        if not message.shape[-1] == self.k:
            raise ValueError(f"Argument `message` must be a 1-D or 2-D array with last dimension equal to {self.k}, not shape {message.shape}.")

        if parity_only:
            parity = message.view(self.field) @ self.G[:, self.k:]
            return parity.view(type(message))
        elif self.systematic:
            parity = message.view(self.field) @ self.G[:, self.k:]
            return np.hstack((message, parity)).view(type(message))
        else:
            codeword = message.view(self.field) @ self.G
            return codeword.view(type(message))

    def decode(self, codeword, errors=False):
        """
        Decodes the Reed-Solomon codeword :math:`\\mathbf{c}` into the message :math:`\\mathbf{m}`.

        The codeword vector :math:`\\mathbf{c}` is defined as :math:`\\mathbf{c} = [c_{n-1}, \\dots, c_1, c_0]`, which
        corresponds to the codeword polynomial :math:`c(x) = c_{n-1} x^{n-1} + \\dots + c_1 x + c_0`.

        In decoding, the syndrome is computed by :math:`\\mathbf{s} = \\mathbf{c}\\mathbf{H}^T`, where
        :math:`\\mathbf{H}` is the generator matrix. The equivalent polynomial operation is :math:`s(x) = c(x)\\ \\textrm{mod}\\ g(x)`.
        A syndrome of zeros indicates the received codeword is a valid codeword and there are no errors. If the syndrome is non-zero,
        the decoder will find an error-locator polynomial :math:`\\sigma(x)` and the corresponding error locations and values.

        Parameters
        ----------
        codeword : numpy.ndarray, galois.FieldArray
            The codeword as either a :math:`n`-length vector or :math:`(N, n)` matrix, where :math:`N` is the
            number of codewords.
        errors : bool, optional
            Optionally specify whether to return the nubmer of corrected errors.

        Returns
        -------
        numpy.ndarray, galois.FieldArray
            The decoded message as either a :math:`k`-length vector or :math:`(N, k)` matrix.
        int, np.ndarray
            Optional return argument of the number of corrected symbol errors as either a scalar or :math:`n`-length vector.
            Valid number of corrections are in :math:`[0, t]`. If a codeword has too many errors and cannot be corrected,
            -1 will be returned.

        Examples
        --------
        Decode a single codeword.

        .. ipython:: python

            rs = galois.ReedSolomon(15, 9)
            GF = rs.field
            m = GF.Random(rs.k); m
            c = rs.encode(m); c
            # Corrupt the first symbol in the codeword
            c[0] ^= 13
            dec_m = rs.decode(c); dec_m
            np.array_equal(dec_m, m)

            # Instruct the decoder to return the number of corrected symbol errors
            dec_m, N = rs.decode(c, errors=True); dec_m, N
            np.array_equal(dec_m, m)

        Decode a matrix of codewords.

        .. ipython:: python

            m = GF.Random((5, rs.k)); m
            c = rs.encode(m); c
            # Corrupt the first symbol in each codeword
            c[:,0] ^= 13
            dec_m = rs.decode(c); dec_m
            np.array_equal(dec_m, m)

            # Instruct the decoder to return the number of corrected symbol errors
            dec_m, N = rs.decode(c, errors=True); dec_m, N
            np.array_equal(dec_m, m)
        """
        # pylint: disable=protected-access
        codeword_1d = codeword.ndim == 1
        dtype = codeword.dtype

        # Make codeword 2-D for array processing
        codeword = np.atleast_2d(codeword)

        # Compute the syndrome by matrix multiplying with the parity-check matrix
        syndrome = codeword.view(self.field) @ self.H.T

        if self.field.ufunc_mode != "python-calculate":
            dec_codeword =  self._decode_jit(codeword.astype(np.int64), syndrome.astype(np.int64), self.t, int(self.field.primitive_element), self._add_jit, self._subtract_jit, self._multiply_jit, self._reciprocal_jit, self._power_jit, self._berlekamp_massey_jit, self._poly_roots_jit, self._poly_eval_jit, self._convolve_jit, self.field.characteristic, self.field.degree, self.field._irreducible_poly_int)
            N_errors = dec_codeword[:, -1]

            if self.systematic:
                message = dec_codeword[:, 0:self.k]
            else:
                message, _ = self.field._poly_divmod(dec_codeword[:, 0:self.n].view(self.field), self.generator_poly.coeffs)
            message = message.astype(dtype).view(type(codeword))

        else:
            raise NotImplementedError("Reed-Solomon codes haven't been implemented for extremely large Galois fields.")

        if codeword_1d:
            message, N_errors = message[0,:], N_errors[0]

        if not errors:
            return message
        else:
            return message, N_errors

    @property
    def field(self):
        """
        galois.FieldClass: The Galois field :math:`\\mathrm{GF}(q)` that defines the Reed-Solomon code.
        """
        return self._field

    @property
    def n(self):
        """
        int: The codeword size :math:`n` of the :math:`\\textrm{RS}(n, k)` code.
        """
        return self._n

    @property
    def k(self):
        """
        int: The message size :math:`k` of the :math:`\\textrm{RS}(n, k)` code.
        """
        return self._k

    @property
    def t(self):
        """
        int: The error-correcting capability of the code. The code can correct :math:`t` symbol errors in a codeword.
        """
        return self._t

    @property
    def systematic(self):
        """
        bool: Indicates if the code is configured to return codewords in systematic form.
        """
        return self._systematic

    @property
    def generator_poly(self):
        """
        galois.Poly: The generator polynomial :math:`g(x)` whose roots are :obj:`ReedSolomon.roots`.
        """
        return self._generator_poly

    @property
    def roots(self):
        """
        galois.FieldArray: The roots of the generator polynomial. These are consecutive powers of :math:`\\alpha`.
        """
        return self._roots

    @property
    def c(self):
        """
        int: The degree of the first consecutive root.
        """
        return self._c

    @property
    def G(self):
        """
        galois.FieldArray: The generator matrix :math:`\\mathbf{G}` with shape :math:`(k, n)`.
        """
        return self._G

    @property
    def H(self):
        """
        galois.FieldArray: The parity-check matrix :math:`\\mathbf{H}` with shape :math:`(2t, n)`.
        """
        return self._H

    @property
    def is_narrow_sense(self):
        """
        bool: Indicates if the Reed-Solomon code is narrow sense, meaning the roots of the generator polynomial are consecutive
        powers of :math:`\\alpha` starting at 1, i.e. :math:`\\alpha, \\alpha^2, \\dots, \\alpha^{2t - 1}`.
        """
        return self._is_narrow_sense


###############################################################################
# JIT-compiled implementation of the specified functions
###############################################################################

DECODE_CALCULATE_SIG = numba.types.FunctionType(int64[:,:](int64[:,:], int64[:,:], int64, int64, BINARY_CALCULATE_SIG, BINARY_CALCULATE_SIG, BINARY_CALCULATE_SIG, UNARY_CALCULATE_SIG, BINARY_CALCULATE_SIG, BERLEKAMP_MASSEY_CALCULATE_SIG, POLY_ROOTS_CALCULATE_SIG, POLY_EVALUATE_CALCULATE_SIG, CONVOLVE_CALCULATE_SIG, int64, int64, int64))

def decode_calculate(codeword, syndrome, t, primitive_element, ADD, SUBTRACT, MULTIPLY, RECIPROCAL, POWER, BERLEKAMP_MASSEY, POLY_ROOTS, POLY_EVAL, CONVOLVE, CHARACTERISTIC, DEGREE, IRREDUCIBLE_POLY):  # pragma: no cover
    """
    References
    ----------
    * S. Lin and D. Costello. Error Control Coding. Section 7.4.
    """
    args = CHARACTERISTIC, DEGREE, IRREDUCIBLE_POLY
    dtype = codeword.dtype

    N = codeword.shape[0]  # The number of codewords
    n = codeword.shape[1]  # The codeword size

    # The last column of the returned decoded codeword is the number of corrected errors
    dec_codeword = np.zeros((N, n + 1), dtype=dtype)
    dec_codeword[:, 0:n] = codeword[:,:]

    for i in range(N):
        if not np.all(syndrome[i,:] == 0):
            # The syndrome vector is S = [S0, S1, ..., S2t-1]

            # The error pattern is defined as the polynomial e(x) = e_j1*x^j1 + e_j2*x^j2 + ... for j1 to jv,
            # implying there are v errors. And δi = e_ji is the i-th error value and βi = α^ji is the i-th error-locator
            # value and ji is the error location.

            # The error-locator polynomial σ(x) = (1 - β1*x)(1 - β2*x)...(1 - βv*x) where βi are the inverse of the roots
            # of σ(x).

            # Compute the error-locator polynomial σ(x) its v-reversal σ(x^-v), since the syndrome is passed in backwards
            sigma = BERLEKAMP_MASSEY(syndrome[i,:], ADD, SUBTRACT, MULTIPLY, RECIPROCAL, *args)
            sigma_rev = BERLEKAMP_MASSEY(syndrome[i,::-1], ADD, SUBTRACT, MULTIPLY, RECIPROCAL, *args)
            v = sigma.size - 1  # The number of errors

            if v > t:
                dec_codeword[i, -1] = -1
                continue

            # Compute βi, the roots of σ(x^-v) which are the inverse roots of σ(x)
            degrees = np.arange(sigma_rev.size - 1, -1, -1)
            results = POLY_ROOTS(degrees, sigma_rev, primitive_element, ADD, MULTIPLY, POWER, *args)
            beta = results[0,:]  # The roots of σ(x^-v)
            error_locations = results[1,:]  # The roots as powers of the primitive element α

            if beta.size != v:
                dec_codeword[i, -1] = -1
                continue

            # Compute σ'(x)
            sigma_prime = np.zeros(v, dtype=np.int64)
            for j in range(v):
                degree = v - j
                sigma_prime[j] = MULTIPLY(degree % CHARACTERISTIC, sigma[j], *args)  # Scalar multiplication

            # The error-value evalulator polynomial Z0(x) = S0*σ0 + (S1*σ0 + S0*σ1)*x + (S2*σ0 + S1*σ1 + S0*σ2)*x^2 + ...
            # with degree v-1
            Z0 = CONVOLVE(sigma[-v:], syndrome[i,0:v][::-1], ADD, MULTIPLY, *args)[-v:]

            # The error value δi = -Z0(βi^-1) / σ'(βi^-1)
            for j in range(v):
                beta_inv = RECIPROCAL(beta[j], *args)
                Z0_i = POLY_EVAL(Z0, beta_inv, ADD, MULTIPLY, *args)
                sigma_prime_i = POLY_EVAL(sigma_prime, beta_inv, ADD, MULTIPLY, *args)
                delta_i = MULTIPLY(SUBTRACT(0, Z0_i, *args), RECIPROCAL(sigma_prime_i, *args), *args)
                dec_codeword[i, n - 1 - error_locations[j]] = SUBTRACT(dec_codeword[i, n - 1 - error_locations[j]], delta_i, *args)
            dec_codeword[i, -1] = v  # The number of corrected errors

    return dec_codeword