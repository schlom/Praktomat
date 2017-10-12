#!/bin/bash

r="\033[31m" # red color
w="\033[0m"  # white color
c="\33[96m"  # cyan color

echo "##############################################"
echo "#   create a new Django Server repository    #"
echo "##############################################"
echo ""
read -p "Please enter new class, e.g. OOP_2099_WS: " name

if [ -z "$name" ]; then
  echo "$r Class must not be empty $w"
  exit 1
fi

for file in /srv/praktomat/* ; do
  if [ -d "$file" ]; then
    fdir=$(basename "$file")
    if [ "$name" = "$fdir" ]; then
      echo "$r Class already exists $w"
      exit 1 
    fi
  fi
done

read -p "Please enter a class name to be copied: " src

echo "$c copy files ... $w"
for file in /srv/praktomat/* ; do
  if [ -d "$file" ]; then
    fdir=$(basename "$file")
    if [ "$src" = "$fdir" ]; then
	cp -aR $src $name
        break
    else
        echo "$r Class not existing $w"
        exit 1
    fi
  fi
done

cd $name
echo "$c switching to virtualenv in $name $w"
. env/bin/activate
echo "$c create new database for $name $w"
sudo -u postgres createdb -O praktomat $name
./Praktomat/src/manage-local.py collectstatic --noinput --link
./Praktomat/src/manage-local.py migrate --noinput
echo "$c create Superuser for new class $w"
./Praktomat/src/manage-local.py createsuperuser
cd ..

echo "Please add the following to your index.html in /srv/praktomat/"
echo "$c"
echo '
			<div class="all-current">
                                <a href="https://127.0.0.1/'$name'/" class="current">
				<span class="lecture">Kursname</span><br/>
				<span class="year">Wintersemester 2017/18</span>
				</a>
			</div>
      '
echo "$w"
echo "also add the following to the end of /etc/apache2/sites-available/000-default.conf"
echo "$c"
echo '
      Use Praktomat '$name' /srv/praktomat/'$name' 80 
     '
echo "$w"
