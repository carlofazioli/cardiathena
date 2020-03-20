#!/bin/bash
salloc --cpus-per-task=16 --mem=8G --exclude=NODE[040-080]
