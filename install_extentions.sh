wget https://github.com/galaxy001/pirs/archive/master.zip;
unzip master.zip;
cd pirs-master/;
sudo apt-get install libboost-dev;
cd /src;
./genauto.sh;
./configure;
make;
sudo make install;
cd ../..;
mkdir assemblers;
cd assemblers;
apt-get install abyss;
wget https://github.com/bachev/mira/releases/download/V5rc1/mira_V5rc1_linux-gnu_x86_64_static.tar.bz2;
tar -xvjf mira_V5rc1_linux-gnu_x86_64_static.tar.bz2;
mv mira_V5rc1_linux-gnu_x86_64_static mira;
cd mira/;
cd dbdata/;
./mira-install-sls-rrna.sh rfam_rrna-21-1.sls.gz;
cd ../..;
wget http://www.bcgsc.ca/platform/bioinfo/software/ssake/releases/4.0/ssake_v4-0.tar.gz;
tar -xzvf ssake_v4-0.tar.gz;
wget http://www.genomic.ch/edena/EdenaV3.131028.tar.gz;
tar -xzvf EdenaV3.131028.tar.gz;
mv EdenaV3.131028 edena;
cd edena/;
make;
cd ..;
wget https://github.com/alekseyzimin/masurca/raw/master/MaSuRCA-3.3.1.tar.gz;
tar -xzvf MaSuRCA-3.3.1.tar.gz;
mv MaSuRCA-3.3.1 masurca;
cd masurca;
./install.sh;
cd ..;
wget http://kmergenie.bx.psu.edu/kmergenie-1.7051.tar.gz;
tar xzfv kmergenie-1.7051.tar.gz;
cd kmergenie-1.7051/;
make;
python3 setup.py install;
cd ..;
wget http://cab.spbu.ru/files/release3.13.1/SPAdes-3.13.1-Linux.tar.gz;
tar -xzf SPAdes-3.13.1-Linux.tar.gz;
mv SPAdes-3.13.1-Linux spades;
git clone git://github.com/dzerbino/velvet.git;
git clone --recursive https://github.com/GATB/minia.git/;
cd minia;
sh INSTALL;
cd ..;
cd ..;
wget https://sourceforge.net/projects/quast/files/quast-5.0.2.tar.gz;
tar -zxvf quast-5.0.2.tar.gz
mv quast-5.0.2 quast;
cd quast/;
sudo python3 setup.py install_full;




