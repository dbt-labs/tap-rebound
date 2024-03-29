#!/bin/bash

### Load configuration
echo "$STITCH_CONFIG" > persist.json
echo "$TAP_CONFIG" > config.json
echo "$CATALOG" > catalog.json

aws s3 cp "$TAP_STATE_S3_FILE_PATH" state.json || echo "{}" > state.json

### Run the tap
{ tap-rebound -s state.json -c config.json --catalog catalog.json | target-stitch -c persist.json > state.log; }

tail -n1 state.log > new-state.json

### Save state file
if [ -s new-state.json ]
then
    aws s3 cp new-state.json "$TAP_STATE_S3_FILE_PATH"
fi
