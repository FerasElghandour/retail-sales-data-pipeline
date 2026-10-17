# Reproduction and benchmark scope

The reusable pipeline now rejects missing schemas, all-null numerics, invalid dates, missing GPU values and invalid hardware denominators. The retained1,000-row generated input preserves all rows, adds six derived fields and leaves no missing numeric values.

## Execute a recorded profile

```sh
python run_reproduction.py --profile checks --output reproduced/checks
```

Use a new output directory for each run. The driver writes command logs, source/input SHA-256 values, versions and an explicit outcome. It does not silently download data or turn generated fixtures into dataset-performance claims.

| Profile | Actual scope | Required inputs |
|---|---|---|
| `checks` | Offline behavioral regressions; not a fresh dataset benchmark | None |
| `full-notebook` | Execute retained notebook against an explicitly supplied input; preserves the original experiment protocol | csv |
| `pipeline` | Validated CSV transformation; input provenance determines real versus generated scope | csv |

Supply named paths with `--input name=/absolute/path`. Exact commands are versioned in [reproduction.json](reproduction.json); direct training commands and preparation contracts are below.

## Evidence boundary

The retained transaction table is generated. Its revenue totals do not describe a real retailer.

Keep input acquisition and source credits in [DATA.md](DATA.md). Historical results, new reference runs and small contract fixtures have separate evidential scope.

## Recorded command definitions

### checks

```text
{python} smoke_test.py
{python} test_pipeline.py
```

### full-notebook

```text
{python} reproduce.py --input {input:csv} --output {output}/notebook
```

### pipeline

```text
{python} pipeline.py {input:csv} --output {output}/pipeline
```

`{python}` is the current interpreter. `{output}` is the new run directory. `{input:name}` refers to a named absolute input path supplied to the driver. Install declared dependencies in a clean environment before executing. Never execute untrusted serialized models or notebooks.
