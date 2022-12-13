# UCL_IFRC_IXN_PUBLIC

## Usage

### Setting up the environment

```bash
conda env create -f conda_environment.yml
conda activate UCL_IFRC_IXN
```

### Download databases in CSV format

```bash
cd DesInventar
python get_csv_databases.py
```

### Clean databases

```bash
python data_cleaner.py
```

### Ignore existing files and download spreadsheets/caches from DesInventar
Modify the 5th line of `get_csv_databases.py` to:
```
    csv_crawler.run(mode)
```
`mode` is an integer from 0 to 7, whose highest bit determines whether ignore
existing spreadsheets and last two bits determine the level of ignoring of
caches.

Let `ignore_cache = mode & 0b011`  
If `ignore_cache` is greater than 0, the crawler will ignore cache in 
`caches/disasters.pkl`. If `ignore_cache` is greater than 1, the crawler will 
ignore cache in `caches/disasters.pkl` and `caches/disasters/*`. 
If `ignore_cache` is greater than 2, all caches will be ignored.
