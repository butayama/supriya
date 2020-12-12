from uqbar.enums import IntEnumeration

from .patterns import Pattern, SequencePattern


class ChoicePattern(SequencePattern):
    def __init__(self, sequence, iterations=1, forbid_repetitions=False, weights=None):
        super().__init__(sequence, iterations=iterations)
        self._forbid_repetitions = bool(forbid_repetitions)
        if weights is None:
            weights = tuple(abs(float(x)) for x in weights)
        self._weights = weights

    def _iterate(self, state=None):
        rng = self._get_rng()
        previous_index = None
        for _ in self._loop(self._iterations):
            # TODO: Integrate weights
            if self.weights:
                index = self._find_index_weighted(rng)
                while self.forbid_repetitions and index == previous_index:
                    index = self._find_index_weighted(rng)
            else:
                index = self._find_index_unweighted(rng)
                while self.forbid_repetitions and index == previous_index:
                    index = self._find_index_unweighted(rng)
            previous_index = index
            choice = self.sequence[index]
            if isinstance(choice, Pattern):
                yield from choice
            else:
                yield choice

    def _find_index_unweighted(self, rng):
        return int(next(rng) * 0x7FFFFFFF) % len(self.sequence)

    def _find_index_weighted(self, rng):
        needle = next(rng) * sum(self.weights)
        sum_of_weights = 0.0
        for index, weight in enumerate(self.weights):
            if sum_of_weights <= needle <= sum_of_weights + weight:
                break
            sum_of_weights += weight
        return index

    @property
    def forbid_repetitions(self):
        return self._forbid_repetitions

    @property
    def weights(self):
        return self._weights


class RandomPattern(Pattern):
    class Distribution(IntEnumeration):
        WHITE_NOISE = 0

    def __init__(
        self, minimum=0.0, maximum=1.0, iterations=None, distribution="WHITE_NOISE"
    ):
        if iterations is not None:
            iterations = int(iterations)
            if iterations < 1:
                raise ValueError("Iterations must be null or greater than 0")
        self._iterations = iterations
        self._distribution = self.Distribution.from_expr(distribution)
        self._minimum = self._freeze_recursive(minimum)
        self._maximum = self._freeze_recursive(maximum)

    def _iterate(self, state=None):
        def procedure(one, two):
            minimum, maximum = sorted([one, two])
            number = next(rng)
            return (number * (maximum - minimum)) + minimum

        rng = self._get_rng()
        for _ in self._loop(self._iterations):
            expr = self._process_recursive(self._minimum, self._maximum, procedure)
            should_stop = yield expr
            if should_stop:
                return

    @property
    def arity(self):
        return max(self._get_arity(x) for x in (self._minimum, self._maximum))

    @property
    def distribution(self):
        return self._distribution

    @property
    def is_infinite(self):
        return self._iterations is None

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum

    @property
    def repetitions(self):
        return self._iterations


class ShufflePattern(SequencePattern):
    def __init__(self, sequence, iterations=1, forbid_repetitions=False):
        super().__init__(sequence, iterations=iterations)
        self._forbid_repetitions = bool(forbid_repetitions)

    def _iterate(self, state=None):
        rng = self._get_rng()
        previous_index = None
        for _ in self._loop(self._iterations):
            indices = self._shuffle(len(self.sequence), rng, previous_index)
            while self.forbid_repetitions and indices[0] == previous_index:
                indices = self._shuffle(len(self.sequence), rng, previous_index)
            previous_index = indices[-1]
            for index in indices:
                choice = self.sequence[index]
                if isinstance(choice, Pattern):
                    yield from choice
                else:
                    yield choice

    def _shuffle(self, length, rng, previous_index=None):
        indices = list(range(length))
        shuffled_indices = []
        while len(indices) > 1:
            index = int(next(rng) * 0x7FFFFFFF) % len(indices)
            shuffled_indices.append(indices.pop(index))
        if indices:
            shuffled_indices.append(indices.pop())
        return shuffled_indices

    @property
    def forbid_repetitions(self):
        return self._forbid_repetitions
