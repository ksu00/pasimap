#!/bin/bash

# Abort script when any command fails.
set -e;

# =====================================================================|======|
# Parse arguments.

job_id=$1;

# =====================================================================|======|
# Preparations for this job.

# FB.
echo '/====================================================================\';
echo "Start pipeline.";
echo "----------------------------------------------------------------------";

# Directory that is running the pipeline.
run_dir_path=`pwd`;

# Directory dedicated to this job.
job_dir_path=${run_dir_path}/src/webserver/static/tmp/${job_id};

# Starting data.
start_dir_path=${job_dir_path}/0_input;
start_mainfile_name=input.txt;
start_dimfile_name=dim.txt;
start_statefile_name=state.txt;
start_countfile_name=count.txt;

# File for signalling the status of this job.
signal_file_name=signal.txt;

# File for warnings.
# (Will only exist, if there are warnings.)
warning_file_name=warning.txt;

# Paths.
start_mainfile_path=${start_dir_path}/${start_mainfile_name};
start_dimfile_path=${start_dir_path}/${start_dimfile_name};
start_statefile_path=${start_dir_path}/${start_statefile_name};
start_countfile_path=${start_dir_path}/${start_countfile_name};
signal_file_path=${job_dir_path}/${signal_file_name};
warning_file_path=${job_dir_path}/${warning_file_name};

# Create symlink.
ln -s $start_mainfile_path ${job_dir_path}/${job_id}_input.txt;

# Get data for this job.
dim=`cat $start_dimfile_path`;
state=`cat $start_statefile_path`;
count=`cat $start_countfile_path`;

# Preparation for potential error messages.
if [ $state == 'unaligned' ];
then
    object_type='sequence';
elif [ $state == 'aligned' ];
then
    object_type='sequence';
elif [ $state == 'quantifier' ];
then
    object_type='object';
fi;

# FB.
echo "job_id: $job_id";
echo "   dim: $dim";
echo " state: $state";
echo " count: $count";
echo '\--------------------------------------------------------------------/';

# =====================================================================|======|
# Create secure copy of input sequences.

