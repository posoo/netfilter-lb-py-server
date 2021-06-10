# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import http.server
import socketserver
import socket, struct
import time

PORT = 80
UPDATE_FLOW_PROC_FILE = '/proc/netfilter-lb/update_flow'


def dottedQuadToNum(ip):
    "convert decimal dotted quad string to long integer"
    return struct.unpack('>L',socket.inet_aton(ip))[0]


def numToDottedQuad(n):
    "convert long int to dotted quad string"
    return socket.inet_ntoa(struct.pack('>L',n))


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/data') and self.path.endswith('.bin'):
            f_size = self.path.split('/')[-1].split('.')[0]
            print(f'flow_size: {f_size} bytes, src_addr: {self.client_address[0]}, src_port: {self.client_address[1]}')
            try:
                with open(UPDATE_FLOW_PROC_FILE, 'wb') as f:
                    f.write(struct.pack('I', socket.ntohl(dottedQuadToNum(self.client_address[0]))))
                    f.write(struct.pack('H', socket.ntohs(self.client_address[1])))
                    f.write(struct.pack('I', int(f_size)))
            except Exception as err:
                print(err)
        print(self.command)
        print(self.path)
        print(time.ctime())
        rval = http.server.SimpleHTTPRequestHandler.do_GET(self)
        print("GET DONE")
        return rval


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    handler = MyHttpRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Web Server started at port: {PORT}")
        # httpd.ser
        httpd.serve_forever()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
