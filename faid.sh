export PYTHONPATH="${PYTHONPATH}:/Users/asabuncuoglu/Documents/faid"

if [ "$1" == "init" ]; then
    python -m faid.main --mod init
fi

if [ "$1" == "scan" ]; then
    python -m faid.main --mod scan
fi
