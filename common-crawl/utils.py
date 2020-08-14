from warc import WARCHeader

def reset_warc_header(header: WARCHeader):
    if "Content-Length" in header:
        del header["Content-Length"]
    if "WARC-Payload-Digest" in header:
        del header["WARC-Payload-Digest"]
    if "WARC-Block-Digest" in header:
        del header["WARC-Block-Digest"]
    return header