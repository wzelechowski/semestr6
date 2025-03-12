import Signal
import inspect

signal = None


def generate_signal(signal_class):
    signature = inspect.signature(signal_class.__init__)
    params = signature.parameters
    params = [param for param in params if param != 'self']
    global signal
    try:
        values = []
        for param in params:
            values.append(float(input(f'{param}: ')))
        signal = signal_class(*values)
        signal.generate_t()
        signal.generate_signal()
        print('Sygnał wygenerowany pomyślnie\n')
    except ValueError:
        print('Błędny format danych\n')


def generate_plot():
    try:
        global signal
        signal.plot_signal()
        print('Wykres wygenerowany pomyślnie\n')
    except AttributeError:
        print("Musisz najpierw wygenerować sygnał\n")


def generate_histogram():
    pass


variants = {
    'Szum o rozkładzie jednostajnym': (generate_signal, Signal.UniformlyDistributedNoise),
    'Szum gaussowski': (generate_signal, Signal.GaussianNoise),
    'Sygnał sinusoidalny': (generate_signal, Signal.SinuosidalSignal),
    'Sygnał sinusoidalny wyprostowany jednopołówkowo': (generate_signal, Signal.SinusoidalOneHalfSignal),
    'Sygnał sinusoidalny wyprostowany dwupołówkowo': (generate_signal, Signal.SinusoidalTwoHalfSignal),
    'Sygnał prostokątny': (generate_signal, Signal.SquareSignal),
    'Sygnał prostokątny symetryczny': (generate_signal, Signal.SquareSimetricalSignal),
    'Sygnał trójkątny': (generate_signal, Signal.TriangleSignal),
    'Skok jednostkowy': (generate_signal, Signal.UnitJump),
    'Impuls jednostkowy': (generate_signal, Signal.UnitImpulse),
    'Szum impulsowy': (generate_signal, Signal.ImpulseNoise)
}

io = ['Zapisz', 'Wczytaj']

operations = ['Dodawanie', 'Odejmowanie', 'Mnożenie', 'Dzielenie']

graphs = {'Wykres': generate_plot, 'Histogram': generate_histogram}

modes = {'Generuj sygnał lub szum': variants,
         'Zapis lub odczyt': io,
         'Podstawowe działania na sygnałach': operations,
         'Reprezentacja graficzna': graphs,
         'Zakończ': None}

if __name__ == '__main__':
    while True:
        for index, mode in enumerate(modes, 1):
            print(f'{index}. {mode}')

        mode_number = None
        while True:
            try:
                mode_number = int(input('Podaj numer: '))
                if 1 <= mode_number <= len(modes):
                    break
                else:
                    raise ValueError('Błędny numer\n')
            except ValueError as e:
                print(f'{e}\n')

        if mode_number == 5:
            break
        selected_mode = list(modes.keys())[mode_number - 1]
        options = modes[selected_mode]

        for index, option in enumerate(options, 1):
            print(f'{index}: {option}')

        while True:
            try:
                option_number = int(input('Podaj numer: '))
                if 1 <= option_number <= len(options):
                    break
                else:
                    raise ValueError('Błędny numer\n')
            except ValueError as e:
                print(f'{e}\n')

        selected_option = list(options.keys())[option_number - 1]
        option = options[selected_option]
        if type(option) is tuple:
            f, x = option
            f(x)
        else:
            option()
