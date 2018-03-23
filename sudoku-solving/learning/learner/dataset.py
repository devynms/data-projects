import numpy as np
from zipfile import ZipFile
from io import BytesIO

def load_whole_dataset(path):
    archive = ZipFile(path)
    with archive.open('quizzes.npy') as quizzes_file:
        quizzes_data = quizzes_file.read()
    quizzes = np.load(BytesIO(quizzes_data))
    del quizzes_data
    with archive.open('solutions.npy') as solutions_file:
        solutions_data = solutions_file.read()
    solutions = np.load(BytesIO(solutions_data))
    del solutions_data
    return (quizzes, solutions)