# If the starting data contains sequences.
if [ $state == 'unaligned' ] || [ $state == 'aligned' ];
then

    # FB.
    echo '/====================================================================\';
    echo "FASTA -> secureFASTA.";
    echo "----------------------------------------------------------------------";

    # Input.
    in_dir_path=$start_dir_path;
    in_file_name=$start_mainfile_name;

    # Output.
    out_dir_path=${job_dir_path}/1_input_secure;
    out_result_file_name=input_secure.fas;
    out_result_spaceless_file_name=input_secure_spaceless.fas;
    out_alias_file_name=alias.csv;

    # Paths.
    in_file_path=${in_dir_path}/${in_file_name};
    out_result_file_path=${out_dir_path}/${out_result_file_name};
    out_result_spaceless_file_path=${out_dir_path}/${out_result_spaceless_file_name};
    out_alias_file_path=${out_dir_path}/${out_alias_file_name};

    # Create output-directory.
    mkdir $out_dir_path;

    # Run program.
    # (Conserve space-characters in this step,
    #  because I need them for mapping the aliases of the FASTA-headers.)
    python -m src.pipeline.FASTA_to_secureFASTA \
           $in_file_path \
           --wrap \
           --verbose \
           > $out_result_file_path;

    # FB.
    echo "----------------------------------------------------------------------";
    echo "-> created secure FASTA-file.";

    # Replace space-characters (only exist in FASTA-headers).
    #
    # Reasoning:
    # If there are several adjacent spaces,
    # 'needle' will replace it with a single space.
    sed 's/ /_/g' $out_result_file_path > $out_result_spaceless_file_path;

    # FB.
    echo "-> created secure FASTA-file (without spaces).";

    # Map aliases of the FASTA-headers.
    # Alias: 1st word of the secure FASTA-header (separated by space).
    # (Will be needed for the labelled plots at the end of the pipeline.)
    paste -d ',' \
          <(grep '^>' $out_result_spaceless_file_path | sed 's/^>//') \
          <(grep '^>' $out_result_file_path | sed 's/^>//' | awk '{print $1}') \
          > $out_alias_file_path;

    # FB.
    echo "-> created aliases for labels.";

    # -----------------------------------------------------------------|------|
    # Check redundacy of FASTA-headers/-bodies.

    # FB.
    echo "----------------------------------------------------------------------";
    echo "Check redundancy of FASTA-headers/-bodies.";

    # Working directory.
    work_dir_path=${job_dir_path}/1_input_secure;

    # Input.
    in_file_name=input_secure_spaceless.fas;

    # Output.
    out_redundant_headers_file_name=input_secure_spaceless_redundant_headers.txt;
    out_redundant_bodies_file_name=input_secure_spaceless_redundant_bodies.txt;
    out_unique_headers_count_file_name=input_secure_spaceless_unique_headers_count.txt;
    out_unique_bodies_count_file_name=input_secure_spaceless_unique_bodies_count.txt;

    # Paths.
    in_file_path=${work_dir_path}/${in_file_name};
    out_redundant_headers_file_path=${work_dir_path}/${out_redundant_headers_file_name};
    out_redundant_bodies_file_path=${work_dir_path}/${out_redundant_bodies_file_name};
    out_unique_headers_count_file_path=${work_dir_path}/${out_unique_headers_count_file_name};
    out_unique_bodies_count_file_path=${work_dir_path}/${out_unique_bodies_count_file_name};

    # Run program.
    python -m src.pipeline.FASTA_to_stats \
           $in_file_path \
           $out_redundant_headers_file_path \
           $out_redundant_bodies_file_path \
           $out_unique_headers_count_file_path \
           $out_unique_bodies_count_file_path;

    # Get stats from output.
    unique_headers_count=`cat $out_unique_headers_count_file_path`;
    unique_bodies_count=`cat $out_unique_bodies_count_file_path`;

    # Get minimum number of unique FASTA-bodies for dim.
    unique_bodies_min=$(( $dim * 2 + 1));

    # Get maximum dim for number of unique FASTA-bodies.
    # (Integer division -> round down result to integer.)
    dim_max=$(( ($unique_bodies_count - 1) / 2 ))

    # FB.
    echo "";
    echo "stats:";
    echo "  unique_headers_count: $unique_headers_count";
    echo "  unique_bodies_count:  $unique_bodies_count";
    echo "check:";
    echo "  unique_bodies_min:    $unique_bodies_min";
    echo "  dim_max:              $dim_max";
    echo "";

    # Sanity check: fail.
    # If the number of unique FASTA-bodies is too low.
    if [ $unique_bodies_count -lt $unique_bodies_min ];
    then
        # Report to signal-file.
        printf "%s\n" \
               "There are not enough unique FASTA-bodies in your input for" \
               "your specified number of output dimensions <i>dim</i>." \
               "For <i>n</i> unique FASTA-bodies:" \
               "<i>dim</i> must not be higher than (<i>n</i>-1)/2." \
               "<hr>" \
               "There are two possible solutions to this problem:" \
               "<ol>" \
               "<li>" \
               "Increase your number of unique FASTA-bodies <i>n</i>" \
               "from the current value of '$unique_bodies_count'" \
               "to '$unique_bodies_min'." \
               "</li>" \
               "<li>" \
               "Decrease your output dimension <i>dim</i>" \
               "(expert-only option)" \
               "from the current value of '$dim'" \
               "to '$dim_max'." \
               "</li>" \
               "</ol>" \
               > $signal_file_path;
        # FB.
        echo "-> not enough unique FASTA-bodies (or dim is too high).";
        # Abort pipeline.
        exit 1;
    fi;

    # Sanity check: fail.
    # If there are redundant FASTA-headers.
    if [ -s $out_redundant_headers_file_path ];
    then
        # Report to signal-file.
        awk 'BEGIN {print "The FASTA-entries contain redundant headers.\n" \
                          "The special characters\n" \
                          "\x27<code>\:\|\,\/\\</code>\x27\n" \
                          "and <code style=\x27padding: 2px; border: 1px\n" \
                          "solid black;\x27>space</code>-characters\n" \
                          "are internally replaced with the character\n" \
                          "\x27<code>_</code>\x27.\n" \
                          "Please make sure that all headers are unique,\n" \
                          "even after this replacement.\n" \
                          "<hr>\n" \
                          "Redundant FASTA-headers with their frequencies:\n" \
                          "<ul>"} \
             {print "  <li><code>" $0 "</code></li>"} \
             END {print "</ul>"}' \
            $out_redundant_headers_file_path \
            > $signal_file_path;
        # FB.
        echo "-> There are redundant FASTA-headers.";
        # Abort pipeline.
        exit 1;
    fi;

    # Sanity check: fail (warning).
    # If there are redundant bodies.
    if [ -s $out_redundant_bodies_file_path ];
    then
        # Report to warning-file.
        awk 'BEGIN {print "The FASTA-entries contain redundant bodies.\n" \
                          "In general, all bodies should be unique in\n" \
                          "order to avoid a bias towards the more frequent\n" \
                          "sequences.\n" \
                          "If you are not absolutely certain that\n" \
                          "redundant bodies are sensible for your particular\n" \
                          "case, you should make sure that all bodies are\n" \
                          "unique and re-run your query.\n" \
                          "<hr>\n" \
                          "Headers of the redundant FASTA-bodies:\n" \
                          "<ul>"} \
             {print "  <li><code>" $0 "</code></li>"} \
             END {print "</ul>"}' \
            $out_redundant_bodies_file_path \
            > $warning_file_path;
        # FB.
        echo "-> There are redundant FASTA-bodies. (warning)";
    fi;

    # FB.
    echo '\--------------------------------------------------------------------/';

