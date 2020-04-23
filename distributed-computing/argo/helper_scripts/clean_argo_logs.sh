#!/bin/bash

$HOME/rsync -a --delete $SCRATCH/empty_dir/ $SCRATCH/logs_argo/out/
$HOME/rsync -a --delete $SCRATCH/empty_dir/ $SCRATCH/logs_argo/err/
