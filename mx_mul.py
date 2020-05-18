#!/usr/bin/python3

from __future__ import annotations

from typing import List, Union, Tuple, Any


class Matrix(object):
    def __init__(self, data: List[List[Union[int, float]]]) -> None:
        self.matrix: List[List[Union[int, float]]] = data
        self.height: int = len(data)
        self.width: int = len(data[0])

    def __matmul__(self, other: Matrix) -> Matrix:
        if self.width != other.height:
            raise ValueError("Dimensions doesn't match.")

        result = [[(sum([row_element * column_element for row_element, column_element in zip(row, column)]))
                   for column in zip(*other.matrix)]
                  for row in self.matrix]
        return Matrix(result)

    def __str__(self) -> str:
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])


def _cast_int(input_value: Any) -> int:
    try:
        input_value: int = int(input_value)
    except ValueError:
        raise ValueError(f"Input value has to be integer.")
    return input_value


def _cast_float(input_value: Any) -> float:
    try:
        input_value: float = float(input_value)
    except ValueError:
        raise ValueError("Input value has to be float.")
    return input_value


def _get_matrix_dimension(prompt: str) -> int:
    user_input: str = input(prompt)
    return _cast_int(user_input)


def get_matrix_size(name: str) -> Tuple[int, int]:
    print(f'Matrix {name}')
    width: int = _get_matrix_dimension('width: ')
    height: int = _get_matrix_dimension('height: ')
    print()
    return width, height


def validate_input_matrix_size(sizes: Tuple[Tuple[int, int], ...]) -> None:
    """
    Make sure user provided valid size for matrix.
    Smallest matrix can be 1x1
    """
    for size in sizes:
        width, height = size
        if width < 1 or height < 1:
            raise ValueError("I can't help you with this magic matrix.")


def _get_matrix_row(width: int) -> List[float]:
    items = input().split(' ')

    # Make sure user provided same amount of numbers as it is intended
    if len(items) != width:
        raise ValueError(f"Incorrect number of items in matrix")
    result = []
    for item in items:
        item = _cast_float(item)
        if item.is_integer():
            item = _cast_int(item)
        result.append(item)

    return result


def get_matrix_values(name: str, size: Tuple[int, int]) -> List[List[Union[int, float]]]:
    print(f'Matrix {name} values:')
    width, height = size
    values = [_get_matrix_row(width) for _ in range(height)]
    print()
    return values


def main() -> None:
    sizes = (get_matrix_size('A'), get_matrix_size('B'))
    validate_input_matrix_size(sizes)

    print(f"Result:\n{Matrix(get_matrix_values('A', sizes[0])) @ Matrix(get_matrix_values('B', sizes[1]))}")


if __name__ == '__main__':
    main()
