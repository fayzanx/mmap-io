# mmap utilities for nodejs

`mmap(2)` / `madvise(2)` / `msync(2)` / `mincore(2)` for nodejs.

**NOTE**: this is a fork of https://github.com/ozra/mmap-io as that repo is
unmaintained.

# Installation

## npm

```bash
$ npm install mmap-utils
```

## git

```bash
$ git clone https://github.com/ipinfo/mmap-utils.git
$ cd mmap-utils
$ npm install
$ npm build
```

# Usage

**Note: All code in examples are in LiveScript**

```livescript
# Following code is plastic fruit; not t[ae]sted...

mmap = require "mmap-utils"
fs = require "fs"

some-file = "./foo.bar"

fd = fs.open-sync some-file, "r"
fd-w = fs.open-sync some-file, "r+"

# In the following comments:
# - `[blah]` denotes optional argument
# - `foo = x` denotes default value for argument

size = fs.fstat-sync(fd).size
rx-prot = mmap.PROT_READ .|. mmap.PROT_EXECUTE
priv = mmap.MAP_SHARED

# map( size, protection, privacy, fd [, offset = 0 [, advise = 0]] ) -> Buffer
buffer = mmap.map size, rx-prot, priv, fd
buffer2 = mmap.map size, mmap.PROT_READ, priv, fd, 0, mmap.MADV_SEQUENTIAL
w-buffer = mmap.map size, mmap.PROT_WRITE, priv, fd-w

# advise( buffer, advise ) -> void
# advise( buffer, offset, length, advise ) -> void
mmap.advise w-buffer, mmap.MADV_RANDOM

# sync( buffer ) -> void
# sync( buffer, offset, length ) -> void
# sync( buffer, is-blocking-sync[, do-page-invalidation = false] ) -> void
# sync( buffer, offset = 0, length = buffer.length [, is-blocking-sync = false [, do-page-invalidation = false]] ) -> void

mmap.sync w-buffer
mmap.sync w-buffer, true
mmap.sync w-buffer, 0, size
mmap.sync w-buffer, 0, size, true
mmap.sync w-buffer, 0, size, true, false

# incore( buffer ) -> [ unmapped-pages Int, mapped-pages Int ]
core-stats = mmap.incore buffer
```

# Tests

```bash
$ npm run test
```

### Misc

- Checkout man pages `mmap(2)`, `madvise(2)`, `msync(2)`, `mincore(2)` for more
  detailed intel.
- The mappings are automatically unmapped when the buffer is garbage collected.
- Write-mappings need the fd to be opened with "r+", or you'll get a permission
  error (13).
- If you make a read-only mapping and then ignorantly set a value in the
  buffer, all hell previously unknown to a JS'er breaks loose (segmentation
  fault). It is possible to write some devilous code to intercept the SIGSEGV
  and throw an exception, but let's not do that!
- `Offset`, and in some cases `length` needs to be a multiple of `PAGESIZE`
  (which commonly is 4096)
- Huge pages are only supported for anonymous / private mappings (well, in
  Linux), so I didn't throw in flags for that since I found no use.
- As Ben Noordhuis previously has stated: Supplying hint for a fixed virtual
  memory adress is kinda moot point in JS, so not supported.
