# Pandas ET

A tool for simple Extract/Transform job for csv/excel files using pandas. The main purpose is describing an ET process in a json/yaml file and apply it without additional coding. Parameters are generally following those in pandas methods.

## Use

```python
from pandas_et import Schema, process_file

# Read schema description from json/yaml file to schema_dict, then parse:
schema = Schema.model_validate(schema_dict)
# Apply schema to input file:
df = process_file(filename, schema)
```

## Read

Common parameters:
- `columns` list of column names, regex pattern or None for all columns
- `filename_column` add filename to dataframe

### csv
- `type=csv`
- `sep` separator

CSV is read with string dtype.

### excel
- `type=excel`
- `sheets` number of sheet, list of sheetnames, regex patter or None for all sheets
- `sheetname_column` add sheetname to dataframe

## Transforms
- `extract` extract value from column with regex
- `rename` rename columns
- `convert` convert data types
- `drop_na`
- `fill_na`
- `query` apply query/filtering to dataframe
- `reindex`
- `sort` optionally with natsort 
- `concat` concat values of several columns to a new column
- `normalize_whitespaces` strip and replace all whitespaces with a single space
