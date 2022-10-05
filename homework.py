from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Informational message about the workout."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: str = ('Workout type: {training_type}; '
                    'Duration: {duration:.3f} h.; '
                    'Distance: {distance:.3f} km; '
                    'Mean speed: {speed:.3f} km/h; '
                    'Calories burned: {calories:.3f}.')

    def get_message(self):
        """Create message with the results."""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Base workout class."""

    M_IN_KM: float = 1000 # Set meters in a kilometer.
    LEN_STEP: float = 0.65 # The parameter is taken from the technical documentation.
    HOURS_IN_MINUTES: float = 60 # Set the minutes in a hour.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Get distance in kilometers."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get mean speed."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get count of burned calories."""
        raise NotImplementedError(
            'Define get_spent_calories() '
            f'in {self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Return an object of InfoMessage class."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Training: Running."""

    CAL_PARAM_1: int = 18 # The parameter is taken from the technical documentation.
    CAL_PARAM_2: int = 20 # The parameter is taken from the technical documentation.

    def get_spent_calories(self) -> float:
        """Redefine method - Get count of burned calories."""
        return ((self.CAL_PARAM_1 * self.get_mean_speed()
                - self.CAL_PARAM_2) * self.weight / self.M_IN_KM
                * self.duration * self.HOURS_IN_MINUTES)


class SportsWalking(Training):
    """Training: SportsWalking."""

    CAL_PARAM_1: float = 0.035 # The parameter is taken from the technical documentation.
    CAL_PARAM_2: float = 0.029 # The parameter is taken from the technical documentation.
    CAL_PARAM_3: int = 2 # The parameter is taken from the technical documentation.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Redefine method - Get count of burned calories."""
        return ((self.CAL_PARAM_1 * self.weight
                + (self.get_mean_speed() ** self.CAL_PARAM_3 // self.height)
                * self.CAL_PARAM_2 * self.weight)
                * self.duration * self.HOURS_IN_MINUTES)


class Swimming(Training):
    """Training: Swimming."""

    LEN_STEP: float = 1.38 # The parameter is taken from the technical documentation.
    CAL_PARAM_1: float = 1.1 # The parameter is taken from the technical documentation.
    CAL_PARAM_2: int = 2 # The parameter is taken from the technical documentation.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Redefine method - Get mean speed."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Redefine method - Get count of burned calories."""
        return ((self.get_mean_speed() + self.CAL_PARAM_1)
                * self.CAL_PARAM_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Determine the type of workout from the received data."""
    train_package: Dict[str, Type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}
    text_error: str = ', '.join(train_package)
    if workout_type not in train_package:
        raise ValueError(f'Unknown workout type - {workout_type}, '
                         f'one of the following types is required: {text_error}')
    return train_package[workout_type](*data)


def training_result(training: Training) -> None:
    """Output of workout results."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        training_result(training)
