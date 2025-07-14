class DummySession:
    def __init__(self):
        self.storage = []

    def add(self, obj):
        self.storage.append(obj)

    def commit(self):
        pass

    def query(self, model):
        class Q:
            def __init__(self, storage):
                self.storage = storage

            def get(self, _):
                return None

            def filter_by(self, **filters):
                class F:
                    def __init__(self, results):
                        self._results = results

                    def all(self):
                        return self._results

                filtered = [u for u in self.storage if all(getattr(u, k) == v for k, v in filters.items())]
                return F(filtered)

        return Q(self.storage)
