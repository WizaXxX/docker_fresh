cd /out_files

tar -xvf client*.rpm64.tar.gz --exclude "*thin*.rpm" --exclude "*nls*.rpm" --exclude "license-tools" -C /main_dir/distr
tar -xvf  rpm64_*.tar.gz --exclude "*crs*.rpm" --exclude "*nls*.rpm" -C /main_dir/distr
