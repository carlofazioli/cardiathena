#!/bin/bash
if [ ! -f ${HOME}/rsync ]
then
  cp /bin/rsync ${HOME}/rsync

$HOME/rsync -a --delete $SCRATCH/empty_dir/ $SCRATCH/logs_argo/out/
$HOME/rsync -a --delete $SCRATCH/empty_dir/ $SCRATCH/logs_argo/err/