# If the starting data contains quantifiers.
elif [ $state == 'quantifier' ];
then

    # FB.
    echo '/====================================================================\';
    echo "Preparations.";
    echo "----------------------------------------------------------------------";

    # Output.
    out_dir_path=${job_dir_path}/1_input_secure;
    out_alias_file_name=alias.csv;

    # Path.
    out_alias_file_path=${out_dir_path}/${out_alias_file_name};

    # Create output-directory.
    mkdir $out_dir_path;

    # Create pseudo-alias-file.
    for n in $(seq $count);
    do
        echo "$n,$n" >> $out_alias_file_path;
    done;

    # FB.
    echo "-> created pseudo-aliases for pseudo-labels.";
    echo '\--------------------------------------------------------------------/';

fi;

# =====================================================================|======|
# Get pairwise alignments.

# If the starting data contains sequences.
if [ $state == 'unaligned' ] || [ $state == 'aligned' ];
then

    # FB.
    echo '/====================================================================\';
    echo "Get pairwise alignments:";

    # Input.
    in_dir_path=${job_dir_path}/1_input_secure;
    in_file_name=input_secure_spaceless.fas;

    # Output.
    out_dir_path=${job_dir_path}/2_alignment;
    out_result_file_name=alignments.fas;

    # Paths.
    in_file_path=${in_dir_path}/${in_file_name};
    out_result_file_path=${out_dir_path}/${out_result_file_name};

    # Create output-directory.
    mkdir $out_dir_path;

fi;

# If the starting data contains unaligned sequences.
if [ $state == 'unaligned' ];
then

    # -----------------------------------------------------------------|------|
    # needleall.

    # FB.
    echo "needleall.";
    echo "----------------------------------------------------------------------";

    # Additional output.
    out_log_file_name=log.txt;

    # Additional path.
    out_log_file_path=${out_dir_path}/${out_log_file_name};

    # Set parameters.
    gapopen_penalty=10.0;
    gapextend_penalty=0.5;
    apply_end_gap_penalties=True;
    minscore=1.0;

    # Run all-against-all Needleman-Wunsch with all fasta-entries in input_file.
    # -auto: turn off prompts.
    # -stdout: write to STDOUT.
    # -aformat3: format of output.
    time needleall -asequence $in_file_path \
                   -bsequence $in_file_path \
                   -gapopen $gapopen_penalty \
                   -gapextend $gapextend_penalty \
                   -endweight $apply_end_gap_penalties \
                   -endopen $gapopen_penalty \
                   -endextend $gapextend_penalty \
                   -minscore $minscore \
                   -auto \
                   -stdout \
                   -aformat3 fasta \
                   -errfile $out_log_file_path \
                   > $out_result_file_path;

    # FB.
    echo '\--------------------------------------------------------------------/';

elif [ $state == 'aligned' ];
then

    # -----------------------------------------------------------------|------|
    # Reformat MSA.

    # FB.
    echo "MSA -> pairwiseFASTA.";
    echo "----------------------------------------------------------------------";

    # Run program.
    python -m src.pipeline.MSA_to_pairwiseFASTA \
       $in_file_path \
       --verbose \
       > $out_result_file_path;

    # FB.
    echo '\--------------------------------------------------------------------/';

fi;

# =====================================================================|======|
# Reformat pairwise alignments.

