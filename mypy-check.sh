#!/bin/bash
counter=0
for file in $(git diff --diff-filter=d --cached --name-only | grep -E '\.(py)$')
do
  pipenv run mypy "$file" --follow-imports=silent
  if [ $? -ne 0 ]; then
    echo "Mypy failed on staged file '$file'. Please check your code and try again."
    ((counter++)) # exit with failure status
  fi
done
if [ $counter -ne 0 ]; then
  exit 1 # exit with failure status
fi