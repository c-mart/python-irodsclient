class iRODSMeta(object):
    def __init__(self, name, value, units=None, id=None):
        self.id = id
        self.name = name
        self.value = value
        self.units = units

    def __repr__(self):
        return "<iRODSMeta (%s, %s, %s, %s)>" % (
            self.name, self.value, self.units, str(self.id)
        )

class iRODSMetaCollection(object):

    def __init__(self, sess, model_cls, path):
        self._sess = sess
        self._model_cls = model_cls
        self._path = path
        self._reset_metadata()

    def _reset_metadata(self):
        self._meta = self._sess.get_meta(self._model_cls, self._path)

    def get_all(self, key):
        """
        Returns a list of iRODSMeta associated with a given key
        """
        if not isinstance(key, str):
            raise TypeError
        return [m for m in self._meta if m.name == key]

    def get_one(self, key):
        """
        Returns the iRODSMeta defined for a key. If there are none,
        of if there are more than one defined, raises KeyError
        """
        values = self.get_all(key)
        if not values:
            raise KeyError
        if len(values) > 1:
            raise KeyError
        return values[0]

    def add(self, meta):
        """
        Add as iRODSMeta to a key
        """
        self._sess.add_meta(self._model_cls, self._path, meta)
        self._reset_metadata()

    def remove(self, meta):
        """
        Removes an iRODSMeta
        """
        self._sess.remove_meta(self._model_cls, self._path, meta)
        self._reset_metadata()
    
    def items(self):
        """
        Returns a list of iRODSMeta
        """
        return self._meta

    def keys(self):
        """
        Return a list of keys. Duplicates preserved
        """
        return [m.name for m in self._meta]
        
    def __getitem__(self, key):
        """
        Returns the first iRODSMeta defined on key. Order is
        undefined. Use get_one() or get_all() instead
        """
        values = self.get_all(key)
        if not values:
            return KeyError 
        return values[0]

    def __setitem__(self):
        """
        Deletes all existing values associated with a given key and associates
        the key with a single iRODSMeta tuple
        """
        self._delete_all_values(key)
        self.add(self, meta)

    def _delete_all_values(self, key):
        for meta in self.get_all(key):
            self.remove(self, meta)

    def __delitem__(self, key):
        """
        Deletes all existing values associated with a given key
        """
        if not isinstance(key, str):
            raise TypeError
        self._delete_all_values(key)
        self._reset_metadata()

    def __contains__(self, key):
        if not isinstance(key, str):
            raise TypeError
        values = self.get_all(key)
        return len(values) > 0