# If the starting data contains sequences.
if [ $state == 'unaligned' ] || [ $state == 'aligned' ];
then

    # FB.
    echo '/====================================================================\';
    echo "pairwiseFASTA -> pairwiseCSV.";
    echo "----------------------------------------------------------------------";

    # Working directory.
    work_dir_path=${job_dir_path}/2_alignment;

    # Input.
    in_file_name=alignments.fas;

    # Output.
    out_file_name=alignments.csv;

    # Paths.
    in_file_path=${work_dir_path}/${in_file_name};
    out_file_path=${work_dir_path}/${out_file_name};

    # Run program.
    python -m src.pipeline.pairwiseFASTA_to_pairwiseCSV \
           $in_file_path \
           --verbose \
           > $out_file_path;

    # FB.
    echo '\--------------------------------------------------------------------/';

fi;

# =====================================================================|======|
# Determine connectivity.

# FB.
echo '/====================================================================\';
echo "Determine connectivity.";
echo "----------------------------------------------------------------------";

# Output.
out_dir_path=${job_dir_path}/3_connectivity;
out_file_name=connectivity.csv;
out_headed_file_name=connectivity+header.csv;

# Paths.
out_file_path=${out_dir_path}/${out_file_name};
out_headed_file_path=${out_dir_path}/${out_headed_file_name};

# Create output-directory.
mkdir $out_dir_path;

# If the starting data contains sequences:
# Determine connectivity of needleall-result.
if [ $state == 'unaligned' ] || [ $state == 'aligned' ];
then

    # Input.
    in_dir_path=${job_dir_path}/2_alignment;
    in_file_name=alignments.csv;

    # Paths.
    in_file_path=${in_dir_path}/${in_file_name};

    # Run program.
    python -m src.pipeline.pairwise_to_connectivity \
           $in_file_path \
           --separator ',' \
           --verbose \
           > $out_file_path;

# If the starting data contains quantifiers.
# Determine connectivity of starting data.
elif [ $state == 'quantifier' ];
then

    # Input.
    in_dir_path=$start_dir_path;
    in_file_name=$start_mainfile_name;

    # Paths.
    in_file_path=${in_dir_path}/${in_file_name};

    # Run program.
    python -m src.pipeline.pairwise_to_connectivity \
           $in_file_path \
           --verbose \
           > $out_file_path;

fi;

# Prepare header.
echo "label,number_of_connections" > $out_headed_file_path;
# Add body.
cat $out_file_path >> $out_headed_file_path;

# Create symlink.
ln -s $out_headed_file_path ${job_dir_path}/${job_id}_connectivity.csv;

# ---------------------------------------------------------------------|------|
# Check how many datapoints/sequences do NOT have enough connections.

# FB.
echo "----------------------------------------------------------------------";
echo "Check connectivity.";

# A datapoint/sequence does NOT have enought connections, when:
# number of connections >= dim.
loose_datapoints_num=$(awk -F ','       `# Parse csv-format.` \
                           -v DIM=$dim  `# Pass external variable to awk.` \
                           'BEGIN {c=0}           # Initialise counter. \
                            {if ($2<DIM) {c++}}   # Count loose datapoints. \
                            END {print c}         # Output counter.' \
                           $out_file_path);

# Sanity check: fail.
# If there are loose datapoints.
if [ $loose_datapoints_num != 0 ];
then
    # Report to signal-file.
    printf "%s\n" \
           "There are '$loose_datapoints_num' ${object_type}s, that do not" \
           "fulfil the condition: <i>connections</i> &ge; <i>dim</i>." \
           "Please remove these ${object_type}s from the input and try" \
           "again." \
           "The connectivity-file will help with identifying these" \
           "${object_type}s." \
           > $signal_file_path;
    # FB.
    echo "-> '$loose_datapoints_num' ${object_type}s do NOT fulfil condition: connections >= dim.";
    # Abort pipeline.
    exit 1;
fi;

# FB.
echo "-> all ${object_type}s fulfil condition: connections >= dim.";
echo '\--------------------------------------------------------------------/';

# =====================================================================|======|
# Calculate/get quantifier.

