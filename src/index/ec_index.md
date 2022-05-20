# ec index

```bash
ec index [options] ec-file
```

convert the markers txt file to number form

## Options

`-g`, `--groups`

The name of the groups file

`-t`, `--targets`

The name of the targets file

`-e`, `--ec`

The name of the ec matrix file

## Examples

```bash
$ ec index -g groups.txt -t targets.txt -e markers.ec markers.txt
# convert from text to number representation
```
