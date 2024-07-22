export PYTHONPATH="${PYTHONPATH}:/Users/asabuncuoglu/Documents/faid"

if [ "$1" == "init" ]; then
    python -m src.faid --mod init
fi

if [ "$1" == "scan" ]; then
    python -m src.faid --mod scan
fi
