uv run jupyter nbconvert --to notebook --execute prep-00.metadata.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  --inplace

uv run jupyter nbconvert --to notebook --execute prep-00.motus.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  --inplace

uv run jupyter nbconvert --to notebook --execute prep-00.virus.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  --inplace

uv run jupyter nbconvert --to notebook --execute prep-01.cooccurrence.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  --inplace

uv run jupyter nbconvert --to notebook --execute prep-01.tableS1.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  --inplace

uv run jupyter nbconvert --to notebook --execute prep-02.post-cooccurrence.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  --inplace

uv run jupyter nbconvert --to notebook --execute prep-03.tableS3.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  --inplace

uv run jupyter nbconvert --to notebook --execute prep-04.tableS4.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  --inplace