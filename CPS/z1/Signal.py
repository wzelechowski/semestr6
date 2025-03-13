import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
import random
matplotlib.use('TkAgg')


class Signal(ABC):
    def __init__(self, A, t1, d):
        self.A = A
        self.t1 = t1
        self.d = d
        self.f = 1
        self.n1 = int(self.t1 * self.f)
        self.t2 = self.t1 + self.d
        self.n2 = int(self.t2 * self.f)
        self.t = []
        self.y = []

    def generate_t(self):
        self.t = np.linspace(self.t1, self.t2, (self.n2 - self.n1 + 1) * 100)

    @abstractmethod
    def generate_signal(self):
        pass

    def avg_value(self):
        return 'Wartość średnia: ', np.sum(self.y) / len(self.t)

    def abs_avg_value(self):
        y = [abs(x) for x in self.y]
        return 'Wartość średnia bezwzględna: ', np.sum(y) / len(self.t)

    def avg_power(self):
        y = [x ** 2 for x in self.y]
        return 'Moc średnia: ', np.sum(y) / len(self.t)

    def variance(self):
        avg = self.avg_value()
        y = [(x - avg[1]) ** 2 for x in self.y]
        return 'Wariancja: ', np.sum(y) / len(self.t)

    def root_mean_square(self):
        y = [x ** 2 for x in self.y]
        return 'Wartość skuteczna: ', (np.sum(y) / len(self.t)) ** 0.5,

    def signal_params(self):
        return [self.avg_value(), self.abs_avg_value(), self.avg_power(), self.variance(), self.root_mean_square()]

    def plot_signal(self):
        plt.plot(self.t, self.y)
        plt.title(f'{self}')
        plt.xlabel('Czas[t]')
        plt.ylabel('Amplituda[A]')
        plt.grid(True)
        plt.show()

    def histogram_signal(self, bins=50):
        plt.hist(self.y, bins=bins, edgecolor='black')
        plt.title(f'{self}')
        plt.xlabel('Amplituda [A]')
        plt.ylabel('Liczba próbek')
        plt.grid(True)
        plt.show()

    def __add__(self, other):
        pass

    def __repr__(self):
        return 'Sygnał'


class SinuosidalSignal(Signal):
    def __init__(self, A, t1, d, T):
        super().__init__(A, t1, d)
        self.T = T
        self.f = 1 / self.T

    def generate_signal(self):
        self.generate_t()
        self.y = [self.A * np.sin(2 * np.pi / self.T * (t - self.t1)) for t in self.t]

    def __repr__(self):
        return super().__repr__() + ' sinusoidalny'


class SinusoidalOneHalfSignal(Signal):
    def __init__(self, A, t1, d, T):
        super().__init__(A, t1, d)
        self.T = T
        self.f = 1 / self.T

    def generate_signal(self):
        self.generate_t()
        self.y = [0.5 * self.A * (
                np.sin(2 * np.pi / self.T * (t - self.t1)) + abs(np.sin(2 * np.pi / self.T * (t - self.t1))))
                  for t in self.t]

    def __repr__(self):
        return super().__repr__() + ' sinusoidalny wyprostowany jednopołówkowo'


class SinusoidalTwoHalfSignal(Signal):
    def __init__(self, A, t1, d, T):
        super().__init__(A, t1, d)
        self.T = T
        self.f = 1 / self.T

    def generate_signal(self):
        self.generate_t()
        self.y = [self.A * abs(np.sin(2 * np.pi / self.T * (t - self.t1))) for t in self.t]

    def __repr__(self):
        return super().__repr__() + ' sinusoidalny wyprostowany dwupołówkowo'


class SquareSignal(Signal):
    def __init__(self, A, t1, d, T, kw):
        super().__init__(A, t1, d)
        self.kw = kw
        self.T = T
        self.f = 1 / self.T

    def generate_signal(self):
        self.generate_t()
        for t in self.t:
            k = int((t - self.t1) / self.T)
            if k * self.T + self.t1 <= t < self.kw * self.T + k * self.T + self.t1:
                self.y.append(self.A)
            elif self.kw * self.T - self.t1 <= t < self.T + k * self.T + self.t1:
                self.y.append(0)

    def __repr__(self):
        return super().__repr__() + ' prostokątny'


