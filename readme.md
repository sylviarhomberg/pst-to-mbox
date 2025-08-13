# Convert from PST to MBOX

First, build with docker using `docker build -t pst_parser .` and then run the container.
We run the container using `docker run --rm -v your-pst-file-path -v your-target-folder pst_parser`.

## Create the Thunderbird file structure (using .sbd files)

If you intend on using this export for Thunderbird, install python3 on your machine, ensure that you have set 
your folder path in the create_sbd file, and run `python3 create_sbd.py`.