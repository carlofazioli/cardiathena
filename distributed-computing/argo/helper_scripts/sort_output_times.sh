#!/bin/bash
# Extracts run times of the games
ls -tr1 | stat -c%y /scratch/$USER/logs_argo/out/*.out >> times
sort -t. -k 3.1,3.15 < times > runtimes
rm times

