# ec merge

```bash
ec merge [options] markers.txt_1 markers.txt_2
```

Merge two markers.txt files.


## Options

`-m`, `--method`

The method to apply. One of: intersect, union

`-o`, `--output`

Path for the output merged markers.txt file

## Examples

```bash
$ ec merge -m union -o merged.txt markers_1.txt markers_2.txt
# Merge markers_1.txt and markers_2.txt (union)
```
