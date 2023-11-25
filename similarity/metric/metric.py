

from omegaconf import DictConfig


class Metric:
    def __init__(self, metric, fit_score, score=None, fit=None, interface=None):
        self._metric = metric
        self._score = score
        self._fit = fit
        self._fit_score = fit_score

        if interface is None:
            interface = {
                "fit": "fit",
                "score": "score",
                "fit_score": "fit_score"
            }
        else:
            assert isinstance(interface, (dict, DictConfig))

        impls = {
            "fit": self._fit_impl,
            "score": self._score_impl,
            "fit_score": self._fit_score_impl
        }
        self.impls = {}
        # use interface to rename impls keys
        for k, v in impls.items():
            new_k = interface.get(k, k)
            self.impls[new_k] = v

    def _fit_impl(self, X, Y):
        if self._fit is not None:
            self._fit(metric=self._metric, X=X, Y=Y)

    def _score_impl(self, X, Y):
        return self._score(metric=self._metric, X=X, Y=Y)

    def _fit_score_impl(self, X, Y):
        if self._fit_score is not None:
            return self._fit_score(metric=self._metric, X=X, Y=Y)
        else:
            self._fit_impl(X, Y)
            return self._score_impl(X, Y)



    # def fit(self, X, Y):
    #     if self._fit is not None:
    #         self._fit(metric=self._metric, X=X, Y=Y)

    # def score(self, X, Y):
    #     return self._score(metric=self._metric, X=X, Y=Y)

    # def fit_score(self, X, Y):
    #     if self._fit_score is not None:
    #         return self._fit_score(metric=self._metric, X=X, Y=Y)
    #     else:
    #         self.fit(X, Y)
    #         return self.score(X, Y)

    def __getattr__(self, name):
        # prevent accessing private attributes
        if name.startswith("_"):
            raise AttributeError(name)

        # call the implementation
        if name in self.impls:
            return self.impls[name]

        # if attr is not found in this class, try the metric
        return getattr(self._metric, name)

    def __call__(self, X, Y):
        # have to handle __call__ separately
        if "__call__" in self.impls:
            return self.impls["__call__"](X, Y)
        else:
            raise TypeError(f"'{self.__class__.__name__}' object is not callable")


class MetricInterface:
    def __init__(self, metric, interface):
        self._metric = metric
        self._interface = interface