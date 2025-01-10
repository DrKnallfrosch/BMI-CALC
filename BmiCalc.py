from typing import Optional


class BmiCalc:
    """Interface for BMI Calculation"""

    def __init__(self, height: float, weight: float, age: Optional[int] = None, sex: Optional[str] = None):
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
        self.height = height
        self.weight = weight
        self.age = age
        self.sex = self.__validate_sex(sex)

    @staticmethod
    def __validate_sex(sex: object) -> object | None:
        """
        Validate Attribute Sex
        :rtype: object
        :param sex:
        :return: 
        """
        if sex in ['m', 'f', 'M', 'F']:
            return sex
        elif sex is None or sex == "":
            return None
        else:
            raise ValueError("Wrong sex is input")

    def get_bmi(self) -> float:
        """ :return: current BMI """
        return self.weight / (self.height ** 2)

    def get_category(self) -> str:
        """
        :return: current weight category as string
        :rtype: str
        """
        category_ = {
            'm': {(0, 19.9): "Underweight", (20, 24.9): "Normal weight", (25, 29.9): "Overweight",
                  (30, 34.9): "Obesity class 1", (35, 39.9): "Obesity class 2", (40, 2 ** 63 - 1): "Obesity class 3"},
            'f': {(0, 18.9): "Underweight", (19, 23.9): "Normal weight", (24, 29.9): "Overweight",
                  (30, 34.9): "Obesity class 1", (35, 39.9): "Obesity class 2", (40, 2 ** 63 - 1): "Obesity class 3"},
            None: {(0, 18.4): "Underweight", (18.5, 24.9): "Normal weight", (25, 29.9): "Overweight",
                   (30, 34.9): "Obesity class 1", (35, 39.9): "Obesity class 2", (40, 2 ** 63 - 1): "Obesity class 3"}}

        bmi = self.get_bmi()
        categories = category_.get(self.sex, category_[None])
        for (lower, upper), category in categories.items():
            if lower <= bmi <= upper:
                return category

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
            if age < 0:
                raise ValueError("Age must be greater than 0")
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
        self.sex = self.__validate_sex(sex)

    def get_size(self) -> float:
        """ get current size
        :return: current size in meters
        :rtype: float
        """
        return self.height

    def set_size(self, size: float) -> None:
        """ Set new size in meters
        :param size: new size
        """
        try:
            if size is float:
                if size < 0.0:
                    raise ValueError("Size must be greater than 0")
            self.height = size
        except ValueError:
            print("Size must be greater than 0")

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
        try:
            if weight is float:
                if weight < 0.0:
                    raise ValueError("Weight must be greater than 0")
            self.weight = weight
        except ValueError:
            print("Weight must be greater than 0")

    def get_ideal_weight(self) -> float:
        """ calculate ideal weight if self is not None then calculate ideal weight with the CREFF formula else with the
        BMI formula. The CREFF formula is only for adults and is use the Body Normal type.
        :return:  in kg
        :rtype: float
        """
        try:
            if self.age is not None:
                return ((self.height * 100) - 100) + (self.age/10) * 0.9
            elif self.sex == 'm':
                return 22.5 * (self.height ** 2)
            elif self.sex == 'f':
                return 21.5 * (self.height ** 2)
        except ZeroDivisionError:
            pass


if __name__ == '__main__':
    a = BmiCalc(1.80, 80, 19, "m")
    # print(a.get_bmi())
    print(a.get_category())
    print(a.get_ideal_weight())
    a.__init__(1.80, 80, 19, "f")
    print(a.get_category())
    print('-' * 100)
    a = BmiCalc(float(input("Size: ")), float(input("Weight: ")), int(input("Age: ")), input("Sex: "))
    print(a.get_bmi())
    print(a.get_category())
    print(a.get_ideal_weight())
