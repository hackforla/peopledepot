file = $1

if [ file == "" ]
then
  file = ".env"
fi

if [ ! -f $file ]
then
  echo "File $file not found"
  exit 1
else
  export $(grep -v '^#' cat .env | xargs)
fi