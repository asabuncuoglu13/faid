export PYTHONPATH="${PYTHONPATH}:/Users/asabuncuoglu/Documents/faid"

if [ "$1" == "init" ]; then
    python -m faid.main --mod init
fi

if [ "$1" == "scan-data" ]; then
    python -m faid.main --mod scan-data
fi

if [ "$1" == "scan-model" ]; then
    python -m faid.main --mod scan-model
fi
