# ec operate

```bash
ec operate [options] ec-file
```

operate on multiple ec files.

note to self: should the .ec file be normally in text or number form? something to decide

## Options

`-m`, `--method`

The method to apply. One of: intersect, setdiff, leftjoin, rightjoin, union

`-g`, `--groups`

Comma delimited list of groups

`-e`, `--elements`

Comma delimited list of elements

`-o`, `--output`

The name of the ec file (number form)

## Examples

```bash
$ ec operate -g groups.txt -e elements.txt -o matrix.ec markers.txt
# convert from text to number representation
```
