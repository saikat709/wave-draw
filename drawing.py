import cv2

class Point:
    def __init__(self, x, y, color=(0, 0, 255)):
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y}, color={self.color})"
    
    
class Circle:
    def __init__(self, center, radius, color=(0, 0, 255)):
        self.center = center  # Point object
        self.radius = radius
        self.color = color

    def __repr__(self):
        return f"Circle(center={self.center}, radius={self.radius}, color={self.color})" 

class Line:
    def __init__(self, start, end, color=(0, 0, 255)):
        self.start = start  # Point object
        self.end = end      # Point object
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
        self.selected_color = (0, 0, 255)
        self.points = []
        self.shapes = []
        self.lines  = []
        self.last_point = None

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
        # print(f"Added line: {line}")
    
    def add_circle(self, center_x, center_y, radius):
        center = Point(center_x, center_y, self.selected_color)
        circle = Circle(center, radius, self.selected_color)
        self.shapes.append(circle)
        print(f"Added circle: {circle}")
    
    def add_rectangle(self, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        rectangle = Rectangle(top_left_x, top_left_y, bottom_right_x, self.selected_color)
        self.shapes.append(rectangle)
        print(f"Added rectangle: {rectangle}")
    
    def draw(self, image):
        for point in self.points:
            cv2.circle(image, (point.x, point.y), self.circle_radius, point.color, -1)

        for line in self.lines:
            cv2.line(image, line.start, line.end, self.selected_color, self.line_width)
        
        for shape in self.shapes:
            if   isinstance(shape, Circle):
                cv2.circle(image, (shape.center.x, shape.center.y), shape.radius, shape.color, self.line_width)
            elif isinstance(shape, Rectangle):
                cv2.rectangle(image, (shape.top_left.x, shape.top_left.y), 
                              (shape.bottom_right.x, shape.bottom_right.y), shape.color, self.line_width)
        
        return image
