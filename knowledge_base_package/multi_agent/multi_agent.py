import argparse
import multiaddr
import trio
import random
from libp2p import new_host
from libp2p.network.stream.net_stream_interface import INetStream
from libp2p.peer.peerinfo import info_from_p2p_addr
from libp2p.typing import TProtocol
from threading import Thread
# based on https://github.com/libp2p/py-libp2p/blob/master/examples/chat/chat.py examples/chat/chat


PROTOCOL_ID = TProtocol("/chat/1.0.0")
MAX_READ_LEN = 2 ** 32 - 1
lis = []            # List with all IP address connected
json_strings = []   # List with all JSON string sended and received
subscriber = []     # List with all subscriber of observer


def add_observ(observ):
    subscriber.append(observ)


def remove_observ(observ):
    subscriber.remove(observ)


def notify(element):
    for observ in subscriber:
        observ.update(element)


def add_lis(ip):
    lis.append(ip)


async def read_data(stream: INetStream) -> None:
    # Connect to DataBase
    try:
        read_bytes = await stream.read(MAX_READ_LEN)
        if read_bytes is not None:
            read_string = read_bytes.decode()
            if read_string != "\n":
                if read_string not in lis and "search" not in read_string and "visited" not in read_string:
                    lis.append(read_string)
                    notify(read_string)
                    print("\x1b[32m %s\x1b[0m " % read_string, end="\n")
                elif read_string not in json_strings and "search" in read_string:
                    json_strings.append(read_string)
                    notify(read_string)
                    print("\x1b[32m %s\x1b[0m " % read_string, end="\n")
                elif read_string not in json_strings and "visited" in read_string:
                    json_strings.append(read_string)
                    notify(read_string)
                    print("\x1b[32m %s\x1b[0m " % read_string, end="\n")
    except:
        pass


class MultiAgent(Thread):
    def __init__(self, inp):
        Thread.__init__(self)
        self.inp = inp

    async def __write_data_json(self, streams: INetStream) -> None:
        await trio.sleep(1)
        for key, stream in streams.items():
            if len(lis) > 0 and len(json_strings) > 0:
                ind = random.randint(1, len(json_strings)) - 1
                try:
                    await stream.write(json_strings[ind].encode())
                except:
                    if key in streams.keys():
                        lis.remove(key)
                        notify(str(len(lis)) + "delete " + key)

    async def __write_data(self, streams: INetStream) -> None:
        await trio.sleep(1)
        for key, stream in streams.items():
            if len(lis) > 0:
                ind = random.randint(1, len(lis)) - 1
                try:
                    await stream.write(lis[ind].encode())
                except:
                    if key in streams.keys():
                        lis.remove(key)
                        notify(str(len(lis)) + "delete " + key)

    def setbootstrap(self, ip):
        lis.append(ip)

    def add_json(self, json_str):
        json_strings.append(json_str)

    async def run_host(self, port: int, dest) -> None:
        localhost_ip = "26.202.82.185"  # get('https://api.ipify.org').text
        listen_addr = multiaddr.Multiaddr(f"/ip4/0.0.0.0/tcp/{port}")
        host = new_host()
        host.get_mux()

        async with host.run(listen_addrs=[listen_addr]), trio.open_nursery() as nursery:
            code = host.get_id().pretty()

            print(
                "_.--.__.-'\"\"`-.__.--.__.-'\"\"`-.__.--.__.-'\"\"`-.__.--.__.-'\"\"`-.__.--.__.-'\"\"`-.__.--.__.-'\"\"`-.__.--.__.-'\"\"`-.__.--.__.-'\"\"`-.__.--.__.-'\"\"`-._")
            print(
                f"Run 'python ./multi_agent_test.py "
                f"-p {int(port)} "
                f"-d /ip4/{localhost_ip}/tcp/{port}/p2p/{code}' "
                "on another console."
            )
            print(
                "\"`--'\"\"`-.__.-'\"\"`--'\"\"`-.__.-'\"\"`--'\"\"`-.__.-'\"\"`--'\"\"`-.__.-'\"\"`--'\"\"`-.__.-'\"\"`--'\"\"`-.__.-'\"\"`--'\"\"`-.__.-'\"\"`--'\"\"`-.__.-'\"\"`--'\"\"`-.__.-'\"\"")

            my_ip = f"/ip4/{localhost_ip}/tcp/{port}/p2p/{code}"
            lis.append(my_ip)
            notify(my_ip)

            while True:
                try:
                    streams = dict()
                    for count in lis:
                        try:
                            if localhost_ip not in count:
                                maddr = multiaddr.Multiaddr(count)
                                info = info_from_p2p_addr(maddr)
                                await host.connect(info)
                                streams[count] = await host.new_stream(info.peer_id, [PROTOCOL_ID])
                        except:
                            lis.remove(count)
                            notify(str(len(lis)) + "delete " + count)

                        async def stream_handler(stream: INetStream) -> None:
                            nursery.start_soon(read_data, stream)

                    nursery.start_soon(self.__write_data, streams)
                    nursery.start_soon(self.__write_data_json, streams)

                    host.set_stream_handler(PROTOCOL_ID, stream_handler)
                    await trio.sleep(1)
                except:
                    pass

    def main(self) -> None:

        parser = argparse.ArgumentParser(description="")
        parser.add_argument(
            "-p", "--port", default=8001, type=int, help="source port number"
        )
        # inp = input("Give bootstrap or 0\n")
        if self.inp != "0":
            self.setbootstrap(self.inp)

        parser.add_argument(
            "-d",
            "--destination",
            type=str,
            default=self.inp,
        )
        args = parser.parse_args()

        if not args.port:
            raise RuntimeError("was not able to determine a local port")

        try:
            trio.run(self.run_host, *(args.port, args.destination))
        except KeyboardInterrupt:
            pass

    def run(self):
        self.main()
