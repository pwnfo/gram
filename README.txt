NAME
       gram - simple and efficient data encoding/decoding utility

SYNOPSIS
       gram <encoder> [options]

DESCRIPTION
       Gram encodes and decodes data in various formats. Input can be
       provided via stdin or the -s string option.

OPTIONS
       -h           show help
       -v           show version
       -d           decode input
       -b           append trailing newline
       -o file      write output to file
       -f option    extra encoder-specific options
       -s string    encode string directly
       -e encoding  set text encoding (default: utf-8)

ENCODERS
       a85        ASCII85
       b32        Base32
       b64        Base64           [ -f lbreak=[mime|pem] ]
       bin        Binary String    [ -f sep=N ]
       hex        Hexadecimal      [ -f sep=N -f upper ]
       html       HTML Escape
       puny       Punycode IDN
       quopri     Quoted-printable
       unicode    Unicode Escape   [ -f format=[short|long|point] -f lower ]
       url        URL Encoding     [ -f plus ]

EXAMPLES
       echo "hello" | gram b64 -b
           # Output: aGVsbG8K

       echo "aGVsbG8K" | gram b64 -d
           # Output: hello

       gram unicode -f format=point -s "hello"
           # Output: U+0068 U+0065 U+006C U+006C U+006F

       gram unicode -f format=point -ds "U+0068 U+0065 U+006C U+006C U+006F"
           # Output: hello

AUTHOR
       Ryan R <pwnfo@proton.me>
