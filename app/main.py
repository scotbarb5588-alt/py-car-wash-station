from decimal import Decimal, ROUND_HALF_UP


def _round1(value):
    """Round to 1 decimal, half up (avoids float surprises like 31.85)."""
    d = Decimal(str(round(value, 9)))
    return float(d.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


class Car:
    def __init__(self, comfort_class, clean_mark, brand):
        self.comfort_class = comfort_class  # 1..7
        self.clean_mark = clean_mark        # 1..10
        self.brand = brand


class CarWashStation:
    def __init__(self, distance_from_city_center, clean_power,
                 average_rating, count_of_ratings):
        self.distance_from_city_center = distance_from_city_center  # 1.0..10.0
        self.clean_power = clean_power
        self.average_rating = average_rating                        # 1.0..5.0
        self.count_of_ratings = count_of_ratings

    def calculate_washing_price(self, car):
        price = (car.comfort_class
                 * (self.clean_power - car.clean_mark)
                 * self.average_rating
                 / self.distance_from_city_center)
        return _round1(price)

    def wash_single_car(self, car):
        if self.clean_power > car.clean_mark:
            car.clean_mark = self.clean_power

    def serve_cars(self, cars):
        income = 0.0
        for car in cars:
            if car.clean_mark < self.clean_power:
                income += self.calculate_washing_price(car)
                self.wash_single_car(car)
        return _round1(income)

    def rate_service(self, rate):
        total = self.average_rating * self.count_of_ratings + rate
        self.count_of_ratings += 1
        self.average_rating = _round1(total / self.count_of_ratings)