# If the starting data contains sequences.
if [ $state == 'unaligned' ] || [ $state == 'aligned' ];
then

    # FB.
    echo '/====================================================================\';
    echo "pairwiseCSV -> pairwiseQuantifier.";
    echo "----------------------------------------------------------------------";

    # Input.
    in_dir_path=${job_dir_path}/2_alignment;
    in_file_name=alignments.csv;

    # Output.
    out_dir_path=${job_dir_path}/4_quantifier;
    out_result_file_name=quantifier.ssv;
    out_map_file_name=info.csv;
    out_headed_map_file_name=info+header.csv;
    out_log_file_name=log.txt;
    out_result_map_file_name=quantifier+info.ssv;

    # Paths.
    in_file_path=${in_dir_path}/${in_file_name};
    out_result_file_path=${out_dir_path}/${out_result_file_name};
    out_map_file_path=${out_dir_path}/${out_map_file_name};
    out_headed_map_file_path=${out_dir_path}/${out_headed_map_file_name};
    out_log_file_path=${out_dir_path}/${out_log_file_name};
    out_result_map_file_path=${out_dir_path}/${out_result_map_file_name};

    # Create output-directory.
    mkdir $out_dir_path;

    # Set parameters.
    gapopen_penalty=10.0;
    gapextend_penalty=0.5;

    # Substitution matrix.
    substmat_file_name=EBLOSUM62;
    substmat_dir_path=/usr/local/EMBOSS-6.6.0/emboss/data;
    substmat_file_path=${substmat_dir_path}/${substmat_file_name};

    # Run program.
    time python -m src.pipeline.pairwiseCSV_to_pairwiseQuantifier \
         $in_file_path \
         $substmat_file_path \
         $out_map_file_path \
         --gapopen_penalty $gapopen_penalty \
         --gapextend_penalty $gapextend_penalty \
         --verbose \
         > $out_result_file_path \
        || { printf "%s\n" \
                    "It was not possible to quantify the pairwise" \
                    "similarities." \
                    "Please make sure that enough sequences can be globally" \
                    "aligned to each other." \
                    > $signal_file_path;
             exit 1;
           };

# If the starting data contains quantifiers.
elif [ $state == 'quantifier' ];
then

    # FB.
    echo '/====================================================================\';
    echo "Get pairwiseQuantifier.";
    echo "----------------------------------------------------------------------";

    # Input.
    in_dir_path=$start_dir_path;
    in_file_name=$start_mainfile_name;

    # Output.
    out_dir_path=${job_dir_path}/4_quantifier;
    out_result_file_name=quantifier.ssv;
    out_map_file_name=info.csv;
    out_headed_map_file_name=info+header.csv;
    out_result_map_file_name=quantifier+info.ssv;

    # Paths.
    in_file_path=${in_dir_path}/${in_file_name};
    out_result_file_path=${out_dir_path}/${out_result_file_name};
    out_map_file_path=${out_dir_path}/${out_map_file_name};
    out_headed_map_file_path=${out_dir_path}/${out_headed_map_file_name};
    out_result_map_file_path=${out_dir_path}/${out_result_map_file_name};

    # Create output-directory.
    mkdir $out_dir_path;

    # Create symlink to starting data.
    ln -s $in_file_path $out_result_file_path;

    # Create pseudo-map-file.
    for n in $(seq $count);
    do
        echo "$n,$n" >> $out_map_file_path;
    done;

    # FB.
    echo "-> finished.";

fi;

# For result-file.
#
# Create symlink.
ln -s $out_result_file_path ${job_dir_path}/${job_id}_pairwise.txt;

# For headed map-file.
#
# Prepare header.
echo "label,number" > $out_headed_map_file_path;
# Add body.
cat $out_map_file_path >> $out_headed_map_file_path;
# Create symlink.
ln -s $out_headed_map_file_path ${job_dir_path}/${job_id}_numbering.csv;

# FB.
echo "----------------------------------------------------------------------";
echo "Combine result with original labels.";

# Replace entry-number with original entry-header.
awk 'FNR==NR{a[$2]=$1;next} {print a[$1],a[$2],$3}' \
    FS=\, $out_map_file_path \
    FS=' ' $out_result_file_path \
    OFS=' ' \
    > $out_result_map_file_path;

# FB.
echo "-> finished.";
echo '\--------------------------------------------------------------------/';

# =====================================================================|======|
# Run cc_analysis.

# FB.
echo '/====================================================================\';
echo "cc_analysis.";
echo "----------------------------------------------------------------------";

# Input.
in_dir_path=${job_dir_path}/4_quantifier;
in_relation_file_name=quantifier.ssv;
in_map_file_name=info.csv;

