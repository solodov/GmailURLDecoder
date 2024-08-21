import base64
import unittest

from doctools.GmailURLDecoder import GmailURLDecoder


def decode(encoded_thread_id):
    input_charset = "BCDFGHJKLMNPQRSTVWXZbcdfghjklmnpqrstvwxz"
    input_charset_size = len(input_charset)
    output_charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    output_charset_size = len(output_charset)
    decoded_char_ords = []
    for encoded_char in encoded_thread_id:
        offset = 0
        for i, decoded_char_ord in enumerate(decoded_char_ords):
            decoded_char_ord = input_charset_size * decoded_char_ord + offset
            if decoded_char_ord >= output_charset_size:
                rest = decoded_char_ord % output_charset_size
                offset = (decoded_char_ord - rest) // output_charset_size
                decoded_char_ord = rest
            else:
                offset = 0
            decoded_char_ords[i] = decoded_char_ord
        while offset:
            rest = offset % output_charset_size
            decoded_char_ords.append(rest)
            offset = (offset - rest) // output_charset_size
        offset = input_charset.index(encoded_char)
        i = 0
        while offset:
            if i >= len(decoded_char_ords):
                decoded_char_ords.append(0)
            decoded_char_ord = decoded_char_ords[i] + offset
            if decoded_char_ord >= output_charset_size:
                rest = decoded_char_ord % output_charset_size
                offset = (decoded_char_ord - rest) // output_charset_size
                decoded_char_ord = rest
            else:
                offset = 0
            decoded_char_ords[i] = decoded_char_ord
            i += 1
    transformed_thread_id = "".join(output_charset[c] for c in reversed(decoded_char_ords))
    padding = '=' * (-len(transformed_thread_id) % 4)
    return "thread-" + base64.b64decode(transformed_thread_id + padding).decode("utf-8")


URLS = """\
http://mail#all/FMfcgxwGCHDmQQHgmFDLhbgGxprwJchL
http://mail#all/FMfcgxwHNVxDmBMvbZfjJFWQhtLXZcXq
http://mail#all/FMfcgxwHNqJFjDzPjMjvWTkbjbqHdVCW
http://mail#all/FMfcgxwJWXSssxwSdggTPWHLHlmbgBjr
http://mail#all/FMfcgxwJWXcxfJCFMSmVldjRwqPMWdNw
http://mail#all/FMfcgxwLsKBxCNcstgXdjpmlqktxBQzj
http://mail#all/FMfcgxwLsdFDFvWxPtSKZKtpmKrngTsz
http://mail#all/FMfcgxwLsmlrCKmKQXBCnmhWrjZZWxGg
http://mail#all/FMfcgxwLtGnvmDKZkxRLTBNbZcMtnLSL
http://mail#all/FMfcgxwLtZmWrPtpZznHKSQvQDccSlzg
http://mail#all/FMfcgxwLtZsLLQgjjwGsMLJdZmZsfHJC
http://mail#all/FMfcgxwLtkVTzfTVZHzzSpMQPsXngwJM
http://mail#all/FMfcgzGkXSTfLRQDdlBJmPZtRdsVLVSD
http://mail#all/FMfcgzGkXSdjKKtGXMfbgqWVHGzmVNNw
http://mail#all/FMfcgzGkZGnTzpkJskqcVwxLcSfgcmJF
http://mail#all/FMfcgzGkZZssHcsLqvzjSMwKJsmfxJvV
http://mail#all/FMfcgzGlkFqXQQmzCFDmCWzkHPxGBzdJ
http://mail#all/FMfcgzGlkFwJhzwFGPdGPkdDxrLJVLzg
http://mail#all/FMfcgzGlkjjMzQpkDrWsWPDtWVjWQWxF
http://mail#all/FMfcgzGllMFZxmMjXgdmRRqxdkgCDLSJ
http://mail#all/KtbxLrjjBDrXSXMZmjzqvGVWrNsHfKmRCL
http://mail#all/KtbxLthVctVThzMxqNdlRzTZLMFpPxKbDq
http://mail#all/KtbxLwGzfNHGwvwXZkxNNdGrLmfbmKsQmL
http://mail#all/KtbxLxgGCTvvbqNZxWfcjgFpzmvsSMMMHg
http://mail#all/KtbxLzGSvTzscrTTSMLxTpzkhKbXGHSZGB
http://mail#all/QgrcJHrnzwQSJFbGMmftGDWbrBGXrxZKrlq
http://mail#all/QgrcJHsBtQfvWqvcxRXlHQVdbxQwkJCZNCq
http://mail#all/QgrcJHsHrSRCfvHnRFhzszwNJTVWtBCnZRl
http://mail#all/QgrcJHsHrSwLnMgnxcvJcSpJDTTdnwjLzJl
http://mail#all/QgrcJHsbgZlJnHfRnxMDHZcqKZgNPCJbVGq
http://mail#all/QgrcJHsbkfNNQTFSNfSgXGMHgWrqxNMrFhq
http://mail#all/QgrcJHshZXxvBGtzfvGfcZvwHSMBJrvbZRl
"""


class GmailURLDecoderTest(unittest.TestCase):
    def setUp(self):
        self.mail_urls = filter(None, URLS.split())

    def test(self):
        for url in self.mail_urls:
            _, encoded_thread_id = url.rsplit("/", 1)
            self.assertEqual(GmailURLDecoder.decode(encoded_thread_id),
                             decode(encoded_thread_id), f"decoding {url}")


if __name__ == '__main__':
    for url in filter(None, URLS.split()):
        _, encoded_thread_id = url.rsplit("/", 1)
        print(
            f'assert_eq!("{decode(encoded_thread_id)}", decode_thread_id("{encoded_thread_id}"));')
