import sys
import logging
import hashlib
from CryptoPlus.Cipher import python_Twofish

_log = logging.getLogger(__name__)


class STFDecrypt:
    SQLITE_PAGESIZE = 1024
    SALT = bytes(bytearray.fromhex('2444335e472e385b'))
    MASTER_KEYS = {
        'core': bytearray.fromhex('41376f23566d29655473335b5f4b6675'),
        'data': bytearray.fromhex('5654384b6a5f342d644631312e336e2c'),
        'unknown': bytearray.fromhex('6674384b7172342d6446745662676363'),
        'game': bytearray.fromhex('4239294b54466771235f2464342c6445'),
        'map': bytearray.fromhex('444a3256682d355f446634342c345821')
    }

    @staticmethod
    def read_file_chunks(infile):
        contents = []
        with open(infile, 'rb') as f:
            for chunk in iter((lambda: f.read(STFDecrypt.SQLITE_PAGESIZE)), b''):
                contents.append(chunk)
        return contents

    @staticmethod
    def write_file_chunks(outfile, contents):
        with open(outfile, 'wb') as f:
            for c in contents:
                f.write(c)

    @staticmethod
    def get_iv(cmac_key, pageno):
        cmac_data = bytes([pageno & 0xff, (pageno >> 8) & 0xff, (pageno >> 16) & 0xff, (pageno >> 24) & 0xff])
        cipher = python_Twofish.new(cmac_key, python_Twofish.MODE_CMAC)
        return cipher.encrypt(cmac_data)

    def compute_keys(self, keyname):
        master_key = bytes(STFDecrypt.MASTER_KEYS[keyname])
        dkey = hashlib.pbkdf2_hmac('sha1', master_key, STFDecrypt.SALT, iterations=128, dklen=80)
        xts_key = (dkey[:32], dkey[32:64])
        cmac_key = dkey[64:]
        _log.info('\tdkey: {}'.format(dkey.hex()))
        _log.info('\tXTS key: {}'.format((xts_key[0].hex(), xts_key[1].hex())))
        _log.info('\tCMAC key: {}'.format(cmac_key.hex()))
        return xts_key, cmac_key

    def decrypt(self, keyname, infilename, outfilename):
        _log.info(f'Decrypting "{keyname}" from "{infilename}" to "{outfilename}"')
        xts_key, cmac_key = self.compute_keys(keyname)
        infile_chunks = self.read_file_chunks(infilename)
        chunks = []
        for pageno, page in enumerate(infile_chunks, start=1):
            iv = self.get_iv(cmac_key, pageno)
            decipher = python_Twofish.new(xts_key, mode=python_Twofish.MODE_XTS)
            chunks.append(decipher.decrypt(page, iv))
        self.write_file_chunks(outfilename, chunks)
        _log.info('Done!')

    def encrypt(self, keyname, infilename, outfilename):
        _log.info(f'Encrypting "{keyname}" from "{infilename}" to "{outfilename}"')
        xts_key, cmac_key = self.compute_keys(keyname)
        infile_chunks = self.read_file_chunks(infilename)
        chunks = []
        for pageno, page in enumerate(infile_chunks, start=1):
            iv = self.get_iv(cmac_key, pageno)
            decipher = python_Twofish.new(xts_key, mode=python_Twofish.MODE_XTS)
            chunks.append(decipher.encrypt(page, iv))
        self.write_file_chunks(outfilename, chunks)
        _log.info('Done!')


if __name__ == '__main__':
    if len(sys.argv) != 5 \
            or sys.argv[1] not in ('encrypt', 'decrypt') \
            or sys.argv[2] not in STFDecrypt.MASTER_KEYS.keys():
        print("Usage: {} <action> <keyname> <infile> <outfile>".format(sys.argv[0]))
        print("\taction can be one of 'encrypt' or 'decrypt'.")
        print("\tkeyname can be one of 'core', 'data', 'game' or 'map'.")
        print("\texample: {} decrypt game game_6.db game_6_decrypted.db".format(sys.argv[0]))
        sys.exit(1)

    logging.basicConfig(level=logging.INFO)

    stf = STFDecrypt()
    if sys.argv[1] == 'decrypt':
        stf.decrypt(sys.argv[2], sys.argv[3], sys.argv[4])
    elif sys.argv[1] == 'encrypt':
        stf.encrypt(sys.argv[2], sys.argv[3], sys.argv[4])
