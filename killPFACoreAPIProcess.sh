#!/bin/bash
source $HOME/.zprofile
root_path=$ROOT
database=PortFolioAnalytics
file_name=PortFolioAnalytics-Backup



# Find the process using port 8500
pid=$(lsof -t -i:8000)

# Check if the process ID exists
if [ -n "$pid" ]; then
  echo "Killing process with PID $pid running on port 8000..."
  kill -9 $pid
  echo "Process killed."
else
  echo "No process found running on port 8000."
fi

#source ~/PFAEnvs/py311API/bin/activate
#
#cd ./PortFolioAnalytics/PFACoreAPI/
#
#uvicorn app.main:app --port 8000 --reload

