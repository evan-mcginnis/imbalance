#
# U T I L I T Y
#
class Utility:
    @classmethod
    def validAsFilename(cls, name: str) -> str:
        """
        Returns a string that can be used as a window filename.
        Invalid characters are changed to undersocre.
        :param name:
        :return:
        """
        partial = name.replace('.', '_')
        return partial.replace(':', 'to')
