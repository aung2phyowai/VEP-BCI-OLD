__author__ = 'Anti'

import emokit.emotiv
from Crypto.Cipher import AES
from Crypto import Random

sensorBits = {
    'F3': [10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7],
    'FC5': [28, 29, 30, 31, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9],
    'AF3': [46, 47, 32, 33, 34, 35, 36, 37, 38, 39, 24, 25, 26, 27],
    'F7': [48, 49, 50, 51, 52, 53, 54, 55, 40, 41, 42, 43, 44, 45],
    'T7': [66, 67, 68, 69, 70, 71, 56, 57, 58, 59, 60, 61, 62, 63],
    'P7': [84, 85, 86, 87, 72, 73, 74, 75, 76, 77, 78, 79, 64, 65],
    'O1': [102, 103, 88, 89, 90, 91, 92, 93, 94, 95, 80, 81, 82, 83],
    'O2': [140, 141, 142, 143, 128, 129, 130, 131, 132, 133, 134, 135, 120, 121],
    'P8': [158, 159, 144, 145, 146, 147, 148, 149, 150, 151, 136, 137, 138, 139],
    'T8': [160, 161, 162, 163, 164, 165, 166, 167, 152, 153, 154, 155, 156, 157],
    'F8': [178, 179, 180, 181, 182, 183, 168, 169, 170, 171, 172, 173, 174, 175],
    'AF4': [196, 197, 198, 199, 184, 185, 186, 187, 188, 189, 190, 191, 176, 177],
    'FC6': [214, 215, 200, 201, 202, 203, 204, 205, 206, 207, 192, 193, 194, 195],
    'F4': [216, 217, 218, 219, 220, 221, 222, 223, 208, 209, 210, 211, 212, 213]
}


class myEmotiv(emokit.emotiv.Emotiv):
    def __init__(self, connection, args):
        self.lock = args[0]
        self.lock.acquire()
        self.connection = connection
        self.devices = []
        self.serialNum = None
        emokit.emotiv.Emotiv.__init__(self)
        self.cipher = None
        self.prev_counter = None
        self.myMainloop()

    def myMainloop(self):
        while True:
            while not self.connection.poll(1):
                pass
            message = self.connection.recv()
            if message == "Start":
                print "Starting emotiv"
                message = self.run()
                self.lock.acquire()
                self.cleanUp()
                if message == "Stop":
                    print "Emotiv stopped"
            if message == "Exit":
                print "Exiting emotiv"
                break

    def setupWin(self):
        for device in emokit.emotiv.hid.find_all_hid_devices():
            if device.vendor_id != 0x21A1 and device.vendor_id != 0x1234:
                continue
            if device.product_name == 'Brain Waves':
                self.devices.append(device)
                device.open()
                self.serialNum = device.serial_number
                device.set_raw_data_handler(self.handler)
            elif device.product_name == 'EPOC BCI':
                self.devices.append(device)
                device.open()
                self.serialNum = device.serial_number
                device.set_raw_data_handler(self.handler)
            elif device.product_name == '00000000000':
                self.devices.append(device)
                device.open()
                self.serialNum = device.serial_number
                device.set_raw_data_handler(self.handler)
            elif device.product_name == 'Emotiv RAW DATA':
                self.devices.append(device)
                device.open()
                self.serialNum = device.serial_number
                device.set_raw_data_handler(self.handler)

    def closeDevices(self):
        for device in self.devices:
            device.close()

    def handler(self, data):
        assert data[0] == 0
        self.packets.put_nowait(''.join(map(chr, data[1:])))
        return True

    def cleanUp(self):
        self._goOn = False
        self.closeDevices()

    def setupCrypto(self, sn):
        type = 0 # feature[5]
        type &= 0xF
        type = 0
        # I believe type == True is for the Dev headset, I'm not using that. That's the point of this library in the first place I thought.
        k = ['\0'] * 16
        k[0] = sn[-1]
        k[1] = '\0'
        k[2] = sn[-2]
        if type:
            k[3] = 'H'
            k[4] = sn[-1]
            k[5] = '\0'
            k[6] = sn[-2]
            k[7] = 'T'
            k[8] = sn[-3]
            k[9] = '\x10'
            k[10] = sn[-4]
            k[11] = 'B'
        else:
            k[3] = 'T'
            k[4] = sn[-3]
            k[5] = '\x10'
            k[6] = sn[-4]
            k[7] = 'B'
            k[8] = sn[-1]
            k[9] = '\0'
            k[10] = sn[-2]
            k[11] = 'H'
        k[12] = sn[-3]
        k[13] = '\0'
        k[14] = sn[-4]
        k[15] = 'P'
        # It doesn't make sense to have more than one greenlet handling this as data needs to be in order anyhow. I guess you could assign an ID or something
        # to each packet but that seems like a waste also or is it? The ID might be useful if your using multiple headsets or usb sticks.
        key = ''.join(k)
        iv = Random.new().read(AES.block_size)
        self.cipher = AES.new(key, AES.MODE_ECB, iv)

    def run(self):
        # Clean up possible previous packets from the queue
        while True:
            try:
                self.packets.get(False)
            except:
                break

        # Make sure we get packets
        self.setupWin()
        if self.serialNum is None:
            print("USB not connected")
            return "Stop"
        self.setupCrypto(self.serialNum)
        # try:
        #     task = self.packets.get(True, 0.1)
        # except:
        #     print "Turn on headset"
        #     return "Stop"

        # Mainloop
        self.lock.release()  # synchronising with psychopy
        while True:
            try:
                task = self.packets.get(True, 0.01)
                data = self.cipher.decrypt(task[:16]) + self.cipher.decrypt(task[16:])
                self.detectPacketLoss(self.getCounter(data))
                #values = {name: self.get_level(data, bits) for name, bits in sensorBits.items()}
                packet = emokit.emotiv.EmotivPacket(data, self.sensors)
                self.connection.send(packet)
                self.printPacket(packet)
                self.checkQueueSize()
            except Exception, e:
                print("Exception: "+ str(e))
            if self.connection.poll():
                return self.connection.recv()

    def get_level(self, data, bits):
        level = 0
        for i in range(13, -1, -1):
            level <<= 1
            b, o = (bits[i] / 8) + 1, bits[i] % 8
            level |= (ord(data[b]) >> o) & 1
        return level

    def checkQueueSize(self):
        if self.packets.qsize() > 6:
            print (str(self.packets.qsize()) + " packets in queue.")

    def printPacket(self, packet):
        print(str(packet.sensors["O1"]["value"]))

    def getCounter(self, data):
        counter = ord(data[0])
        if counter > 127:
            counter = 128
        return counter

    def detectPacketLoss(self, counter):
        if counter != 0 and counter-1 != self.prev_counter and self.prev_counter is not None or counter == 0 and self.prev_counter != 128:
            print("Packet(s) lost!", self.prev_counter, counter)
        self.prev_counter = counter
