# import numpy as np

# class Element:
#     def __init__(self,name, length):
#         self.name = name
#         self.length = length

#     def matrix(self):
#         raise NotImplementedError
    
# class Drift(Element):
#     def matrix(self):
#         L = self.length
#         return np.array([[1,L],[0,1]])
# class Quadrupole(Element):
#     def __init__(self, name, length, k1):
#         super().__init__(name, length)
#         self.k1 = k1

#     def matrix(self):
#         omega = np.sqrt(np.abs(self.k1))*self.length
#         if self.k1 <0:
#             return np.array([np.cos(omega),np.sin(omega)/np.sqrt(np.abs(self.k1))],[-np.sqrt(np.abs(self.k1))*np.sin(omega),np.cos(omega)])
#         else:
#             return np.array()

# class Sextupole(Element):
#     def __init__(self, name, length,k2):
#         super().__init__(name, length)
#         self.k2 = k2

#     def matrix(self):
#         L = self.length
#         return np.array([[1,L],[0,1]])
# class Dipole(Element):
#     def __init__(self, name, length, angle, k1 = 0, entry_angle=0,exit_angle=0):
#         super().__init__(name, length)
#         self.angle = angle
#         self.k1 = k1
#         self.entry_angle = entry_angle
#         self.exit_angle = exit_angle
# class Marker(Element):
#     def __init__(self, name):
#         super().__init__(name, length=0)

#     def matrix(self):
#         return np.eye(2)
# class Multipole(Element):
#     def __init__(self, name, length, polynom):
#         super().__init__(name, length)
#         self.polynom = polynom

#     def matrix(self):
#         L = self.length
#         return np.array([[1,L],[0,1]])