import yaml

class Cache:
    """
        The Cache object is a singleton class holding a persistent state which
        is read upon creation and saved upon exit. As of now, info is kept
        into a yaml file (and the class itself is a dictionary).
    """
    #
    # singleton pattern scheme
    #
    class __Cache__(dict):

        def __init__(self, cache_path):
            self.cache_path = cache_path

        #
        # TODO: add persistency here
        #

    instance = None

    def __new__(cls, cache_path):
        if not Cache.instance:
            Cache.instance = Cache.__Cache__(cache_path)
        return Cache.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)
