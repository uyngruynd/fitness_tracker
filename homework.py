from dataclasses import asdict, dataclass
from typing import ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    SAMPLE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                             'Длительность: {duration:.3f} ч.; '
                             'Дистанция: {distance:.3f} км; '
                             'Ср. скорость: {speed:.3f} км/ч; '
                             'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        return self.SAMPLE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65  # один шаг, метров
    M_IN_KM: ClassVar[int] = 1000  # константа для перевода значений из м.в км.
    HRS_IN_MIN: ClassVar[int] = 60  # константа для перевода часов в минуты

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
        raise NotImplementedError('Метод должен быть определен в классе-'
                                  'наследнике')

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

    CNT_18: ClassVar[int] = 18
    CNT_20: ClassVar[int] = 20

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

    CNT_35: ClassVar[float] = 0.035
    CNT_29: ClassVar[float] = 0.029

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

    CNT_11: ClassVar[float] = 1.1
    LEN_STEP: ClassVar[float] = 1.38  # расстояние за один гребок

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
    used_classes: Dict[str, Type[Training]] = {'SWM': Swimming,
                                               'RUN': Running,
                                               'WLK': SportsWalking}

    if workout_type not in used_classes.keys():
        raise KeyError('Получен неизвестный тип тренировки')

    return used_classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
