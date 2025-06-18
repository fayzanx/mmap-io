
# mmap-io - Node.js memory mapping bindings

## Note
- This is a fork of [ARyaskov/mmap-io](https://github.com/ARyaskov/mmap-io) -> [ozra/mmap-io](https://github.com/ozra/mmap-io) and [ipinfo/mmap-utils](https://github.com/ipinfo/mmap-utils)

This fork fixes a couple of things
- Ability to be used with >= Node v22
- Ability to handle large files being loaded into the map

## Quick info

- Long story short: with this addon you can increase performance of your file interactions by memory mapping files, 
you are "project" some file to RAM and push data to RAM without any interactions with hdd/ssd subsystem -- this module will
facilitate reliable syncing between RAM-file and disk-file.
- **mmap-io** is written in C++17 and TypeScript, when you're installing it in your project, you're automatically getting 
a precompiled binary (.node-file) for your platform from Downloads section of this project. 
Otherwise it requires a C++17 compiler and Python 3.12+ on your machine to build.
- **mmap-io** is tested on Node.js 16 (16.14+), 18, 19, 20, 21, 22. Sorry, but there is no Node.js 17 because of some compilation stage issues.
- **mmap-io** has built binaries for Windows x86_64, Linux x86_64, Mac x86_64, Mac ARM.
- Potential use cases: working with big files (like highly volatile game map files), pushing data to cache files, video/audio-processing, messaging mechanics for inter-process communication.

## Quick TS example

```typescript
    import fs from "fs"
    import mmap from "@fayzanx/mmap-io"
    
    const file = fs.openSync("/home/ubuntu/some-file-here", "r+")
    const buf = mmap.map(fs.fstatSync(file).size, mmap.PROT_WRITE, mmap.MAP_SHARED, file)
    mmap.advise(buf, mmap.MADV_RANDOM)
    // Now you can work with "buf" as with a regular Buffer object.
    // All your changes will be synced with the file "some-file-here" on disk.
    // For example, add number 1024 at 0 position of buffer:
    // buf.writeUInt32LE(1024, 0)

```

# Author's notice: 
## Mmap for Node.js
Please refer for man pages for mmap(2) / madvise(2) / msync(2) / mincore(2).


# Installation

## npm

This is my first node.js addon and after hours wasted reading up on V8 API I luckily stumbled upon [Native Abstractions for Node](https://github.com/rvagg/nan). Makes life so much easier. Hot tip!

_mmap-io_ is written in C++11 and ~~[LiveScript](https://github.com/gkz/LiveScript)~~ — _although I love LS, it's more prudent to use TypeScript for a library, so I've rewritten that code._

It should be noted that mem-mapping is by nature potentially blocking, and _should not be used in concurrent serving/processing applications_, but rather has it's niche where multiple processes are working on the same giant sets of data (thereby sparing physical memory, and load times if the kernel does it's job for read ahead), preferably multiple readers and single or none concurrent writer, to not spoil the gains by shitloads of spin-locks, mutexes or such. _And your noble specific use case of course._


# News and Updates

### 2024-05-12: version 1.4.3
- Add support for Node 22

# Install
Use npm or yarn or git.

```bash
$ npm install @fayzanx/mmap-io
```
```bash
$ yarn add @fayzanx/mmap-io
```

```bash
$ git clone https://github.com/fayzanx/mmap-io.git
$ cd mmap-io
$ yarn build
$ yarn install
```

### Good to Know (TM)

- Checkout man pages mmap(2), madvise(2), msync(2), mincore(2) for more detailed intell.
- The mappings are automatically unmapped when the buffer is garbage collected.
- Write-mappings need the fd to be opened with "r+", or you'll get a permission error (13).
- If you make a read-only mapping and then ignorantly set a value in the buffer, all hell previously unknown to a JS'er breaks loose (segmentation fault). It is possible to write some devilous code to intercept the SIGSEGV and throw an exception, but let's not do that!
- `Offset`, and in some cases `length` needs to be a multiple of mmap-io.PAGESIZE (which commonly is 4096)
- Huge pages are only supported for anonymous / private mappings (well, in Linux), so I didn't throw in flags for that since I found no use.
- As Ben Noordhuis previously has stated: Supplying hint for a fixed virtual memory adress is kinda moot point in JS, so not supported.
- If you miss a feature - contribute! Or request it in an issue.
- If documentation isn't clear, make an issue.


# Tests

```bash
$ yarn test
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
