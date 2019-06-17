if [ "$1" = "install" ]
then
    sudo python -m virtualenv env3
fi

source env3/bin/activate

if [ "$1" = "install" ]
then
    pip install -r requirements.txt
    python savecookie.py
fi

bash clean_data.sh
python videos_only.py -n 100 -sleep 1
