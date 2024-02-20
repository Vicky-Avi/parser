# parser

Folder Strtucture:
corrupted_files ==> Folder which contains the corrupted input files                                                                                                                                                    cleaned_files   ==> Folder which contains the output file with cleaned up data.                                                                                                                                       
config.json     ==> File contains the input arguments like files path, extension details, etc. in json format.
build_in_parser.py ==> Script which is used to pars the corrupted data without external packages.
csvparser.py ==> Script which is used to parse the corrupted data by using pandas package

How to run:
python build_in_parser.py ==> without external package
python csvparser.py ==> with external package

Packages used:
pandas ==> Pandas package will help you to have the read and write operations inbuild and also it can able to read 'n' number of datas and making it as a dataframe, which is easy to do some specific operations like            search, drop, etc.,
json   ==> Json package used to parse the input details from config.json


