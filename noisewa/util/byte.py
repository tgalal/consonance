class ByteUtil(object):
    @staticmethod
    def split(input, first_len, second_len, third_len=None):
        """
        :param input:
        :type input: bytes
        :param first_len:
        :type first_len: int
        :param second_len:
        :type second_len: int
        :param third_len:
        :type third_len: int
        :return:
        :rtype:
        """
        parts = []
        parts.append(input[:first_len])
        parts.append(input[first_len:first_len + second_len])
        if third_len is not None:
            parts.append(input[first_len + second_len: first_len + second_len + third_len])
        return parts
