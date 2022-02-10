# ec fromtext

```bash
ec fromtext [options] ec-file
```

convert the .ec file in text form to number form

## Options

`-g`, `--groups`

The name of the groups file

`-e`, `--elements`

The name of the elements file

`-o`, `--output`

The name of the ec file (number form)

## Examples

```bash
$ ec fromtext -g groups.txt -e elements.txt -o matrix.ec markers.txt
# convert from text to number representation
```
