#!/bin/bash
salloc --cpus-per-task=16 --mem=8G --exclude=NODE[040,041-049,050,051-054,056,076-081,071-075,083-087]
