#!/usr/bin/env bash

FT_MODEL_NAME="wiki-ru.bin"
FT_MODEL_SOURCE="transfer.sh/QNBOEw/${FT_MODEL_NAME}"

IN_PROJECT_DESTINATION="data/models"
TMP_FOLDER=$(mktemp -d -t artifacts-XXXXXXXXX)


mkdir -p $TMP_FOLDER
curl https://${FT_MODEL_SOURCE} -o ${IN_PROJECT_DESTINATION}/${FT_MODEL_NAME}

#curl -f -k -u${USER}:${PASSWORD} "https://${FT_MODEL_SOURCE}" -o ${TMP_FOLDER}/${FT_MODEL_NAME}
#if [[ $? -ne 0 ]]; then echo "Failed download https://${FT_MODEL_SOURCE}"; exit 1; fi
## unzip artifacts
#mkdir -p ${IN_PROJECT_DESTINATION}/${VERSION}
#unzip -o ${TMP_FOLDER}/${MODEL_FILE_NAME} -d ${IN_PROJECT_DESTINATION}/${VERSION}
#if [[ $? -ne 0 ]]; then echo "Failed to unzip ${IN_PROJECT_DESTINATION}/${VERSION}/${MODEL_FILE_NAME}"; exit 1; fi

rm -r $TMP_FOLDER