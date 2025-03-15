import os
import pickle
from tkinter import filedialog, Tk
import Signal
import inspect

signal1 = None
signal2 = None


def generate_signal(signal_class):
    signature = inspect.signature(signal_class.__init__)
    params = signature.parameters
    params = [param for param in params if param != 'self']
    global signal1
    try:
        values = []
        for param in params:
            values.append(float(input(f'{param}: ')))
        signal1 = signal_class(*values)
        signal1.generate_t()
        signal1.generate_signal()
        results = signal1.signal_params()
        for result in results:
            print(result[0], result[1])
        print('Sygnał wygenerowano pomyślnie\n')
    except ValueError:
        print('Błędny format danych\n')


def generate_plot():
    global signal1
    try:
        signal1.plot_signal()
        print('Wykres wygenerowany pomyślnie\n')
    except AttributeError:
        print("Musisz najpierw wygenerować sygnał\n")


def generate_histogram():
    global signal1
    try:
        signal1.histogram_signal()
        print('Histogram wygenerowany pomyślnie\n')
    except AttributeError:
        print("Musisz najpierw wygenerować sygnał\n")


def write():
    root = Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', 1)

    filepath = filedialog.asksaveasfilename(
        initialdir=os.getcwd() + '/files/',
        defaultextension=".pkl",
        filetypes=[("Pickle Files", "*.pkl")],
        initialfile=f"{signal1}.pkl",
    )

    try:
        if filepath:
            if not filepath.endswith(".pkl"):
                filepath += ".pkl"

            with open(filepath, 'wb') as f:
                pickle.dump(signal1, f)
                print(f"Obiekt zapisany w: {filepath}\n")
    except IOError as e:
        print(f'Błąd zapisu {e}')


def read():
    global signal2
    root = Tk()
    root.withdraw()
    root.lift()
    root.attributes('-topmost', 1)

    filepath = filedialog.askopenfilename(initialdir=os.getcwd() + '/files/', filetypes=[("Pickle Files", "*.pkl")])
    try:
        if filepath:
            with open(filepath, 'rb') as f:
                signal2 = pickle.load(f)
                print(f"Załadowany obiekt: {signal2}\n")
    except FileNotFoundError as e:
        print(f'Taki plik nie istnieje {e}')


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
    'Szum impulsowy': (generate_signal, Signal.ImpulseNoise),
    'Powrót': None
}

io = {'Zapisz': write, 'Wczytaj': read, 'Powrót': None}

operations = {'Dodawanie': lambda: signal1 + signal2,
              'Odejmowanie': lambda: signal1 - signal2,
              'Mnożenie': lambda: signal1 * signal2,
              'Dzielenie': lambda: signal1 / signal2,
              'Powrót': None
}

graphs = {'Wykres': generate_plot, 'Histogram': generate_histogram, 'Powrót': None}

modes = {'Generuj sygnał lub szum': variants,
         'Zapis lub odczyt': io,
         'Podstawowe działania na sygnałach': operations,
         'Reprezentacja graficzna': graphs,
         'Zakończ': None
}

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
        try:
            if type(option) is tuple:
                f, x = option
                f(x)
            else:
                option()
        except (AttributeError, TypeError) as e:
            print(e)