# Reference.
ref_dir_path=${job_dir_path}/1_input_secure;
ref_alias_file_name=alias.csv;

# Output.
out_dir_path=${job_dir_path}/5_cc_analysis;
out_log_file_name=log.txt;
out_vec_ssv_file_name=vec.ssv;
out_vec_csv_file_name=vec.csv;
out_vec_map_file_name=vec+info.csv;
out_vec_map2_file_name=vec+info2.csv;
out_vec_map2_headed_file_name=vec+info2+header.csv;

# Paths.
in_relation_file_path=${in_dir_path}/${in_relation_file_name};
in_map_file_path=${in_dir_path}/${in_map_file_name};
ref_alias_file_path=${ref_dir_path}/${ref_alias_file_name};
out_log_file_path=${out_dir_path}/${out_log_file_name};
out_vec_ssv_file_path=${out_dir_path}/${out_vec_ssv_file_name};
out_vec_csv_file_path=${out_dir_path}/${out_vec_csv_file_name};
out_vec_map_file_path=${out_dir_path}/${out_vec_map_file_name};
out_vec_map2_file_path=${out_dir_path}/${out_vec_map2_file_name};
out_vec_map2_headed_file_path=${out_dir_path}/${out_vec_map2_headed_file_name};

# Create output-directory.
mkdir $out_dir_path;

# Go to directory of input.
cd $in_dir_path;

# Run program in directory of input,
# because cc_analysis has problems with long paths.
#
# If cc_analysis encounters connectivity problems, it does NOT seem to
# exit with non-zero status.
# Therefore, do sanity-check later (when moving the result-file).
time cc_analysis -dim $dim \
                 -f \
                 $in_relation_file_name \
                 $out_vec_ssv_file_name \
                 &> $out_log_file_name;

# Go back to directory that is running the pipeline.
cd $run_dir_path;

# Move log-file to output-directory.
# (Even if cc_analysis failed, the log-file exists.)
mv ${in_dir_path}/${out_log_file_name} $out_log_file_path;
# Move output-file to output-directory.
# (If cc_analysis failed, the output-file will NOT exist.)
mv ${in_dir_path}/${out_vec_ssv_file_name} $out_vec_ssv_file_path \
    || { printf "%s\n" \
                "It was not possible to map the pairwise similarities." \
                "This was caused by the presence of 2 (or more) loose groups" \
                "in the dataset." \
                "I.e. the requirement of <i>connections</i> &ge; <i>dim</i>" \
                "was only fulfilled on the inter-${object_type} level," \
                "but not on the inter-group level." \
                "<br>" \
                "The loose groups can be manually identified with the" \
                "output-file 'pairwise.txt'." \
                "Please split your dataset into these loose groups and" \
                "re-run the query on each separate dataset." \
                > $signal_file_path;
         exit 1;
       };

# FB.
echo "----------------------------------------------------------------------";
echo "Re-format result: ssv -> csv.";

# Run program.
python -m src.pipeline.SSV_to_CSV \
       $out_vec_ssv_file_path \
       --verbose \
       > $out_vec_csv_file_path;

# FB.
echo "-> finished.";
echo "----------------------------------------------------------------------";
echo "Combine result with original labels.";

# Paste information from map-file (csv-format) to results.
# Prerequisite: the 2 files should have the same order.
paste -d ',' \
      $out_vec_csv_file_path \
      <(awk -F ',' '{print $1}' $in_map_file_path) \
      > $out_vec_map_file_path;

# Add aliases from alias-file (csv-format).
awk -F ',' \
    'FNR==NR{a[$1]=$2; next} $8 in a{print $0","a[$8]}' \
    $ref_alias_file_path \
    $out_vec_map_file_path \
    > $out_vec_map2_file_path;

# FB.
echo "-> finished.";
echo "----------------------------------------------------------------------";
echo "Add header to result.";

# Prepare header.
#
# 1 Number.
echo -n "number" > $out_vec_map2_headed_file_path;
# dim Cartesian coordinates.
for d in $(seq 1 $dim);
do
    echo -n ",coordinate_${d}" >> $out_vec_map2_headed_file_path;
done;
# 1 Length.
echo -n ",length" >> $out_vec_map2_headed_file_path;
# dim-1 Angles.
for d in $(seq 1 $(( $dim - 1 )));
do
    echo -n ",angle_${d}" >> $out_vec_map2_headed_file_path;
