from multiprocessing.managers import Value
from typing import Optional


class BmiCalc:
    """Interface for BMI Calculation"""

    def __init__(self, size: float, weight: float, age: Optional[int] = None, sex: Optional[str] = None):
        """ Initialize BMI Calculation
        :param size: size in meters **required**
        :type size: float
        :param weight: weight in kg **required**
        :type weight: float
        :param age: age in years
        :type age: int
        :param sex: m or f for male or female
        :type sex: str
        """
        self.size = size
        self.weight = weight
        self.age = age
        self.sex = sex

        self.category = {
            'm': {(0, 20): "Untergewicht",
                  (20, 25): "Normalgewicht",
                  (25, 30): "Übergewicht",
                  (30, 35): "Adipositas Grad I",
                  (35, 40): "Adipositas Grad II",
                  (40, 2 ** 63 - 1): "Adipositas Grad III"},
            'f': {(0, 19): "Untergewicht",
                  (19, 24): "Normalgewicht",
                  (24, 30): "Übergewicht",
                  (30, 35): "Adipositas Grad I",
                  (35, 40): "Adipositas Grad II",
                  (40, 2 ** 63 - 1): "Adipositas Grad III"},
            None: {(0, 18.5): "Untergewicht",
                   (18.5, 25): "Normalgewicht",
                   (25, 30): "Übergewicht",
                   (30, 35): "Adipositas Grad I",
                   (35, 40): "Adipositas Grad II",
                   (40, 2 ** 63 - 1): "Adipositas Grad III"}}


        self.ideal_bmi_table = {(19, 24): (19, 24),
                          (25, 34): (20, 25),
                          (35, 44): (21, 26),
                          (45, 54): (22, 27),
                          (55, 65): (23, 28),
                          (65, 2 ** 63 - 1): (24, 29)}

    def get_bmi(self) -> float:
        """ :return: current BMI """
        return self.weight / (self.size ** 2)

    def get_category(self) -> str:
        """
        :return: current weight category as string
        :rtype: str
        """
        bmi = self.get_bmi()
        categories = self.category.get(self.sex, self.category[None])
        for (lower, upper), category in categories.items():
            if lower <= bmi < upper:
                return category
        else:
            raise ValueError("BMI category could not be determined.")

    def get_age(self) -> int:
        """ get current age
        :return: current age
        :rtype: int
        """
        return self.age

    def set_age(self, age: Optional[int]) -> None:
        """ Set new or reset age
        :param age: new age or None to reset
        :type age: Optional(int)
        """
        if age is not None:
            if not isinstance(age, int):
                raise TypeError("Age must be an integer")
            if age < 0:
                raise ValueError("Age must be greater than or equal to 0")
        self.age = age

    def get_sex(self) -> str:
        """ get current sex as 'm' or 'f'
        :return: current sex only 'm' or 'f'
        :rtype: str
        """
        return self.sex

    def set_sex(self, sex: Optional[str]) -> None:
        """ Set new or reset sex
        :param sex: new sex as 'm' or 'f' or None to reset
        """
        if sex not in (None, 'm', 'f'):
            raise ValueError("Sex must be either None, 'm' 'f'")

    def get_size(self) -> float:
        """ get current size
        :return: current size in meters
        :rtype: float
        """
        return self.size

    def set_size(self, size: float) -> None:
        """ Set new size in meters
        :param size: new size
        """
        if not isinstance(size, float):
            raise ValueError("Size must be a float")
        if size <= 0.0:
            raise ValueError("Size must be greater than 0")
        self.size = size

    def get_weight(self) -> float:
        """ get current weight
        :return: current weight in kg
        :rtype: float
        """
        return self.weight

    def set_weight(self, weight: float) -> None:
        """ Set new weight in meters
        :param weight: new weight
        """
        if not isinstance(weight, float):
            raise ValueError("Weight must be a float")
        if weight <= 0.0:
            raise ValueError("Weight must be greater than 0")
        self.weight = weight

    def get_ideal_weight(self) -> float:
        """ calculate ideal weight
        :return:  in kg
        :rtype: float
        """
        ideal_bmi = None
        if self.age is None:
            categories = self.category.get(self.sex, self.category[None])
            for (lower_bmi, upper_bmi), label in categories.items():
                if label == "Normalgewicht":
                    ideal_bmi = (lower_bmi + upper_bmi) / 2
        else:
            for (lower_age, upper_age), (lower_bmi, upper_bmi) in self.ideal_bmi_table.items():
                if lower_age <= self.age <= upper_age:
                    ideal_bmi = (lower_bmi + upper_bmi) / 2

        if ideal_bmi is None:
            raise ValueError("Ideal BMI must be greater than 0")

        return ideal_bmi * (self.size ** 2)