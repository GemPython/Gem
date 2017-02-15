usage=false

case $# in
  0) ;;
  1) usage=true ;;
esac

if $usage
then
    echo "? usage: $0" >&2
    exit 1
fi

tmp_dir='../tmp'

if [ ! -d $tmp_dir ]
then
    mkdir $tmp_dir
fi

tmp1=$tmp_dir/tmp.1.$$.txt

for i in 1 2 3 15
do
    trap "trap $i; rm -f $tmp1; kill -$i $$; exit $i" $i
done

amount=1
command='python ../Beryl/Beryl.py'

while :
do
    $command </dev/null >&$tmp1

    if cmp -s $tmp1 r
    then    
        case $amount in
          [1-8]) amount=`expr $amount + 1` ;;
        esac
    else
        mv $tmp1 r
        amount=1
    fi

    sleep 0.01
done
