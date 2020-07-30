import os
import random

from MySQL.Mapping import mapping
from config import nif


class Mapping():
    ''' Port forwarding mapping. '''

    def __init__(self, address):
        self.address = address

    def get(self):
        try:
            mapped = mapping.get_mapping_by_address(self.address)

            return mapped
        except Exception as e:
            print('Cannot get forward mapping. ', e)
            return []

    def view(self, destination_port: int, protocol: str):
        try:
            mapped = mapping.get_mapping(
                self.address, destination_port, protocol)

            return mapped
        except Exception as e:
            print('Cannot view forward mapping. ', e)
            return None

    def create(self, destination_port: int, protocol: str):
        try:
            if destination_port is not None:
                exists = mapping.get_mapping(
                    self.address, destination_port, protocol)

                if exists is not None:
                    return exists

            source_port = Mapping.generate_port(protocol)
            if destination_port is None:
                destination_port = source_port

            success = mapping.create_mapping(
                self.address, protocol, source_port, destination_port)

            if success is None:
                return None

            os.system(
                f'iptables -t nat -A PREROUTING -p {protocol} --dport {source_port} -j DNAT --to {self.address}:{destination_port}')

            mapped = mapping.get_mapping_by_port(source_port, protocol)

            return mapped
        except Exception as e:
            print('Cannot add forward mapping. ', e)
            return None

    def delete(self, destination_port: int, protocol: str):
        try:
            exists = mapping.get_mapping(
                self.address, destination_port, protocol)

            if exists is None:
                return True

            source_port = exists['source_port']
            success = mapping.delete_mapping(
                self.address, destination_port, protocol)

            os.system(
                f'iptables -t nat -D PREROUTING -p {protocol} --dport {source_port} -j DNAT --to {self.address}:{destination_port}')

            return success
        except Exception as e:
            print('Cannot remove forward mapping. ', e)
            return False

    @staticmethod
    def sync():
        os.system('iptables -F')
        os.system(f'iptables -t nat -A POSTROUTING -o {nif} -j MASQUERADE')

        mappings = mapping.get_all_mapping()
        for m in mappings:
            source_port = m['source_port']
            address = m['address']
            destination_port = m['destination_port']
            protocol = m['protocol']

            try:
                print(
                    f'Routing {source_port} -> {address}:{destination_port}/{protocol}')

                os.system(
                    f'iptables -t nat -D PREROUTING -p {protocol} --dport {source_port} -j DNAT --to {address}:{destination_port}')
            except:
                print(
                    f'Cannot routing {source_port}-> {address}:{destination_port}/{protocol}')

    @staticmethod
    def generate_port(protocol: str):
        port = None
        while (True):
            try:
                # random port
                port = random.randint(10000, 49151)
                mapped = mapping.get_mapping_by_port(port, protocol)
                if mapped is None:
                    return port
            except Exception as err:
                continue
