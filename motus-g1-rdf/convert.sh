
# Check if the outputs of the pipeline tasks are already present
if [ ! -f "{{ upstream['sites_and_libraries']['data'] }}" ]; then
    echo "Missing output for sites_and_libraries task."
    exit 1
fi

if [ ! -f "{{ upstream['host']['data'] }}" ]; then
    echo "Missing output for host task."
    exit 1
fi

if [ ! -f "{{ upstream['virus']['data'] }}" ]; then
    echo "Missing output for virus task."
    exit 1
fi

if [ ! -f "{{ upstream['bacteria']['data'] }}" ]; then
    echo "Missing output for bacteria task."
    exit 1
fi


cp data-model.yarrrml.yaml output/
docker run --rm -it -v $(pwd)/output:/data rmlio/yarrrml-parser:latest -i /data/data-model.yarrrml.yaml -o /data/mulvirisk.v4.rml
docker run --rm -v $(pwd)/output:/data rmlio/rmlmapper-java -m mulvirisk.v4.rml -s turtle > "{{ product['ttl'] }}"
# rm output/data-model.yarrrml.yaml