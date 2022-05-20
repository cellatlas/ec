# ec index

```bash
ec index [options] markers.txt
```

convert the markers txt file to number form

## Options

`-g`, `--groups`

Path of the output groups file

`-t`, `--targets`

Path of the output targets file

`-e`, `--ec`

Path of the output ec matrix file

## Examples

```bash
$ ec index -g groups.txt -t targets.txt -e markers.ec markers.txt
# convert from text to number representation
```
