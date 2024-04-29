import numpy as np

movies_lines=np.random.choice(3883, 100, replace=False)

_id=0
f=open("ml-1m/original_dataset/movies.dat", "r", encoding = "ISO-8859-1")
g=open("ml-1m/original_dataset/subsampled_movies.dat", "w+", encoding = "ISO-8859-1")

import re

_surrogates = re.compile(r"[\uDC80-\uDCFF]")

def detect_decoding_errors_line(l, _s=_surrogates.finditer):
    """Return decoding errors in a line of text

    Works with text lines decoded with the surrogateescape
    error handler.

    Returns a list of (pos, byte) tuples

    """
    # DC80 - DCFF encode bad bytes 80-FF
    return [(m.start(), bytes([ord(m.group()) - 0xDC00]))
            for m in _s(l)]


for line in f:
  try: 
    errors = detect_decoding_errors_line(line)
    if errors:
      print(line)
      continue
    if _id in movies_lines:
      g.write(line)
      print(line)
    _id+=1
  except Exception as e:
    continue

f.close()
g.close()