# PaSiMap (Pairwise Similarity Map)

## Purpose
The aim of the tool PaSiMap is to map protein sequences as coordinates based on their pairwise similarities.

In order to determine the pairwise similarities, PaSiMap first computes global alignments for each pair of sequences.
The similarity of each aligned pair of sequences is then quantified as a number in order to allow the mapping with the multidimensional scaling method [*cc_analysis*](https://pubmed.ncbi.nlm.nih.gov/28375141/)

For more details please refer to [PaSiMap paper](https://doi.org/10.1016/j.csbj.2022.09.034).

## How to get started

### PaSiMap webserver
The easiest way to use PaSiMap is with our [PaSiMap webserver](http://pasimap.biologie.uni-konstanz.de).

Simply submit your query to the webserver and download your results.
You can also try out PaSiMap with the example query provided on the webserver.

### Local PaSiMap on Linux

#### Setting up

1. Get PaSiMap from GitHub:
   ```
   git clone https://github.com/ksu00/pasimap.git
   ```
   This results in the directory named `pasimap`.

   :warning: All the following steps will be done from within this `pasimap` directory.

2. Set up directory structure:
   ```
   # In pasimap directory.
   mkdir src/webserver
   mkdir src/webserver/static
   mkdir src/webserver/static/tmp
   ```
   The directory for each job (contains query, interim results and final results) will have to be located in this `tmp` directory.

3. Set up Python Virtual Environment:

   :warning: Make sure that the correct Python version (Python 3) is active, PaSiMap was developed with Python 3.6.12.

   Install Python package for Virtual Environments:
   ```
   pip install virtualenv --user
   ```

   Create new Virtual Environment for PaSiMap:
   ```
   # In pasimap directory.
   python -m venv venv
   ```

   Activate Virtual Environment for PaSiMap:
   ```
   # In pasimap directory.
   source venv/bin/activate
   ```

   Install packages required by PaSiMap:
   ```
   # In pasimap directory.
   pip install -r requirements.txt
   ```

4. Set up needleall (EMBOSS).

   Download and configure EMBOSS software suite (version 6.6.0) from [EMBOSS](https://emboss.sourceforge.net/download/).

   Add `needleall` to `PATH` **OR** adjust to your `needleall` path in the following line in `run_pipeline.sh` (in `pasimap` directory):
   ```
   time needleall -asequence $in_file_path \
   ```

   Adjust location of substitution matrix to your path in the following line in `run_pipeline.sh` (in `pasimap` directory):
   ```
   substmat_dir_path=/usr/local/EMBOSS-6.6.0/emboss/data;
   ```

5. Set up *cc_analysis*:

   Download [binary of *cc_analysis*](https://wiki.uni-konstanz.de/pub/cc_analysis).

   Add *cc_analysis* to to `PATH` **OR** adjust to your *cc_analysis* path in the following line in `run_pipeline.sh` (in `pasimap` directory):

   ```
   time cc_analysis -dim $dim \
   ```

#### Running job

1. Create job directory (e.g. `ASDF`, but you can name it whatever you want):
   ```
   # In pasimap directory.
   mkdir src/webserver/static/tmp/ASDF
   ```

2. Prepare query:
   ```
   # In pasimap directory.
   mkdir src/webserver/static/tmp/ASDF/0_input
   touch src/webserver/static/tmp/ASDF/0_input/dim.txt
   touch src/webserver/static/tmp/ASDF/0_input/state.txt
   touch src/webserver/static/tmp/ASDF/0_input/input.txt
   touch src/webserver/static/tmp/ASDF/0_input/count.txt
   ```

   - Specify dimensionality for output in `dim.txt`, e.g.:
     ```
     echo 3 > src/webserver/static/tmp/ASDF/0_input/dim.txt
     ```

   - Specify mode for PaSiMap in `state.txt`, e.g.:
     ```
     echo unaligned > src/webserver/static/tmp/ASDF/0_input/state.txt
     ```
     The possible options are `unaligned` for unaligned protein sequences (in FASTA-format), `aligned` for MSA of protein sequences (in FASTA-format) and `quantifier` for pairwise similarities.

   - Specify query in `input.txt` according to `state.txt`, e.g. unaligned protein sequences ( in FASTA-format) for `unaligned`.

     Please refer to [Help page of PaSiMap webserver](http://pasimap.biologie.uni-konstanz.de/help) for details.

   - Specify number of datapoints (e.g. sequences) of query in `count.txt`.
     For sequences, you can take advantage of the syntax of FASTA-format:
     ```
     grep -c '>' src/webserver/static/tmp/ASDF/0_input/input.txt > src/webserver/static/tmp/ASDF/0_input/count.txt
     ```

3. Activate Virtual Environment for PaSiMap, if not already active:
   ```
   # In pasimap directory.
   source venv/bin/activate
   ```

4. Run job:
   ```
   # In pasimap directory.
   ./run_pipeline.sh ASDF
   ```
