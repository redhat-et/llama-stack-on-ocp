## Run Guidellm to Evaluate & Optimize LLMs

[Guidellm](https://github.com/neuralmagic/guidellm/blob/main/README.md) is a powerful tool for evaluating and optimizing the deployment of large
language models (LLMs).

Here's an example to run `guidellm` with `meta-llama/Llama-3.2-3B-Instruct` that has been deployed with this
[llama-serve manifests](../../llama-serve/llama3.2-3b/vllm.yaml). Replace the `--target` and references to `Llama-3.2-3B` in
[guidellm-job.yaml](./guidellm-job.yaml) to evaluate any served LLM.

### Run evaluation

```bash
oc apply -f pvc.yaml
oc apply -f guidellm-job.yaml
```

> **📝 NOTE:** The HF_TOKEN is passed to the job, but this will not be necessary if you use the same PVC as the one storing your model.
> Guidellm uses the model's tokenizer/processor files in its evaluation. You can pass a path instead with `--tokenizer=/path/to/model`.
> This eliminates the need for Guidellm to download the files from Huggingface.

The PVC is RWX, so all guidellm pods can access the results.
The logs from the job will show pretty tables that summarize the results. There is also a large yaml file created. The evaluation for this model
will take ~25 minutes.

### Extract Guidellm Report

To extract the results, first run a job to compress the report file. Then, create an accessor pod from which you can use `oc rsync` to download the
results.

```bash
oc apply -f retriever-job.yaml
oc apply -f accessor-pod.yaml
mkdir guidellm-reports
oc rsync guidellm-accessor:/mnt/output/guidellm-reports.tgz ./guidellm-reports
# ignore the WARNING: cannot use rsync: rsync not available in container
```

You will now have a local `./guidellm-reports/guidellm-reports.tgz`, to extract it run:

```bash
tar -xvf guidellm-reports.tgz
```

You will now have a local file `./guidellm-reports/llama32-3b.yaml`
You can remove the accessor pod with:

```bash
oc delete pod guidellm-accessor
```
