# TOOD: see cookie cutter code.. 
if [ $# -eq 0 ]; then
    echo "Error: No arguments provided. Need to pass a folder name "
    exit 1
fi

# TODO check that folder name exists.. 

root_dir="/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/studies"
target_folder="$root_dir/$1"
echo "Folder Name: $1"
# echo "Folder to add in: $target_folder"

create_path() {
    location=$2
    dir="$root_dir/$location/$1"
    if  [ ! -d $dir ]; then 
        echo "Error: Not a valid path: $dir"
        exit 1
    fi
    new_dir="$dir/$3"
    echo "preparing to make a path at $new_dir"
    mkdir $new_dir
}


create_path $1 "static" "_01_inputs" 
create_path $1 "static" "_02_plans" 
create_path $1 "static" "_03_models" 
create_path $1 "static" "_04_temp" 
create_path $1 "static" "_05_figures" 

create_path $1  "src/studies" "generation" 
create_path $1  "src/studies" "dataframes" 
create_path $1  "src/studies" "plots" 



