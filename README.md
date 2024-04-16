# ec

`ec` is a tool for manipulating marker gene "equivalence class" files. This file is text based and has the following format

- Lines preceded with a "#" are comments
- Subsequent lines contain two columns (separated by a tab)
- The first column is the cell type
- The second column is a comma separated list of genes

Here is an example:

```
# homo_sapiens
CT1	GA,GB
CT2	GB,GC
CT3	GA,GD
```

## Installation

The development version can be installed with

```bash
pip install git+https://github.com/sbooeshaghi/ec
```

## Usage

`ec` consists of five subcommands:

```bash
usage: ec [-h] [--verbose] <CMD> ...

ec 0.0.1: handle ec files

positional arguments:
  <CMD>
    index     Index markers.txt file into groups, targets, and ec matrix files
    mark      Created markers.txt from deg.txt file
    merge     Merge two markers.txt files (union or intersection)
    verify    Check whether the provided groups, targets, ec matrix and markers.txt files are correct and compatible with each other
    filter    Filter out bad genes from markers.txt file

optional arguments:
  -h, --help  show this help message and exit
  --verbose   Print debugging information
```

### `ec index`: index markers.txt into groups, targets, and ec matrix

`ec index` assigns a number to each cell type and a number to each gene and creates three files: 1. groups.txt (one line for each cell type, the line number is the assigned cell type number), 2. targets.txt (one line for each gene, the line number is the assigned gene number), and 3. markers.ec (the same structure as the markers.txt but each cell type and marker gene is replaced with its corresponding number.).

```bash
ec index [-h] -g GROUPS -t TARGETS -e EC markers.txt
```

- `-g GROUPS`: path to save the groups file (single column)
- `-t TARGETS`: path to save the targes file (single column)
- `-e EC`: path to save the markers.ec
- `markers.txt`: the markers.txt file

#### Examples

```bash
$ cat markers.txt
CT1	GA,GB
CT2	GB,GC
CT3	GA,GD

$ ec index -t targets.txt -g groups.txt -e ec.txt markers.txt

$ cat targets.txt
GA
GB
GC
GD

$ cat  groups.txt
CT1
CT2
CT3

$ cat ec.txt
0	0,1
1	1,2
2	0,3
```

### `ec mark`: create a markers.txt from `mx diff` output file

```bash
ec mark [-h] -p MP -f MFC -g GS -m MPCT -o OUTPUT degs.txt
```

- `-p MP`: Minimum corrected p-value
- `-f MFC`: Minimum log2 fold-change
- `-g GS`: Maximum number of genes shared
- `-m MPCT`: Maximum number of genes per cell type
- `-o OUTPUT`: Output path
- `markers.txt`

#### Examples

### `ec merge`: Merge two markers.txt files (union or intersection)

```bash
ec merge [-h] -o OUTPUT -m {intersection,union} markers.txt_1 markers.txt_2
```

- `-o OUTPUT`: Path to output merged markers.txt file
- `-m {intersection,union}`: Method used to merge
- `markers.txt_1` the first set of markers
- `markers.txt_2` the second set of markers

#### Examples

```bash
$ cat markers.txt_1
CT1	GA,GB
CT2	GB,GC
CT3	GA,GD

$ cat markers.txt_2
CT1	GA,GB
CT2	GB,GC
CT3	GA
CT4	GA,GE

$ ec merge -o markers_union.txt -m union markers.txt_1 markers.txt_2

$ cat markers_union.txt
CT3	GD,GA
CT1	GA,GB
CT2	GC,GB
CT4	GE,GA
```

### `ec verify`: Verify that ec files are compatible with each other

```bash
ec verify [-h] -g GROUPS -t TARGETS -e EC markers.txt
```

- `-g GROUPS`: Path to groups file to verify
- `-t TARGETS`: Path to targets file to verify
- `-e EC`: Path to ec matrix to verify
- `markers.txt`

#### Examples

```bash
# using the same files generated with ec index
$ ec verify -g groups.txt -t targets.txt -e ec.txt markers.txt
Files are correct
```

### `ec filter`: filter out bad genes from markers.txt

```bash
ec filter [-h] -bt BAD_TARGETS -o OUTPUT markers.txt
```

- `-bt BAD_TARGETS`: Path to bad targets file
- `-o OUTPUT`: Path to output filtered markers.txt file
- `markers.txt`

#### Examples

```bash
$ cat markers.txt
CT1	GA,GB
CT2	GB,GC
CT3	GA,GD

$ cat bad_markers.txt
GA

$ ec filter -bt bad_markers.txt -o markers_clean.txt markers.txt

$ cat markers_clean.txt
CT1	GB
CT2	GB,GC
CT3	GD
```
