{
    "targets": [{
        "target_name": "mmap-utils",
        "sources": [ "src/mmap-utils.cc" ],
        "include_dirs": [
            "<!(node -e \"require('nan')\")"
        ],
        "cflags_cc": [
            "-std=c++17"
        ]
    }]
}
