# Mmap for Node.js

mmap(2) / madvise(2) / msync(2) / mincore(2) for Node.js.

**NOTE**: this is a fork of https://github.com/ozra/mmap-io as that repo is
unmaintained.

`mmap`-ing is by nature potentially blocking, and _should not be used in
concurrent serving/processing applications_, but rather has it's niche where
multiple processes are working on the same giant sets of data (thereby sparing
physical memory, and load times if the kernel does it's job for read ahead),
preferably multiple readers and single or none concurrent writer, to not spoil
the gains by loads of spin-locks, mutexes or such.

# News and Updates

### 2021-11-29: version 2.0.0

- basic cleanups over docs/code.
- fixed bug where `mmap` wouldn't work with lengths or offsets greater than
  2GB; this was due to some bad type-casting.

### 2019-07-09/B: version 1.1.3, ..., 1.1.6

- rewritten the C++-code to catch up with V8/Nan breaking changes for node.js
  `12.*`, which also removes all warnings in earlier versions.
- refactored in to wrapper functions for extracting values, so should new
  breaking changes come in later versions, it will be quicker to adjust.
- major "package.json" mistakes. Unless running build manually, the js-files
  where never packaged, nor built. Now whitelisted in package.json.
- major mistake 2: when they finally where packaged, they we're killed off when
  the C++ module was rebuilt on installment. So. Finally: js-files are now
  built to "dist", and the binary into "build". This way the TypeScript and
  LiveScript aren't required for end user

### 2019-07-09/A: version 1.1.1

- when replacing GNU Make, for some reason I used `yarn` in "package.json" —
  which may have failed builds for those not having it installed (and then not
  building "es-release"), and completely missing the point of getting rid of
  Make.
- updated README to reflect new build command (`npm run build`) (_should only
  ever be needed if you clone from git and contribute_)
- added back the "main" entry in package.json. Hell of a blunder! Tests changed
  to import from root so they fail without it.
- the never before tested example code here in the README, has been ran and
  corrected, thanks to @LiamKarlMitchell

### 2019-03-08: version 1.1.0

- rewrote the es part of the _lib_ code from LiveScript to TypeScript. The
  prudent thing to do in a lib. The test remains in LS.
- `offs_t` changed to `size_t` because of bitwidth goofyness. Thanks to @bmarkiv
- removed dependency on GNU Make by adding build commands to "package.json".
  Might help those on windows platform who didn't have it installed. However
  they still rely on a horde of "common posix utils", so your setup might be
  lacking anyway then.
- note that there are some compile warnings because of changes in C++ API's in
  NAN/V8, ignored for now in contemplation whether to switch to node-addon-api
  (napi for C++), since call overhead isn't an issue in this library,
  everything considered.

### 2018-01-16: version 1.0.0

- bumped the version to 1.0.0 since, well, why not.
- changed deprecated calls from `ForceSet` to `DefineOwnProperty`
- general source noise cleanups
- fixed compilation errors for newer nodejs. Thanks to @djulien
- windows-specific problems (#5, #6), and more, fixed. Thanks to @bkmartinjr
- updated README clarifying _Contribution Guidelines_

### 2017-03-08: version 0.11.1

- compilation fixes 10.8 OSX fix. Thanks to @arrayjam

### 2016-07-21: version 0.10.1

- `incore` fix for Mac OS. Thanks to @rustyconover

### 2016-07-14: version 0.10.0

- `incore` added. Thanks to @rustyconover

### 2015-10-10: version 0.9.4

- Compilation on Mac should work now. Thanks to @aeickhoff

### 2015-10-01: version 0.9.3

- Windows compatibility added. Thanks to @toxicwolf
- Rewrote the bindings to Nan 2.0.9 API version (V8/io/Node hell...)
    - Had to remove the error _codes_ to get it working in the time I had
      available (or rather - didn't have..) —
      error messages are still there — with code in message instead. Though,
      usually nothing goes wrong, so only the test cares ;-)
- Added some helpful targets in Makefile `human_errors`, `ls` only, `build`
  only, etc. (useful if you wanna hack the module)
- Since all _functionality_ that can possibly be is in place, I bumped all the
  way to 0.8. Not battle tested enough to warrant higher.
- Commented away experimental async read-ahead caching when readahead hint was
  on. It hasn't broken, but it's an unnecessary risk. Plays safe. You can toy
  with it yourself if you want to try to milk out some _ms_ performance.

### 2015-03-04: version 0.1.3

- This is the first public commit, and the code has one day of development put
  into it as of now. More tests are needed so don't count on it being
  production ready just yet (but soon).

# Install

Use npm or git.

```bash
$ npm install mmap-io
```

```bash
$ git clone https://github.com/ipinfo/mmap-io.git
$ cd mmap-io
$ npm build
```

# Usage

**Note: All code in examples are in LiveScript**

```livescript
# Following code is plastic fruit; not t[ae]sted...

mmap = require "mmap-io"
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

### Misc

- Checkout man pages mmap(2), madvise(2), msync(2), mincore(2) for more
  detailed intell.
- The mappings are automatically unmapped when the buffer is garbage collected.
- Write-mappings need the fd to be opened with "r+", or you'll get a permission
  error (13).
- If you make a read-only mapping and then ignorantly set a value in the
  buffer, all hell previously unknown to a JS'er breaks loose (segmentation
  fault). It is possible to write some devilous code to intercept the SIGSEGV
  and throw an exception, but let's not do that!
- `Offset`, and in some cases `length` needs to be a multiple of
  mmap-io.PAGESIZE (which commonly is 4096)
- Huge pages are only supported for anonymous / private mappings (well, in
  Linux), so I didn't throw in flags for that since I found no use.
- As Ben Noordhuis previously has stated: Supplying hint for a fixed virtual
  memory adress is kinda moot point in JS, so not supported.

# Tests

```bash
$ npm test
```