class SquareSimetricalSignal(Signal):
    def __init__(self, A, t1, d, T, kw):
        super().__init__(A, t1, d)
        self.kw = kw
        self.T = T
        self.f = 1 / self.T

    def generate_signal(self):
        self.generate_t()
        for t in self.t:
            k = int((t - self.t1) / self.T)
            if k * self.T + self.t1 <= t < self.kw * self.T + k * self.T + self.t1:
                self.y.append(self.A)
            elif self.kw * self.T + self.t1 <= t < self.T + k * self.T + self.t1:
                self.y.append(self.A * (-1))

    def __repr__(self):
        return super().__repr__() + ' prostokątny symetryczny'


class TriangleSignal(Signal):
    def __init__(self, A, t1, d, T, kw):
        super().__init__(A, t1, d)
        self.kw = kw
        self.T = T
        self.f = 1 / self.T

    def generate_signal(self):
        self.generate_t()
        for t in self.t:
            k = int((t - self.t1) / self.T)
            if k * self.T + self.t1 <= t < self.kw * self.T + k * self.T + self.t1:
                self.y.append(self.A / (self.kw * self.T) * (t - k * self.T - self.t1))
            elif self.kw * self.T + self.t1 + k * self.T <= t < self.T + k * self.T + self.t1:
                self.y.append(
                    (self.A * (-1)) / ((1 - self.kw) * self.T) * (t - k * self.T - self.t1) + self.A / (1 - self.kw))

    def __repr__(self):
        return super().__repr__() + ' trójkątny'


class UnitJump(Signal):
    def __init__(self, A, t1, d, ts):
        super().__init__(A, t1, d)
        self.ts = ts

    def generate_signal(self):
        self.generate_t()
        for t in self.t:
            if t > self.ts:
                self.y.append(self.A)
            elif t == self.ts:
                self.y.append(0.5 * self.A)
            elif t < self.ts:
                self.y.append(0)

    def __repr__(self):
        return 'Skok jednostkowy'


class UniformlyDistributedNoise(Signal):
    def generate_signal(self):
        self.generate_t()
        self.y = [random.uniform(self.A, self.A * (-1)) for _ in self.t]

    def __repr__(self):
        return 'Szum o rozkładzie jednostajnym'


class GaussianNoise(Signal):
    def generate_signal(self):
        self.generate_t()
        self.y = [random.gauss(self.A, self.A * (-1)) for _ in self.t]

    def __repr__(self):
        return 'Szum gaussowski'


class DiscreteSignal(Signal, ABC):
    def __init__(self, A, t1, d):
        super().__init__(A, t1, d)

    def generate_t(self):
        self.t = np.linspace(self.n1, self.n2, self.n2 - self.n1 + 1)

    def plot_signal(self):
        plt.scatter(self.t, self.y)
        plt.title(f'{self}')
        plt.xlabel('Czas[t]')
        plt.ylabel('Amplituda[A]')
        plt.grid(True)
        plt.show()


class UnitImpulse(DiscreteSignal):
    def __init__(self, A, t1, d, ns):
        super().__init__(A, t1, d)
        self.ns = ns

    def generate_signal(self):
        self.generate_t()
        for t in self.t:
            if np.floor(t - self.ns) == 0:
                self.y.append(self.A)
            else:
                self.y.append(0)

    def __repr__(self):
        return 'Impuls jednostkowy'


class ImpulseNoise(DiscreteSignal):
    def __init__(self, A, t1, d, p):
        super().__init__(A, t1, d)
        self.p = p

    def generate_signal(self):
        self.generate_t()
        self.y = [self.A if np.random.uniform(0, 1) < self.p else 0 for _ in self.t]

    def __repr__(self):
        return 'Szum impulsowy'
