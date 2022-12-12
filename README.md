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
