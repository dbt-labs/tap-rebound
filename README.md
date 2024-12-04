# ***Archival Notice***
This repository has been archived.

As a result all of its historical issues and PRs have been closed.

Please *do not clone* this repo without understanding the risk in doing so:
- It may have unaddressed security vulnerabilities
- It may have unaddressed bugs

<details>
   <summary>Click for historical readme</summary>

# tap-rebound

Author: Drew Banin (drew@fishtownanalytics.com)

This is a [Singer](http://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

It:
- Generates a catalog of available data in Rebound
- Extracts the following resources:
  - [returns](https://intelligentreturns.net/api/#returns_get)
  - [tracking](https://intelligentreturns.net/api/#tracking_get)

### Quick Start

1. Install

```bash
git clone git@github.com:fishtown-analytics/tap-rebound.git
cd tap-rebound
pip install .
```

2. Get an API token and username from the Rebound application

3. Create the config file.

Copy the `config.json.example` file to `config.json` and update the configs based on the credentials you obtained in Step 2.

4. Run the application to generate a catalog.

```bash
tap-rebound -c config.json --discover > catalog.json
```

5. Select the tables you'd like to replicate

Step 4 generates a a file called `catalog.json` that specifies all the available endpoints and fields. You'll need to open the file and select the ones you'd like to replicate. See the [Singer guide on Catalog Format](https://github.com/singer-io/getting-started/blob/c3de2a10e10164689ddd6f24fee7289184682c1f/BEST_PRACTICES.md#catalog-format) for more information on how tables are selected.

6. Run it!

```bash
tap-rebound -c config.json --catalog catalog.json
```

Copyright &amp;copy; 2019 Fishtown Analytics

