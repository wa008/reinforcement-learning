if [ $# != 1 ] ; then
	echo "need comment!"
	exit 1
fi

comm=$1
echo "comment: ${comm}"

git pull

git add *
git status 

# echo "check commit... Yes or No"
# echo "Yes : 1"
# echo "No  : 0"
# read flag
# if [ $flag != 1 ] ; then
# 	echo "No, exit"
# 	exit 1
# else
#     echo "Yes, continue"
# fi

git commit -m "$comm"
git push origin main