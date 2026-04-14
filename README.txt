Gram is a simple and efficient data encoding/decoding tool for the command line.
It supports multiple encoding formats and works with both stdin and direct string input.


Usage: gram <encoder> [options]

Options:
  -h             Show help
  -v             Show version
  -d             Decode input
  -b             Append trailing newline to output
  -o file        Write output to a file
  -f option      Set encoder-specific options (key=value or flag)
  -s string      Encode a string directly instead of reading stdin
  -e encoding    Set text encoding (default: utf-8)

Available encoders:
  a85       Ascii85
  b32       Base32
  b64       Base64               -f lbreak=[mime|pem]
  bin       Binary String        -f sep=N
  hex       Hexadecimal String   -f sep=N  -f upper
  html      HTML Escape          -f full
  puny      Punycode IDN
  quopri    Quoted-printable     -f full
  unicode   Unicode Escape       -f format=[short|long|point]  -f lower
  url       URL Encoding         -f plus  -f full

> Use 'gram list' to list all encoders from the terminal.

Examples:

  Encode a string to Base64:
    $ echo "hello" | gram b64 -b
    aGVsbG8K

  Decode Base64 back:
    $ echo "aGVsbG8K" | gram b64 -d
    hello

  Hexadecimal with separator and uppercase:
    $ gram hex -f sep=2 -f upper -bs "Hello"
    48 65 6C 6C 6F

  Unicode codepoints:
    $ gram unicode -f format=point -bs "hello"
    U+0068 U+0065 U+006C U+006C U+006F

  Decode unicode codepoints:
    $ gram unicode -f format=point -dbs "U+0068 U+0065 U+006C U+006C U+006F"
    hello

  Full URL encoding:
    $ gram url -f full -bs "hello world"
    %68%65%6c%6c%6f%20%77%6f%72%6c%64

Author: Ryan R <pwnfo@proton.me>
