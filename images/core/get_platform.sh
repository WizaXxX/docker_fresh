cd /out_files
DISTR_FILE_VERSION=$(ls  | grep "client" | grep -Eo "[0-9]+\_[0-9]+\_[0-9]+\_[0-9]+")
DISTR_VERSION=$(ls  | grep "client" | grep -Eo "[0-9]+\_[0-9]+\_[0-9]+\_[0-9]+" | sed 's/_/./g')
DISTR_VER1=$(echo $DISTR_VERSION | cut -d '.' -f 1-3)
DISTR_VER2=$(echo $DISTR_VERSION | cut -d '.' -f 4)

common_file_name=1C_Enterprise83-common-$DISTR_VER1-$DISTR_VER2.x86_64.rpm
server_file_name=1C_Enterprise83-server-$DISTR_VER1-$DISTR_VER2.x86_64.rpm
ws_file_name=1C_Enterprise83-ws-$DISTR_VER1-$DISTR_VER2.x86_64.rpm
client_file_name=1C_Enterprise83-client-$DISTR_VER1-$DISTR_VER2.x86_64.rpm

tar -xvf client_$DISTR_FILE_VERSION.rpm64.tar.gz $client_file_name -C /main_dir/distr
tar -xvf rpm64_$DISTR_FILE_VERSION.tar.gz $common_file_name $server_file_name $ws_file_name -C /main_dir/distr

