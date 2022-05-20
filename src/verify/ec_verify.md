
# ec verify

```bash
ec verify [options] 
```

Check whether the provided groups, elements, ec matrix and markers.txt files are correct and compatible with each other. Specifically, the function tests whether:
* The individual elements, groups and ec matrix files are correct.
* The elements, groups and ec matrix files are compatible with each other
* The markers.txt file is compatible with the elements, groups and ec matrix files.




## Options

`-g`, `--groups`

The name of the groups file

`-e`, `--elements`

The name of the elements file

`-m`, `--matrixec`

Tha name of the ec matrix file

`-t`, `--txtmarkers`
The name of the markers txt file 
## Examples

```bash
$ ec verify -g groups.txt -e elements.txt -m matrix.ec -t markers.txt
```
