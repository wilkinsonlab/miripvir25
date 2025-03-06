import pandas as pd
import yaml
import os 
from jinja2 import Template

template_str = """#!/bin/bash
#SBATCH --job-name={{ run_name }}
#SBATCH -c={{ processors }}
#SBATCH -m={{ memory }}GB
#SBATCH --output={{ run_name }}.$SLURM_ARRAY_TASK_ID.out
#SBATCH --array=1-{{ array_length }}
#SBATCH --time={{ time_limit }}
#SBATCH --partition={{ partition }}


input=run
library_name=$(awk -v i=$SLURM_ARRAY_TASK_ID '$1==i {print $2}' $input)
cd $library_name
srun ploomber build -e {{ pipeline_location }}

"""


def create_environments(product, change, source_env, source_data, run_name, pipeline_location, cwd):
    """
    create_environments
    ===

    """
    source_data = pd.read_csv(source_data)
    with open(source_env, "r") as file:
        source_env = yaml.safe_load(file)
    
    out = []
    for i, row in source_data.iterrows():
        library_name = row['library_name']
        os.makedirs(cwd + '/' + library_name, exist_ok=True)
        mod_env = source_env.copy()
        for key in change:
            mod_env.update({key: row[key]})
        mod_env['pipeline_location'] = pipeline_location
        with open(cwd + '/' + library_name + '/env.yaml', 'w') as f:
            yaml.safe_dump(mod_env, f)
        out.append(" ".join([str(i + 1), library_name]))

    with open(product, 'w') as f:
        f.write('\n'.join(out))


def create_sbatch(upstream, product, run_name, processors, memory, time_limit, partition, pipeline_location):
    """
    create sbatch
    ===

    """
    array = pd.read_csv(upstream['create_environments'])
    array_length = len(array) + 1 # Counting from 1
    template = Template(template_str)
    context = dict(
        run_name = run_name,
        array_length = array_length,
        time_limit = time_limit,
        partition = partition,
        pipeline_location=pipeline_location,
        memory=memory,
        processors=processors
    )
    slurm_job_file = template.render(context)
    with open(product, 'w') as f: 
        f.write(slurm_job_file)