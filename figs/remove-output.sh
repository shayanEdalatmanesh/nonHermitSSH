for notebook in *ipynb
do
    echo "cleanup" $notebook
    jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace $notebook
done
