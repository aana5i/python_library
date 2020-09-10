import math


class Polygon:
    def __init__(self, n, R):
        self._n = n
        self._R = R

    def __repr__(self):
        return f'Polygon(n={self._n}, R={self._R})'

    @property
    def count_vertices(self):
        return self._n

    @property
    def count_edges(self):
        return self._n

    @property
    def circumradius(self):
        return self._R

    @property
    def interior_angle(self):
        return (self._n - 2) * 180 / self._n

    @property
    def side_length(self):
        return 2 * self._R * math.sin(math.pi / self._n)

    @property
    def apothem(self):
        return self._R * math.cos(math.pi / self._n)

    @property
    def area(self):
        return self._n / 2 * self.side_length * self.apothem

    @property
    def perimeter(self):
        return self._n * self.side_length

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.count_edges == other.count_edges
                    and self.circumradius == other.circumradius)
        else:
            return NotImplemented


def test_polygon():
    rel_tol = 0.001
    abs_tol = 0.001

    n = 3
    R = 1
    p = Polygon(n, R)
    assert str(p) == f'Polygon(n=3, R=1)', f'actual: {str(p)}'
    assert p.count_vertices == n, (f'actual: {p.count_vertices}, '
                                   f' excepted: {n}')
    assert p.count_edges == n
    assert p.circumradius == R
    assert p.interior_angle == 60

    n = 4
    R = 1
    p = Polygon(n, R)
    assert math.isclose(p.interior_angle, 90)
    assert math.isclose(p.area,
                        2.0,
                        rel_tol=rel_tol,
                        abs_tol=abs_tol), f'actual: {p.area}, excepted: {2.0}'

    assert math.isclose(p.side_length,
                        math.sqrt(2),
                        rel_tol=rel_tol,
                        abs_tol=abs_tol)

    assert math.isclose(p.perimeter,
                        4 * math.sqrt(2),
                        rel_tol=rel_tol,
                        abs_tol=abs_tol)

test_polygon()
