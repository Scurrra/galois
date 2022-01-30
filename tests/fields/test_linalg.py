"""
A pytest module to test linear algebra routines over Galois fields.
"""
import random

import pytest
import numpy as np

import galois

from ..helper import array_equal


def test_dot_scalar(field):
    dtype = random.choice(field.dtypes)
    a = field.Random((3,3), dtype=dtype)
    b = field.Random(dtype=dtype)

    c = np.dot(a, b)
    assert type(c) is field
    assert c.dtype == dtype
    assert array_equal(c, a * b)

    c = a.dot(b)
    assert type(c) is field
    assert c.dtype == dtype
    assert array_equal(c, a * b)


def test_dot_vector_vector(field):
    dtype = random.choice(field.dtypes)
    a = field.Random(3, dtype=dtype)
    b = field.Random(3, dtype=dtype)

    c = np.dot(a, b)
    assert type(c) is field
    assert c.dtype == dtype
    assert array_equal(c, np.sum(a * b))

    c = a.dot(b)
    assert type(c) is field
    assert c.dtype == dtype
    assert array_equal(c, np.sum(a * b))


def test_dot_matrix_matrix(field):
    dtype = random.choice(field.dtypes)
    A = field.Random((3,3), dtype=dtype)
    B = field.Random((3,3), dtype=dtype)

    C = np.dot(A, B)
    assert type(C) is field
    assert C.dtype == dtype
    assert array_equal(C, A @ B)

    C = A.dot(B)
    assert type(C) is field
    assert C.dtype == dtype
    assert array_equal(C, A @ B)


def test_dot_tensor_vector(field):
    dtype = random.choice(field.dtypes)
    A = field.Random((3,4,5), dtype=dtype)
    b = field.Random(5, dtype=dtype)

    C = np.dot(A, b)
    assert type(C) is field
    assert C.dtype == dtype
    assert array_equal(C, np.sum(A * b, axis=-1))

    C = A.dot(b)
    assert type(C) is field
    assert C.dtype == dtype
    assert array_equal(C, np.sum(A * b, axis=-1))


def test_vdot_scalar(field):
    dtype = random.choice(field.dtypes)
    a = field.Random(dtype=dtype)
    b = field.Random(dtype=dtype)
    c = np.vdot(a, b)
    assert type(c) is field
    assert c.dtype == dtype
    assert array_equal(c, a * b)


def test_vdot_vector_vector(field):
    dtype = random.choice(field.dtypes)
    a = field.Random(3, dtype=dtype)
    b = field.Random(3, dtype=dtype)
    c = np.vdot(a, b)
    assert type(c) is field
    assert c.dtype == dtype
    assert array_equal(c, np.sum(a * b))


def test_vdot_matrix_matrix(field):
    dtype = random.choice(field.dtypes)
    A = field.Random((3,3), dtype=dtype)
    B = field.Random((3,3), dtype=dtype)
    C = np.vdot(A, B)
    assert type(C) is field
    assert C.dtype == dtype
    assert array_equal(C, np.sum(A.flatten() * B.flatten()))


def test_inner_scalar_scalar(field):
    dtype = random.choice(field.dtypes)
    a = field.Random(dtype=dtype)
    b = field.Random(dtype=dtype)
    c = np.inner(a, b)
    assert type(c) is field
    assert c.dtype == dtype
    assert c == a*b


def test_inner_vector_vector(field):
    dtype = random.choice(field.dtypes)
    a = field.Random(3, dtype=dtype)
    b = field.Random(3, dtype=dtype)
    c = np.inner(a, b)
    assert type(c) is field
    assert c.dtype == dtype
    assert array_equal(c, np.sum(a * b))


def test_outer_vector_vector(field):
    dtype = random.choice(field.dtypes)
    a = field.Random(3, dtype=dtype)
    b = field.Random(4, dtype=dtype)
    c = np.outer(a, b)
    assert type(c) is field
    assert c.dtype == dtype
    assert array_equal(c, np.multiply.outer(a, b))


def test_outer_nd_nd(field):
    dtype = random.choice(field.dtypes)
    a = field.Random((3,3), dtype=dtype)
    b = field.Random((4,4), dtype=dtype)
    c = np.outer(a, b)
    assert type(c) is field
    assert c.dtype == dtype
    assert array_equal(c, np.multiply.outer(a.ravel(), b.ravel()))


def test_matmul_scalar(field):
    dtype = random.choice(field.dtypes)
    A = field.Random((3,3), dtype=dtype)
    B = field.Random(dtype=dtype)
    with pytest.raises(ValueError):
        A @ B
    with pytest.raises(ValueError):
        np.matmul(A, B)


def test_matmul_1d_1d(field):
    dtype = random.choice(field.dtypes)
    A = field.Random(3, dtype=dtype)
    B = field.Random(3, dtype=dtype)
    C = A @ B
    assert C == np.sum(A * B)
    assert C.shape == ()
    assert type(C) is field
    assert C.dtype == dtype
    assert array_equal(A @ B, np.matmul(A, B))


def test_matmul_2d_1d(field):
    dtype = random.choice(field.dtypes)
    A = field.Random((3,4), dtype=dtype)
    B = field.Random(4, dtype=dtype)
    C = A @ B
    assert C[0] == np.sum(A[0,:] * B)  # Spot check
    assert C.shape == (3,)
    assert type(C) is field
    assert C.dtype == dtype
    assert array_equal(A @ B, np.matmul(A, B))


