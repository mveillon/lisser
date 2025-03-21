# Lisser

Lisser is a Python CLI app that takes the transaction data you provide and analyzes it. There are a number of built-in graphs and aggregations that it performs, and there is also support for configuring those calculations and adding more, specific to the user. 

# Installation

This repository has only been tested with Python 3.12.7. Support for other versions is limited but on the roadmap. It is assumed you have [Python 3](https://www.python.org/downloads/) installed.

First, clone the repository to your machine. `> git clone https://github.com/mveillon/lisser.git`

It is recommended, but not required, to setup a virtual environment using something like Pyenv. 

To install the needed dependencies and setup the folder structure, navigate to the `lisser` directory and run the following command: `> pip3 install -r requirements.txt && python3 main.py init`.

If you have `make` installed, you can also run `make init` instead.

This will install all dependent libraries and create template files for you to populate. If you run this command more than once, it will prompt you before overwriting any files in case you've added any data. This can be disabled by adding the `-F` or `--force` flag to the python3 command.

You can also set up the spreadsheets for a previous year using the `-y {year}` or `--year={year}` option. See **CLI Usage**.

# Running the Code

## Command Cheatsheet

Here are some commonly used commands:

| command         | alias                             | description                                             |
| --------------- | --------------------------------- | ------------------------------------------------------- |
| make cli        | python main.py cli                | runs the command line for the year of the system time   |
|                 | python main.py cli -y 2024        | runs the command line for the 2024 data                 |
|                 | python main.py cli -f '{path}'    | runs the command line for the data at path              |
| make ui         | python main.py ui                 | launches the TKinter UI                                 |

And for developers:

| command         | alias                             | description                                             |
| --------------- | --------------------------------- | ------------------------------------------------------- |
| make fmt        | black src tests main.py           | formats the Python code                                 |
| make lint       | flake8 src tests main.py          | lints the Python code                                   |
| make test       | pytest                            | runs all the tests                                      |
| make types      | mypy src                          | type checks the Python code                             |

## Input

The input spreadsheet can be an Excel sheet (.xlsx), a Numbers file (.numbers), a .csv file, or a .txt file formatted like a .csv. It should have a row for every transaction in which the user spent money that year.

The year does not have to complete, but the year of every transaction should be the same (i.e. it should start no sooner than January 1st and end no later than December 31st the same year).

Note that income does not belong in this spreadsheet.

The spreadsheet needs, at minimum, the following columns:

- `Date`: the date of the transaction
- `Category`: the general category of the transaction, e.g. "Groceries", or "Bills"
- `Price`: how much was spent. Should always be positive
- `Is Food`: whether the transaction was spent on food. Either zero (no) or one (yes)
- `Controllable`: whether you had a reasonable amount of control over the transaction or how much it was. Either zero (no) or one (yes)

Additionally, the default spreadsheets also have columns for `Description`, a brief description of what was bought, and `Vendor`, to whom the money went. These categories are not used by the code by default, but they can be accessed by any plots or aggregations in `config_overwrite.yml` as string columns.

Although not needed by the machine, these columns are highly recommended for the human creating or reviewing the data. Certain plots can also use them for additional information if present.

## Output

After running the code at least once, there will be two sets of outputs saved to `data/{year}/`. If ran through the GUI, this will all also be served to the user as a `.zip` file.

The main output are the graphs in the `plots/` directory. These are divided into graphs aggregated weekly and separated into monthly chunks, as well as graphs that analyze the whole year of data. Each monthly graph organizes its plots into folders with the name of the month e.g. `January`, `February`. The yearly graphs are all found in `plots/Combined`.

There are also aggregations done on the full year of data. These are found at `aggregation.csv`.

## CLI Usage

Once installation is complete, you run the code with the following commands: `> python3 main.py cli`. 

Or if you have `make` installed, you can also run `> make cli`.

This will analyze one year of data. By default, this will be the year of the current local time, but this can be changed with the `-y {year}` or `--year={year}` option.

Using this year, it will search for a spreadsheet at `data/{year}/Spending.{csv|txt|numbers|xlsx}`. This can be changed by passing the path to the spreadsheet using the `-f` or `--file` argument.

If `--file` is passed, the `--year` flag will be ignored, as the year will be inferred from the spreadsheet.

## Running the GUI

There is also a neat little GUI just to make the file navigation a little easier. Simply run `python3 main.py ui`, or `make ui` and it will launch a window.

By default, the UI will read and write from `data/{year}/Spending.{csv|txt|numbers|xlsx}`, but this can be changed with the `Change path` button. Once the desired spreadsheet is selected, click `Start analysis` to generate the output report.

You can also add transactions one at a time by filling out the fields and clicking `Submit`. Editing and deleting existing expenses are not currently supported.

# Files

The only files that the user will interact with are `base_config.yml / config_overwrite.yml` and all the files in the `data` directory. These files should be arranged like this. 

```bash
├── data
│   ├── ...
│   ├── 2024
│       ├── plots
│           ├── January                         # plots for the month of January
│           ├── February                        # plots for the month of February
│           ├── ...
│           ├── Combined                        # plots for the whole year
│       ├── aggregation.csv                     # generated aggregations
│       ├── Spending.{csv|xlsx|txt|numbers}     # spending for the whole year
│   ├── 2025
│       ├── ...
│   ├── ...
├── base_config.yml                             # default configurations
├── config_overwrite.yml                        # user-defined configuration overwrites
```

## Configuration

There are a number of built-in plots and aggregations that can be found in the `base_config.yml` file. The user is free to edit these however they please. They also serve as an example. 

Additional plots and aggregations can be added to the `config_overwrite.yml` file. If a key in the `config_overwrite.yml` file is also present in `base_config.yml`, the value from `config_overwrite.yml` will be used.

This is useful because there may be changes to the code that you want to download with `git pull`. If you've changed anything in `base_config.yml` directly, there will likely be conflicts and it may be hard to resolve them.

## Globals

There are a few global variables that can be configured under the `globals` key.

- `YEARLY_TAKE_HOME_PAY`: how much take-home pay you had for each year you have spending data. **Must Be Overwritten** or the code will not run.
- `SANKEY_OTHER_THRESHOLD`: the proportion of the yearly income that the spending in a category has to exceed to not be put in the "Other" category in `sankeyflow.png`.
- `PROJECTED_SPENDING_BILL_THRESHOLD`: at what price threshold bills are filtered out from weekly samples and averaged out over the whole month. See **Projected Spending**.
- `PROJECTED_SPENDING_LARGE_EXPENSE_THRESHOLD`: at what price threshold all transactions are filtered out from certain yearly graphs and smoothed out. See **Projected Spending**.

Because the user has to set `globals.YEARLY_TAKE_HOME_PAY` for the code to work properly, and it is the only such config, many users will want to just change that one variable in `base_config.yml` and not worry about `config_overwrite.yml` since the base settings work pretty well out of the box.

For that reason, we will never change the `base_config.yml` in such a way that will cause merge conflicts to that variable, meaning you are free to set it directly in `base_config.yml`.

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

The allowed values for `func` are any of the methods of a [Pandas Series](https://pandas.pydata.org/docs/reference/api/pandas.Series.html), but only those that don't take an argument will work. Common values are `sum`, `any`, `all`, and `mean`.

The value of the `column` parameter will be the column selected from the data for aggregation. It will almost always be `Price`.

In addition `func` can equal `count`, at which point the `column` key is not needed and will not be used.

The key for each aggregation in `config_overwrite.yml` ∪ `base_config.yml` will be converted to a row in `data/{year}/aggregation.csv`.

# Other Notes

## What is projected spending?

One of the most useful features of this repo is normalizing spending using what I call "projection".

Many people have rent or other bills due on the first of the month, and there are various other reasons why spending might consistently and predictably spike at certain points each month. 

Projected spending takes all rows where the Category is "Bills" and they're over a small threshold (set to `PROJECTED_SPENDING_BILL_THRESHOLD` in the `config` files), and smooths out those expenses over the course of the entire month. 

This effectively lowers the total amount spent that week, and raises that of the other weeks.

It then takes the weekly spending and prorates it over a month, since the "weekly" spending value has bills from the full month.

This concept of smoothing outliers is also applied to all transactions _other than_ bills for certain graphs. For these graphs, all non-bill transactions over the `PROJECTED_SPENDING_LARGE_EXPENSE_THRESHOLD` threshold defined in the `config` files will be removed.

The large expenses threshold is applied to all monthly graphs. In this case, the transaction totals are not smoothed and added back in.

The code also uses the large expenses threshold for yearly graphs that are grouped by week instead of month. This is to say that a full year of data would produce a graph with 52 dots instead of 12. With a smaller sample size per point, the data points would seem much more extreme. In this case, the total price of the outliers is smoothed out evenly over the whole graph and added back in.

## Can I turn projected spending off?

**YES!**

If this whole smoothing-things-out thing isn't for you, you can disable it in the configs.

If you want to disable filtering and smoothing large bills, set the `PROJECTED_SPENDING_BILL_THRESHOLD` global variable to zero.

Similarly, to disable the large transaction filtering, set the `PROJECTED_SPENDING_LARGE_EXPENSE_THRESHOLD` global variable to zero.

These variables are independent and don't interact with each other. You can disable one, the other, or both.
