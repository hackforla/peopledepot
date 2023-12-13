export file=$1
echo "file = $file / $1 / $2"
if [ file == "" ]
then
  echo "File not specified.  Using .env"
  file = ".env"
fi
echo "Loading environment variables from $file"
if [ ! -f $file ]
then
  echo "File $file not found"
  exit 1
else
  export $(grep -v '^#' $file | xargs)
fi