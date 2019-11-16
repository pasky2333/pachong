#!/usr/bin/env python
# -*- coding:utf-8 -*-
from proxypool.scheduler import Schedualer
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s = Schedualer()
        s.run()
    except:
        main()


if __name__ == '__main__':
    main()