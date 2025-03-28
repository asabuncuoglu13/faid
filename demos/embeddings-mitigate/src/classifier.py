import numpy as np

# an abstract class for linear classifiers
class Classifier(object):
    def __init__(self):
        pass

    def train(self, X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray) -> float:
        """
        :param X_train:
        :param y_train:
        :param X_test:
        :param y_test:
        :return: accuracy score on the dev set
        """
        raise NotImplementedError

    def get_weights(self) -> np.ndarray:
        """
        :return: final weights of the model, as np array
        """
        raise NotImplementedError

class SKlearnClassifier(Classifier):

    def __init__(self, m):
        """
        :param m: a sklearn model
        """
        self.model = m

    def train_network(self, X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray) -> float:
        """
        :param X_train:
        :param y_train:
        :param X_test:
        :param y_test:
        :return: accuracy score on the dev set / Person's R in the case of regression
        """
        self.model.fit(X_train, y_train)
        score = self.model.score(X_test, y_test)
        return score

    def get_weights(self) -> np.ndarray:
        """
        :return: final weights of the model, as np array
        """
        w = self.model.coef_
        if len(w.shape) == 1:
                w = np.expand_dims(w, 0)

        return w
