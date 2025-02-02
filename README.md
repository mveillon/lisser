# Spending Tracking

This is a Python CLI app that takes the transaction data you provide and analyzes it. There are a number of built-in graphs and aggregations that it performs, and there is also support for configuring those calculations and adding more, specific to the user. 

# Installation

This repository has only been tested with Python 3.12.7. Support for other versions is limited but on the roadmap. It is assumed you have [Python 3](https://www.python.org/downloads/) installed.

First, clone the repository to your machine. `> git clone https://github.com/mveillon/spending-tracking.git`

It is recommended, but not required, to setup a virtual environment using something like Pyenv. 

To install the needed dependencies and setup the folder structure, navigate to the `spending-tracking` directory and run the following command: `> pip3 install -r requirements.txt && python3 initialize.py`.

If you have `make` installed, you can also run `make init` instead.

This will install all dependent libraries and create template files for you to populate. If you run this command more than once, it will prompt you before overwriting any files in case you've added any data. This can be disabled by adding the `-f` or `--force` flag to the python3 command.

You can also set up the spreadsheets for a previous year using the `-y {year}` or `--year={year}` option.

# Usage

Once installation is complete, you run the code with the following commands: `> python3 main.py`

Or if you have `make` installed, you can also run `> make run`.

This will analyze one year of data. By default, this will be the year of the current local time, but this can be changed with the `-y {year}` or `--year={year}` option.

*Note the `main.py` file also has a `-f` option because it uses the same function as the `initialize.py` file, but this flag does nothing here.*

# Files

The only files that the user will interact with are `base_config.yml / config_overwrite.yml` and all the files in the `data` directory. These files should be arranged like this. 

```bash
├── data
│   ├── ...
│   ├── 2024
│       ├── plots
│           ├── January                     # plots for the month of January
│           ├── February                    # plots for the month of February
│           ├── ...
│           ├── Combined                    # plots for the whole year
│       ├── aggregation.yml                 # generated aggregations
│       ├── Spending.\{csv\|xlsx\|txt\}     # spending for the whole year
│   ├── 2025
│       ├── ...
│   ├── ...
├── base_config.yml                         # default configurations
├── config_overwrite.yml                    # user-defined configuration overwrites
```

## Input

The `data/{year}/Spending` spreadsheet can be an Excel sheet (.xlsx), a Numbers file (.numbers), a .csv file, or a .txt file formatted like a .csv. It should have a row for every transaction in which the user spent money that year.

Note that income does not belong in these spreadsheets, and the numbers in the `Price` column should always be positive. Furthermore, the values in `Is Food` and `Controllable` should either be zero (no) or one (yes).


## Output

After running the `main.py` file once, there will be two sets of outputs. 

The main output are the graphs in `data/{year}/plots`. These are divided into graphs aggregated weekly and separated into monthly chunks, as well as graphs that analyze the whole year of data. Each monthly graph organizes its plots into folders with the name of the month e.g. `January`, `February`. The yearly graphs are all found in `data/{year}/plots/Combined`.

There are also aggregations done on the full year of data. These are found at `data/{year}/aggregation.yml`.


# Configuration

There are a number of built-in plots and aggregations that can be found in the `base_config.yml` file. The user is free to edit these however they please. They also serve as an example. 

Additional plots and aggregations can be added to the `config_overwrite.yml` file. If a key in the `config_overwrite.yml` file is also present in `base_config.yml`, the value from `config_overwrite.yml` will be used.

This is useful because if there are ever changes to the code and you want to download them, if you've changed anything in `base_config.yml` directly, there will be conflicts and it may be hard to resolve them.


## Globals

There are a few global variables that can be configured under the `globals` key.

- `YEARLY_TAKE_HOME_PAY`: how much take-home pay you had for each year you have spending data.
- `SANKEY_OTHER_THRESHOLD`: the proportion of the yearly income that the spending in a category has to exceed to not be put in the "Other" category.
- `PROJECTED_SPENDING_BILL_THRESHOLD`: at what price threshold bills are filtered out from weekly samples at averaged out over the whole month.
- `PROJECTED_SPENDING_LARGE_EXPENSE_THRESHOLD`: at what price threshold transactions are filtered out from certain graphs and smoothed out. See __Projected Spending__.

## Plots

The `plots` key maps to a dictionary where each key maps to a single plot. Each plot will be a line plot with any number of lines.

Each line will be the sum of the `Price` column over either each month (if `timeframe = monthly`) or each year (if `timeframe = yearly`), with any numbers of filters applied to the data over any of the columns.

Each filter listed will be combined using `AND` operators, forming a conjunction. For both plots and aggregations, a `disjunction` key can be provided at the same level as the filters. If the value is `True`, the filters will be combined using the `OR` operator instead.

There is currently no support for combining the `AND` and `OR` operators in a single line/aggregation.

If there are multiple lines in a plot, it is recommended to provide the optional `style` and `label` parameters to each line. If the label is not present on any of the lines, it will not be in the legend, which will only be present if at least one line has a label.

For information on the `style` parameter, see the **Notes** section of [this page](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html).

There is also an optional `agg` paramater, which is a list of aggregations, each having the same format as the ones in the **Aggregations** section. Each aggregation will be its own line. For the aggregations to have different styles, labels, etc., the aggregations can be split across multiple lines.

## Aggregations

The structure is similar to the `plots` dictionary. Each aggregation will summarize the whole year, with any number of filters applied. These filters have the same rules as those in `plots`.

The allowed values for `func` are any of the methods of a [Pandas Series](https://pandas.pydata.org/docs/reference/api/pandas.Series.html), but only those that don't take an argument will work. Common values are `sum`, `any`, `all`, and `mean`. In addition `func` can equal `count`, at which point the `column` key is not needed and will not be used.

The value of the `column` parameter will be the column selected from the data for aggregation. If the `divide` key is provided and set to True, the resulting total will be grouped weekly, monthly, and yearly.

The key for each aggregation in `config_overwrite.yml` ∪ `base_config.yml` will be converted to a title and be a key in `data/{year}/aggregation.yml`.

# Other Notes

## What is projected spending?

One of the most useful features of this repo is normalizing spending using what I call "projection".

Many people have rent or other bills due on the first of the month, and there are various other reasons why spending might consistently and predictably spike at certain points each month. Projected spending takes all rows where the Category is "Bills" and they're over a small threshold, and smooths out those expenses over the course of the entire month. This effectively lowers the total amount spent that week, and raises that of the other weeks.

It then takes the weekly spending and prorates it over a month, since the "weekly" spending value has bills from the full month.

This concept of smoothing outliers is also applied to certain graphs. For these graphs, all transactions over the threshold defined in the `config` files will be removed.

This happens for all monthly graphs, and the transaction totals are not smoothed and added back in.

This only happens for yearly graphs that are grouped by week instead of month. This is to say that a full year of data would produce a graph with 52 dots instead of 12. With a smaller sample size, the data points would seem much more extreme. In this case, the total price of the outliers is smoothed out evenly over the whole graph and added back in.

## Can I turn projected spending off?

__YES!__

If this whole smoothing-things-out thing isn't for you, you can disable it in the configs.

If you want to disable filtering and smoothing large bills, set the `PROJECTED_SPENDING_BILL_THRESHOLD` global variable to zero.

Similarly, to disable the large transaction filtering, set the `PROJECTED_SPENDING_LARGE_EXPENSE_THRESHOLD` global variable to zero.

These variables are independent and don't interact with each other. You can disable one, the other, or both.
