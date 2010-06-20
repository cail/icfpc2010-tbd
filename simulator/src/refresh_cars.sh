python ./submit_fuel.py listcars > ../data/car_ids
python ./submit_fuel.py loadcars >> ../data/car_data
sort -g ../data/car_data > ../data/car_data_sorted
