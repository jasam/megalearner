args = ['/home/jasam/repositories/megalearner/tests/gotham/Gotham - 1x01.srt', '/home/jasam/repositories/megalearner/tests/gotham/']

import pysrt
file_name = args[0]


subs = pysrt.open(file_name)
for item in subs:
    print(item.text.replace('-', ''))
print('finished')