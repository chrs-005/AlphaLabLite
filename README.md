# AlphaLabLite

A small time-series transformation engine that can:

- execute a script made of time-series transformations
- save the computed variables
- view saved variables later by execution id
- expose the same core logic through both a CLI and a REST API

## Project Shape

The code is split by responsibility:

- `parser.py` parses the script text into program lines
- `executor.py` runs the program line by line
- `transformations.py` contains the transformation logic
- `storage.py` saves and loads variables with SQLite
- `app.py` shares the main execute/view flow
- `cli.py` is the command-line interface
- `rest.py` is the REST interface

## Supported Transformations

- `Fetch`
- `SimpleMovingAverage`
- `ExponentialMovingAverage`
- `RateOfChange`
- `CrossAbove`
- `ConstantSeries`
- `PortfolioSimulation`

## CLI

Run from the project folder.

Execute a script:

```powershell
python cli.py execute
```

Then paste a script like:

```txt
price = Fetch{OneMinuteGoldPrices}{}
fast = ExponentialMovingAverage{0.3}{price}
slow = SimpleMovingAverage{20}{price}
entry = CrossAbove{}{fast, slow}
exit = CrossAbove{}{slow, fast}
result = PortfolioSimulation{10000}{entry, exit, price}
```

Finish input with `Ctrl+Z`, then press Enter.

View saved variables:

```powershell
python cli.py view --id YOUR_ID price result
```

## REST

Start the server:

```powershell
python rest.py
```

It runs on:

```txt
http://127.0.0.1:8000
```

### Execute

`POST /execute`

Example body:

```json
{
  "script": "price = Fetch{OneMinuteGoldPrices}{}\nfast = ExponentialMovingAverage{0.3}{price}"
}
```

### View

`GET /view/<execution_id>?items=price&items=fast`

## Persistence

Saved variables are stored in a local SQLite database:

```txt
alphalablite.db
```
