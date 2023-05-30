from typing import Sequence, Tuple
import pymunk

class ShapeEx(pymunk.Shape):
    def attach_to_body(self, body):
        self.super_body = body

class PolyEx(pymunk.Poly, ShapeEx):
    def __init__(self, body: pymunk.Body, vertices: Sequence[Tuple[float, float]], transform: pymunk.Transform=None, radius: float = 0) -> None:
        super().__init__(body, vertices, transform, radius)
        self.super_body = None

class CircleEx(pymunk.Circle, ShapeEx):
    def __init__(self, body: pymunk.Body, radius: float, offset: Tuple[float, float] = (0, 0)) -> None:
        super().__init__(body, radius, offset)
        self.super_body = None

class SegmentEx(pymunk.Segment, ShapeEx):
    def __init__(self, body: pymunk.Body, a: Tuple[float, float], b: Tuple[float, float], radius: float) -> None:
        super().__init__(body, a, b, radius)
        self.super_body = None