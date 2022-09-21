#! /bin/bash

# En file espero tener un archivo csv
file=$1
name=$(echo $file | awk -F '.' '{print $1}')
new_file="$name"otro.csv

# Pasamos todo a minúsculas
awk '{if (NR == 1) gsub(/ /,"_"); print tolower($0)}' $file > "$new_file"

# Limpiamos algunos caracteres
sed -i 's/√≠/í/g' $new_file
sed -i 's/√≥/ó/g' $new_file
sed -i 's/√∫/ú/g' $new_file
sed -i 's/√©/é/g' $new_file
sed -i 's/√°/á/g' $new_file

sed -i 's/√ì/ó/g' $new_file

mv "$new_file" "../datasets/$new_file"
echo -e "$new_file is ready"