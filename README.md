# argus_hash
Excludes Argus header/footer information and hashes content. Header/Footer are both 128 bytes. Script checks input is a argus binary, then hashes excluding header/footer.

## Bash Alternative
```bash
$ > tail -c +129 file.argus | head -c -128 | md5sum
```

## Usage

```bash
./argus_hash.py file.argus

# multiple files
./argus_hash.py *.argus
```

## Help
```console
$ > ./argus_hash.py -h
usage: argus_hash.py [-h] input [input ...]

Excludes Argus header/footer information and hashes content.

positional arguments:
  input       Input filename(s).
```
