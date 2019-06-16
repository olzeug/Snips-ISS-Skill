#/usr/bin/env bash -e

VENV=venv

if [ ! -d "$VENV" ]
then

    PYTHON=`which python3`

    if [ ! -f $PYTHON ]
    then
        echo "could not find python"
    fi
    virtualenv -p $PYTHON $VENV

fi

. $VENV/bin/activate
chmod +x /var/lib/snips/skills/Snips-ISS-Skill/action-olzeug-getPeopleonISS-olzeug.ISS.py /var/lib/snips/skills/Snips-ISS-Skill/action-olzeug-locationofISS-olzeug.ISS.py
pip install -r requirements.txt
