#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np
from typing import Callable
import tensorflow as tf
from tabulate import tabulate


class Metrics:
    def __init__(self, model, predict_func: Callable):
        self.model = model
        self.predict_func = predict_func

    def accuracy(self, x, y: np.array, verbose=True):
        y_pred = self.predict_func(self.model, x)
        acc = accuracy_score(y, y_pred)
        if verbose:
            print(f"Dokładność: {acc}")
        return acc

    def precision(self, x, y: np.array, average=None, verbose=True):
        y_pred = self.predict_func(self.model, x)
        prec = precision_score(y, y_pred, average=average)
        if verbose:
            print(f"Precyzja: {prec}")
        return prec

    def recall(self, x, y: np.array, average=None, verbose=True):
        y_pred = self.predict_func(self.model, x)
        rec = recall_score(y, y_pred, average=average)
        if verbose:
            print(f"Czułość: {rec}")
        return rec

    def f1(self, x, y: np.array, average=None, verbose=True):
        y_pred = self.predict_func(self.model, x)
        f1_sc = f1_score(y, y_pred, average=average)
        if verbose:
            print(f"F1: {f1_sc}")
        return f1_sc

    def print_confusion_matrix(self, x, y: np.array):
        y_pred = self.predict_func(self.model, x)
        print(confusion_matrix(y, y_pred))

    def print_metrics(self, x, y, average=None):
        acc = np.around(self.accuracy(x, y, False), 3)
        prec = np.around(self.precision(x, y, average, False), 3)
        rec = np.around(self.recall(x, y, average, False), 3)
        f1 = np.around(self.f1(x, y, average, False), 3)
        metrics_array = np.vstack((prec, rec, f1))
        print(tabulate(metrics_array, tablefmt="fancy_grid"))
        print(f"Dokładność: {acc}")