done;
# 1 Name.
echo -n ",label" >> $out_vec_map2_headed_file_path;
# 1 alias (1st word of orignal input name).
echo ",label_alias" >> $out_vec_map2_headed_file_path;

# Add body.
cat $out_vec_map2_file_path >> $out_vec_map2_headed_file_path;

# Create symlink.
ln -s $out_vec_map2_headed_file_path ${job_dir_path}/${job_id}_coordinates.csv;

# FB.
echo "-> finished.";
echo '\--------------------------------------------------------------------/';

# =====================================================================|======|
# Plot results.

# FB.
echo '/====================================================================\';
echo "Plot result of cc_analysis.";

# Working directory.
work_dir_path=${job_dir_path}/5_cc_analysis;

# Input.
in_file_name=vec+info2.csv;
in_file_path=${work_dir_path}/${in_file_name};

# Special case:
# dim=1.
if [ $dim == 1 ];
then
    # Select the 1st dimension for both axes.
    x_dim=1;
    y_dim=1;
# Normal case:
# dim>1.
else
    # Select the 2 highest dimensions.
    x_dim=$(( $dim - 1 ));
    y_dim=$dim;
fi;

# Relevant columns in the input file.
x_col_idx=$x_dim;
y_col_idx=$y_dim;
number_col_idx=0;
label_col_idx=$(( $dim * 2 + 2 ));

# Parameters, that are shared for all plots.
parameters="$in_file_path \
            $x_col_idx $y_col_idx \
            --separator , \
            --x_label coordinate_${x_dim} \
            --y_label coordinate_${y_dim} \
            --edge_colour black \
            --edge_linewidth 0.5 \
            --origin \
            --outfile_bbox tight";

# Initialise enumerator for flip-combinations.
flip_parameters_num=0;

# Do the same for all flip-combinations.
for flip_parameters in '' '--x_invert';
do

    # FB.
    echo "----------------------------------------------------------------------";
    echo "flip_parameters_num: $flip_parameters_num";

    # Output.
    out_normal_file_name=vec+info2_${flip_parameters_num}.svg;
    out_numbered_file_name=vec+info2_numbered_${flip_parameters_num}.svg;
    out_labelled_file_name=vec+info2_labelled_${flip_parameters_num}.svg;

    # Paths.
    out_normal_file_path=${work_dir_path}/${out_normal_file_name};
    out_numbered_file_path=${work_dir_path}/${out_numbered_file_name};
    out_labelled_file_path=${work_dir_path}/${out_labelled_file_name};

    # Run program:
    # Default.
    python -m src.pipeline.scatter \
           $parameters \
           $flip_parameters \
           --alpha 0.5 \
           --outfile $out_normal_file_path;

    # Create symlink.
    ln -s $out_normal_file_path ${job_dir_path}/${job_id}_plot${flip_parameters_num}.svg;

    # FB.
    echo "-> finished normal plot.";

    # Run program:
    # Plot numbering on top of markers.
    python -m src.pipeline.scatter \
           $parameters \
           $flip_parameters \
           --description_col_idx $number_col_idx \
           --alpha 0.1 \
           --outfile $out_numbered_file_path;

    # Create symlink.
    ln -s $out_numbered_file_path ${job_dir_path}/${job_id}_plot${flip_parameters_num}_numbered.svg;

    # FB.
    echo "-> finished numbered plot.";

    # Run program:
    # Plot label on top of markers.
    python -m src.pipeline.scatter \
           $parameters \
           $flip_parameters \
           --description_col_idx $label_col_idx \
           --alpha 0.1 \
           --outfile $out_labelled_file_path;

    # Create symlink.
    ln -s $out_labelled_file_path ${job_dir_path}/${job_id}_plot${flip_parameters_num}_labelled.svg;

    # FB.
    echo "-> finished labelled plot.";

    # Increase enumerator for flip-combinations.
    flip_parameters_num=$(( $flip_parameters_num + 1 ));

done;

# FB.
echo '\--------------------------------------------------------------------/';

# =====================================================================|======|
# If pipeline finished successfully:
# Signal success.

# FB.
echo '/====================================================================\';
echo "Create empty signal-file.";
echo "----------------------------------------------------------------------";

# Create empty signal-file.
touch $signal_file_path;

# FB.
echo "-> Signal that pipeline finished successfully.";
echo '\--------------------------------------------------------------------/';
