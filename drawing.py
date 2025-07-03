import cv2
from constants import COLOR_GREEN_BGR, COLOR_WHITE
from utils import get_distance


class Point:
    def __init__(self, x, y, color=(0, 0, 255)):
        self.x     = x
        self.y     = y
        self.color = color

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y}, color={self.color})"


    
class Circle:
    def __init__(self, center, radius, color=(0, 0, 255)):
        self.center = center  # Point object
        self.radius = radius
        self.color  = color

    def __repr__(self):
        return f"Circle(center={self.center}, radius={self.radius}, color={self.color})" 


class Line:
    def __init__(self, start, end, color=(0, 0, 255)):
        self.start = start    # Point object
        self.end   = end      # Point object
        self.color = color

    def __repr__(self):
        return f"Line(start={self.start}, end={self.end}, color={self.color})"  



class Rectangle:
    def __init__(self, top_left, bottom_right, color=(0, 0, 255)):
        self.top_left = top_left  
        self.bottom_right = bottom_right
        self.color = color

    def __repr__(self):
        return f"Rectangle(top_left={self.top_left}, bottom_right={self.bottom_right}, color={self.color})"



class Drawing:
    def __init__(self, width = 0, height = 0):
        self.width = width
        self.height = height
        
        self.selected_color = COLOR_GREEN_BGR 
        self.background_color = COLOR_WHITE
        
        self.points = []
        self.shapes = []
        self.lines  = []

        self.last_point = None
        self.last_shape = None

        self.circle_radius = 3
        self.line_width    = 6

    
    def add_point(self, x, y):
        point = Point(x, y, self.selected_color)
        self.points.append(point)
        self.last_point = point
        # print(f"Added point: {point}")
    

    def add_line(self, start_x, start_y, end_x, end_y):
        line = Line((start_x, start_y), (end_x, end_y), self.selected_color)
        self.lines.append(line)


    def update_line(self, current_x, current_y):
        if self.lines and isinstance(self.lines[-1], Line):
            line = self.lines[-1]
            line.end = (current_x, current_y)
        else:
            print("No line to update. Please add a line first.")

    
    def add_circle(self, center_x, center_y, radius = 0):
        center = Point(center_x, center_y, self.selected_color)
        circle = Circle(center,  radius,   self.selected_color)
        self.shapes.append(circle)


    def update_circle(self, current_x, current_y):
        if self.shapes and isinstance(self.shapes[-1], Circle):
            circle = self.shapes[-1]
            radius = get_distance((circle.center.x, circle.center.y), (current_x, current_y))
            circle.radius = radius
        else:
            print("No circle to update. Please add a circle first.")


    def add_rectangle(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        rectangle = Rectangle((top_left_x, top_left_y), (bottom_right_x, bottom_right_y), self.selected_color)
        self.shapes.append(rectangle)
        print(f"Added rectangle: {rectangle}")


    def update_rectangle(self, bottom_right_x, bottom_right_y):
        if self.shapes and isinstance(self.shapes[-1], Rectangle):
            rectangle = self.shapes[-1]
            rectangle.bottom_right = (bottom_right_x, bottom_right_y)
        else:
            print("No rectangle to update. Please add a rectangle first.")


    def draw(self, image):
        for point in self.points:
            cv2.circle(image, (point.x, point.y), self.circle_radius, point.color, -1)

        for line in self.lines:
            cv2.line(image, line.start, line.end, self.selected_color, self.line_width)

        # print(f"Shapes: {self.shapes}")
        for shape in self.shapes:
            print(f"Drawing shape: {shape}")
            if isinstance(shape, Circle):
                cv2.circle(image, (shape.center.x, shape.center.y), shape.radius, shape.color, self.line_width)
            elif isinstance(shape, Rectangle):
                cv2.rectangle(image, (shape.top_left[0], shape.top_left[1]), 
                            (shape.bottom_right[0], shape.bottom_right[1]), shape.color, self.line_width)
        
        return image
    

    def clear_all(self):
        self.points = []
        self.shapes = []
        self.lines  = []
        self.last_point = None
        self.last_shape = None
        print("Cleared all drawings.")
