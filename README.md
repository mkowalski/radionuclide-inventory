# radionuclide-inventory

## Branch `master`

```python2 main.py```

The script is supposed to read a set of rules and values from the `Andra FMA` and with the help of `scanner` store them in a list of dictionaries where each element represents one parsed line from the results. `scanner` also implements support for missing values in case the measurement is missing some data like limit or declaration.

`FMA` performs a simple analysis over the parsed data against nuclides provided as the inventory. In the sample code three selected nuclides are analysed instead of reading them from the real data.

## Branch `statistics`

```python2 main.py```

The script is supposed to read a set of results from `Results/Aluminium_6060` directory and generate an analysis as `Results/Aluminium_6060_RA/RadionuclideInventory_RA_new.csv`. All the results are grouped so one row represents one nuclide with all the data. In case of missing measurements, the row corresponding to the affected nuclide will contain less results.
