class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        return (f'Тип тренировки: {self.training_type}; '
                + f'Длительность: {self.duration:.3f} ч.; '
                + f'Дистанция: {self.distance:.3f} км; '
                + f'Ср. скорость: {self.speed:.3f} км/ч; '
                + f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # один шаг, метров
    M_IN_KM = 1000  # константа для перевода значений из м.в км.
    HRS_IN_MIN = 60  # константа для перевода часов в минуты

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Вернуть преодоленную дистанцию в километрах."""
        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories()
                              )
        return message


class Running(Training):
    """Тренировка: бег."""

    CNT_18 = 18  # какая-то константа
    CNT_20 = 20  # еще одна константа

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для тренировки: бег."""
        return ((Running.CNT_18 * self.get_mean_speed() - Running.CNT_20)
                * self.weight / Running.M_IN_KM * self.duration
                * Running.HRS_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CNT_35 = 0.035  # какая-то константа
    CNT_29 = 0.029  # еще одна константа

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий для тренировки:
        спортивная ходьба.
        """
        return ((SportsWalking.CNT_35 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * SportsWalking.CNT_29 * self.weight)
                * self.duration * self.HRS_IN_MIN)


class Swimming(Training):
    """Тренировка: плавание."""

    CNT_11 = 1.1  # какая-то константа
    LEN_STEP = 1.38  # расстояние, преодолеваемое за один гребок

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения для тренировки: плавание."""
        return (self.length_pool * self.count_pool
                / Swimming.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """
        Получить количество затраченных калорий для тренировки: плавание.
        """
        return (self.get_mean_speed() + Swimming.CNT_11) * 2 * self.weight

    def get_distance(self) -> float:
        """Вернуть преодоленную дистанцию в километрах."""
        return self.action * Swimming.LEN_STEP / Swimming.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные, полученные от датчиков."""

    used_classes = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking}

    return used_classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    msg = info.get_message()
    print(msg)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