def test_matmul_1d_2d(field):
    dtype = random.choice(field.dtypes)
    A = field.Random(4, dtype=dtype)
    B = field.Random((4,3), dtype=dtype)
    C = A @ B
    assert C[0] == np.sum(A * B[:,0])  # Spot check
    assert C.shape == (3,)
    assert type(C) is field
    assert C.dtype == dtype
    assert array_equal(A @ B, np.matmul(A, B))


def test_matmul_2d_2d(field):
    dtype = random.choice(field.dtypes)
    A = field.Random((3,4), dtype=dtype)
    B = field.Random((4,3), dtype=dtype)
    C = A @ B
    assert C[0,0] == np.sum(A[0,:] * B[:,0])  # Spot check
    assert C.shape == (3,3)
    assert type(C) is field
    assert C.dtype == dtype
    assert array_equal(A @ B, np.matmul(A, B))


# def test_matmul_nd_2d(field):
#     A = field.Random((2,3,4), dtype=dtype)
#     B = field.Random((4,3), dtype=dtype)
#     C = A @ B
#     assert array_equal(C[0,0,0], np.sum(A[0,0,:] * B[:,0]))  # Spot check
#     assert C.shape == (2,3,3)
#     assert type(C) is field
#     assert array_equal(A @ B, np.matmul(A, B))


# def test_matmul_nd_nd(field):
#     A = field.Random((2,3,4), dtype=dtype)
#     B = field.Random((2,4,3), dtype=dtype)
#     C = A @ B
#     assert array_equal(C[0,0,0], np.sum(A[0,0,:] * B[0,:,0]))  # Spot check
#     assert C.shape == (2,3,3)
#     assert type(C) is field
#     assert array_equal(A @ B, np.matmul(A, B))


def full_rank_matrix(field, n, dtype):
    A = field.Identity(n, dtype=dtype)
    while True:
        A = field.Random((n,n), dtype=dtype)
        if np.linalg.matrix_rank(A) == n:
            break
    return A


###############################################################################
# Tests against Sage test vectors
###############################################################################

def test_matrix_multiply(field_matrix_multiply):
    GF, X, Y, Z = field_matrix_multiply["GF"], field_matrix_multiply["X"], field_matrix_multiply["Y"], field_matrix_multiply["Z"]

    for i in range(len(X)):
        dtype = random.choice(GF.dtypes)
        x = X[i].astype(dtype)
        y = Y[i].astype(dtype)
        z = x @ y
        assert np.array_equal(z ,Z[i])
        assert type(z) is GF


def test_row_reduce(field_row_reduce):
    GF, X, Z = field_row_reduce["GF"], field_row_reduce["X"], field_row_reduce["Z"]

    for i in range(len(X)):
        dtype = random.choice(GF.dtypes)
        x = X[i].astype(dtype)
        z = x.row_reduce()
        assert np.array_equal(z, Z[i])
        assert type(z) is GF


def test_lu_decompose(field_lu_decompose):
    GF, X, L, U = field_lu_decompose["GF"], field_lu_decompose["X"], field_lu_decompose["L"], field_lu_decompose["U"]

    for i in range(len(X)):
        dtype = random.choice(GF.dtypes)
        x = X[i].astype(dtype)
        l, u = x.lu_decompose()
        assert np.array_equal(l, L[i])
        assert np.array_equal(u, U[i])
        assert type(l) is GF
        assert type(u) is GF


def test_plu_decompose(field_plu_decompose):
    GF, X, P, L, U = field_plu_decompose["GF"], field_plu_decompose["X"], field_plu_decompose["P"], field_plu_decompose["L"], field_plu_decompose["U"]

    for i in range(len(X)):
        dtype = random.choice(GF.dtypes)
        x = X[i].astype(dtype)
        p, l, u = x.plu_decompose()
        assert np.array_equal(p, P[i])
        assert np.array_equal(l, L[i])
        assert np.array_equal(u, U[i])
        assert type(p) is GF
        assert type(l) is GF
        assert type(u) is GF


def test_matrix_inverse(field_matrix_inverse):
    GF, X, Z = field_matrix_inverse["GF"], field_matrix_inverse["X"], field_matrix_inverse["Z"]

    for i in range(len(X)):
        dtype = random.choice(GF.dtypes)
        x = X[i].astype(dtype)
        z = np.linalg.inv(x)
        assert np.array_equal(z, Z[i])
        assert type(z) is GF


def test_matrix_determinant(field_matrix_determinant):
    GF, X, Z = field_matrix_determinant["GF"], field_matrix_determinant["X"], field_matrix_determinant["Z"]

    for i in range(len(X)):
        dtype = random.choice(GF.dtypes)
        x = X[i].astype(dtype)
        z = np.linalg.det(x)
        assert z == Z[i]
        assert type(z) is GF


def test_matrix_solve(field_matrix_solve):
    GF, X, Y, Z = field_matrix_solve["GF"], field_matrix_solve["X"], field_matrix_solve["Y"], field_matrix_solve["Z"]

    # np.linalg.solve(x, y) = z corresponds to X @ z = y
    for i in range(len(X)):
        dtype = random.choice(GF.dtypes)
        x = X[i].astype(dtype)
        y = Y[i].astype(dtype)
        z = np.linalg.solve(x, y)
        assert np.array_equal(z, Z[i])
        assert type(z) is GF
