from pyqtgraph import QtCore

import socket
import struct

chooseMuse = True

class UDPThread(QtCore.QThread):
  newPacket = QtCore.pyqtSignal(object)
  
  def __init__(self, port=8888):
    super(UDPThread, self).__init__()

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    self.socket.bind(('127.0.0.1', port))

    self.buffer = []

  def run(self):
    if chooseMuse:
      while True:
        unpacker = struct.Struct("fffff")
        data  = self.socket.recv(unpacker.size)
        data = unpacker.unpack(data)
        self.newPacket.emit(data)
    else:
      while True:
        data, addr = self.socket.recvfrom(1024)
        data = eval(data)
        
        self.newPacket.emit(eval(str(data)))
        #QtGui.QApplication.instance().processEvents()
