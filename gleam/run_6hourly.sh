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

python download.py
python gleam.py -n 100 -headless 1 -sleep 1
bash clean_data.sh
python subscribe_like_follow.py -headless 1
bash clean_data.sh
