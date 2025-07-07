import numpy as np
import json

class LimitLines:
    def __init__(self, axis="Primary", color="#ff0000", name="limits", passfail="dc"):
        self.axis = axis
        self.color = color
        self.name = name
        self.passfail = self._passfail_text(passfail)
        self.limitLines_dict = create_limitLines_dict()

        self.create_limits_from_points()


    def _passfail_text(self, passfail):
        if passfail == "dc":
            return "Dont Care"
        elif passfail == "high":
            return "High Limit"
        elif passfail == "low":
            return "Low Limit"
        else:
            print("Incorrect passfail string, options are: dc, high, low")
        
        def create_limits_from_points(self):
            for i in range(points):
                point = {"x": f[i], "y": il_db[i]}
                limitsLines["limitLines"][0]["points"].append(point)


def func(x, a, b, c):
    return (a + b * np.sqrt(x * 1e-6) + c * (x * 1e-9))

def create_limitLines_dict(self):
    limitsLines = {
    "limitLines" : [
        {
            "axis": self.axis,
            "color": self.color, 
            "name": self.name,
            "passfail": self.passfail,
            "points": [

            ]
    }]}

    return limitsLines


limitsLines = create_limitLines_dict(name="Channel Return Loss", passfail="high")

points = 100
f = np.linspace(5e6, 3.5e9, points, endpoint=True)
il_db = -func(f, 2.74, 0.25, 1.56)

for i in range(points):
    point = {"x": f[i], "y": il_db[i]}
    limitsLines["limitLines"][0]["points"].append(point)

with open("limits.limits", "w") as f:
    f.write(json.dumps(limitsLines, indent=4))
