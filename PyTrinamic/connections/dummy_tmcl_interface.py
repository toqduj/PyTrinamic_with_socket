from PyTrinamic.connections.TmclInterface import TmclInterface


class dummy_tmclInterface(TmclInterface):

    def __init__(self, port, datarate=115200, host_id=2, module_id=1, debug=True):
        """
        Opens a dummy TMCL connection
        """
        if type(port) != str:
            raise TypeError

        del debug

        TmclInterface.__init__(self, host_id, module_id, debug=True)

        if self._debug:
            print("Opened dummy TMCL interface on port '" + port + "'")
            print("\tData rate:  " + str(datarate))
            print("\tHost ID:    " + str(host_id))
            print("\tModule ID:  " + str(module_id))

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, traceback):
        """
        Close the connection at the end of a with-statement block.
        """
        del exit_type, value, traceback
        self.close()

    def close(self):
        """
        Closes the dummy TMCL connection
        """
        if self._debug:
            print("Closed dummy TMCL interface")

    def _send(self, host_id, module_id, data):
        """
            Send the bytearray parameter [data].

            This is a required override function for using the tmcl_interface
            class.
        """
        del host_id, module_id, data
        pass

    def _recv(self, host_id, module_id):
        """
            Read 9 bytes and return them as a bytearray.

            This is a required override function for using the tmcl_interface
            class.
        """
        del host_id, module_id

        return bytearray(9)

    def print_info(self):
        print("Connection: type=dummy_tmcl_interface")

    # @staticmethod
    def supports_tmcl(self):
        return True

    # @staticmethod
    # def supportsCANopen():
    #    return False

    #@staticmethod
    def list(self):
        """
            Return a list of available connection ports as a list of strings.

            This function is required for using this interface with the
            connection manager.
        """
        return ["dummy"]


if __name__ == "__main__":
    interface = dummy_tmclInterface("dummy")

    interface.get_version_string()
    interface.send_boot()

    interface.close()
