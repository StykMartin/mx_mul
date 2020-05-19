import builtins

import mock
import pytest

from mx_mul import (
    _cast_int,
    _cast_float,
    _validate_input_matrix_size,
    get_matrix_size,
    Matrix,
    get_matrix_values
)


class TestMatrix(object):
    @pytest.mark.parametrize("test_input, expected_width, expected_height",
                             [([[1]], 1, 1),
                              ([[1, 2, 3], [4, 5, 6]], 3, 2)]
                             )
    def test_matrix_init(self, test_input, expected_width, expected_height):
        matrix = Matrix(test_input)
        assert matrix.width == expected_width
        assert matrix.height == expected_height

    @pytest.mark.parametrize(
        "matrix_1, matrix_2, expected",
        [([[1]], [[2]], [[2]]),
         ([[1, 2], [5, 3], [6, 7]], [[5], [1]], [[7], [28], [37]])])
    def test_matrix_mul(self, matrix_1, matrix_2, expected):
        m1 = Matrix(matrix_1)
        m2 = Matrix(matrix_2)
        assert (m1 @ m2).matrix == expected

    def test_matrix_mul_exp(self):
        m1 = Matrix([[1]])
        m2 = Matrix([[1], [2]])

        with pytest.raises(ValueError):
            m1 @ m2

    def test_matrix_str(self):
        m1 = Matrix([[1, 2, 3], [4, 5, 6]])
        assert str(m1) == '1 2 3\n4 5 6'


class TestCasts(object):
    @pytest.mark.parametrize("test_input, get_exp, expected",
                             [("1", False, 1),
                              (1.0, False, 1),
                              ('A', True, ValueError)])
    def test_cast_to_int(self, test_input, get_exp, expected):
        if not get_exp:
            assert _cast_int(test_input) == expected
        else:
            with pytest.raises(expected):
                _cast_int(test_input)

    def test_cast_to_int_exp(self):
        with pytest.raises(ValueError):
            _cast_int('One exception please!')

    @pytest.mark.parametrize("test_input, get_exp, expected",
                             [("1", False, 1.0),
                              (1, False, 1.0),
                              ('ZZ', True, ValueError)])
    def test_cast_to_float(self, test_input, get_exp, expected):
        if not get_exp:
            assert _cast_float(test_input) == expected
        else:
            with pytest.raises(expected):
                _cast_float(test_input)


class TestGetMatrixValues(object):
    @pytest.mark.parametrize(
        "test_input, size, expected",
        [(['1 2 3'], (3, 1), [[1, 2, 3]]),
         (['1 2 3', '4 5 6'], (3, 2), [[1, 2, 3], [4, 5, 6]])])
    def test_get_matrix_values(self, test_input, size, expected):
        with mock.patch('builtins.input'):
            builtins.input.side_effect = test_input
            result = get_matrix_values('A', size)
            assert result == expected

    def test_get_matrix_exp(self):
        with mock.patch('builtins.input', return_value='1 2 3 4'):
            with pytest.raises(ValueError):
                get_matrix_values('A', (3, 1))


@pytest.mark.parametrize("test_input, get_exp, expected",
                         [((1, 1), False, None),
                          ((0, 1), True, ValueError),
                          ((9, 0), True, ValueError)])
def test_validate_input_matrix_size(test_input, get_exp, expected):
    if not get_exp:
        assert _validate_input_matrix_size(*test_input) == expected
    else:
        with pytest.raises(expected):
            _validate_input_matrix_size(*test_input)


def test_get_matrix_size(capsys):
    with mock.patch('builtins.input'):
        builtins.input.side_effect = [42, 24]
        width, height = get_matrix_size('A')
        assert capsys.readouterr().out.strip() == 'Matrix A'
        assert width == 42
        assert height == 24
