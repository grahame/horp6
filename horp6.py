#!/usr/bin/env python3

from lxml import etree
etree.set_default_parser(etree.HTMLParser())
import os
import subprocess
import requests
from urllib.parse import urljoin
from io import BytesIO

tmpdir = './tmp/'
index_uri = 'http://www.aph.gov.au/About_Parliament/House_of_Representatives/Powers_practice_and_procedure/Practice6'
chunk_size = 4096

def main():
    data = requests.get(index_uri).content
    et = etree.parse(BytesIO(data))
    pdfs = []
    for idx, elem in enumerate(et.xpath('//a[contains(@href, ".pdf")]')):
        pdf = os.path.join(tmpdir, '%d.pdf' % idx)
        pdfs.append(pdf)
        tmpf = pdf + '_tmp'
        if os.access(pdf, os.R_OK):
            print("skipping %d, already down..." % (idx))
            continue
        req = requests.get(urljoin(index_uri, elem.get('href')), stream=True)
        with open(tmpf, 'wb') as fd:
            for data in req.iter_content(chunk_size):
                fd.write(data)
            os.rename(tmpf, pdf)
    cmd = [ 'pdftk' ] + pdfs + ['cat', 'output', 'horp6.pdf']
    print(cmd)
    subprocess.call(cmd)

if __name__ == '__main__':
    main()


