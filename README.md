# csv2json

Convert csv files to json.

### Usage

```
Usage: python csv2json.py -c <csvFile> <jsonFile> [options]

Required arguments:
    -c, --convert <csvFilePath> <jsonFilePath>  Converts csv file to json file

Options:
    -h, --help                  Display help
    -i, --indent <value>        Define indent in output file (default value is 4)
    --rows [rowIndices]         Select specific rows to be included in output json
    --xrows [rowIndices]        Exclude specific rows from output json
    --head                      Save first 5 csv rows
    --tail                      Save last 5 csv rows
    --columns [columnNames]     Select specific columns to be included in output json
    --xcolumns [columnNames]    Exclude specific columns from output json
```

### Examples

```
input.csv:

Id;Name;Age;Country;Job
0;John;67;USA;Retired
1;Betty;44;UK;Teacher
2;Frank;27;USA;Engineer
3;Mark;32;USA;Unemployed
4;Anna;21;Poland;Student
5;Tom;53;USA;Nurse
6;William;41;UK;Chef
7;Alice;51;UK;Doctor
8;Mario;24;Italy;Plumber
9;Natalie;19;Canada;Salesperson
```

#### Basic conversion:

```
python csv2json.py -c input.csv output.json

output.json:

[
    {
        "Id":0,
        "Name":"John",
        "Age":67,
        "Country":"USA",
        "Job":"Retired"
    },
    {
        "Id":1,
        "Name":"Betty",
        "Age":44,
        "Country":"UK",
        "Job":"Teacher"
    },
    {
        "Id":2,
        "Name":"Frank",
        "Age":27,
        "Country":"USA",
        "Job":"Engineer"
    },
    {
        "Id":3,
        "Name":"Mark",
        "Age":32,
        "Country":"USA",
        "Job":"Unemployed"
    },
    {
        "Id":4,
        "Name":"Anna",
        "Age":21,
        "Country":"Poland",
        "Job":"Student"
    },
    {
        "Id":5,
        "Name":"Tom",
        "Age":53,
        "Country":"USA",
        "Job":"Nurse"
    },
    {
        "Id":6,
        "Name":"William",
        "Age":41,
        "Country":"UK",
        "Job":"Chef"
    },
    {
        "Id":7,
        "Name":"Alice",
        "Age":51,
        "Country":"UK",
        "Job":"Doctor"
    },
    {
        "Id":8,
        "Name":"Mario",
        "Age":24,
        "Country":"Italy",
        "Job":"Plumber"
    },
    {
        "Id":9,
        "Name":"Natalie",
        "Age":19,
        "Country":"Canada",
        "Job":"Salesperson"
    }
]
```

#### Select rows 2-5 and 9 and columns "Id", "Name" and "Country":

```
python csv2json.py -c input.csv output.json --rows 2-5 9 --columns Id Name Country

output.json:

[
    {
        "Id":2,
        "Name":"Frank",
        "Country":"USA"
    },
    {
        "Id":3,
        "Name":"Mark",
        "Country":"USA"
    },
    {
        "Id":4,
        "Name":"Anna",
        "Country":"Poland"
    },
    {
        "Id":5,
        "Name":"Tom",
        "Country":"USA"
    },
    {
        "Id":9,
        "Name":"Natalie",
        "Country":"Canada"
    }
]
```

#### Selecting 5 first rows excluding columns Name and Age:

```
python csv2json.py -c input.csv output.json --head --xcolumns Name Age

output.json:

[
    {
        "Id":0,
        "Country":"USA",
        "Job":"Retired"
    },
    {
        "Id":1,
        "Country":"UK",
        "Job":"Teacher"
    },
    {
        "Id":2,
        "Country":"USA",
        "Job":"Engineer"
    },
    {
        "Id":3,
        "Country":"USA",
        "Job":"Unemployed"
    },
    {
        "Id":4,
        "Country":"Poland",
        "Job":"Student"
    }
]
```

#### Exclude rows 2-9 and use indent=2:

```
python csv2json.py -c input.csv output.json --xrows 2-9 -i 2

output.json:

[
  {
    "Id":0,
    "Name":"John",
    "Age":67,
    "Country":"USA",
    "Job":"Retired"
  },
  {
    "Id":1,
    "Name":"Betty",
    "Age":44,
    "Country":"UK",
    "Job":"Teacher"
  }
]

```

### Test

```
python -m unittest
```
