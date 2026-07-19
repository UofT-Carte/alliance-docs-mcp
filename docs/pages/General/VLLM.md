---
title: "VLLM"
url: "https://docs.alliancecan.ca/wiki/VLLM"
category: "General"
last_modified: "2026-07-08T14:30:43Z"
page_id: 28589
display_title: "VLLM"
---

vLLM is a community-driven project that provides high-throughput and memory-efficient inference and serving for large language models (LLMs). It supports various decoding algorithms, quantizations, parallelism, and models from Hugging Face and other sources.

= Installation =

==Latest available wheels==
To see the latest version of vLLM that we have built:

For more information, see Available wheels.

==Installing our wheel==

The preferred option is to install it using the Python wheel as follows:
:1. Load dependencies, load a Python and OpenCV modules,

:2. Create and start a temporary virtual environment.

:3. Install vLLM in the virtual environment and its Python dependencies.
X.Y.Z
}}
where X.Y.Z is the exact desired version, for instance 0.8.4.
You can omit to specify the version in order to install the latest one available from the wheelhouse.

:4. Freeze the environment and requirements set.

:5. Deactivate the environment.

:6. Clean up and remove the virtual environment.

= Job submission =

== Before submitting a job: Downloading models ==

Models loaded for inference on vLLM will typically come from the Hugging Face Hub.

The following is an example of how to use the command line tool from the Hugging face to download a model. Note that models must be downloaded on a login node to avoid idle compute while waiting for resources to download. Also note that models will be cached at by default at $HOME/.cache/huggingface/hub. For more information on how to change the default cache location, as well as other means of downloading models, please see our article on the Hugging Face ecosystem.

 module load python/3.13
 virtualenv --no-download temp_env && source temp_env/bin/activate
 pip install --no-index huggingface_hub
 huggingface-cli download facebook/opt-125m
 rm -r temp_env

== Single Node ==
The following is an example of how to submit a job that performs inference on a model split across 2 GPUs. If your model fits entirely inside one GPU, change the python script below to call LLM() without extra arguments.

This example assumes you have pre-downloaded the model facebook/opt-125m as described on the previous section.

== Multiple Nodes ==
The following example revisits the single node example above, but splits the model across 4 GPUs over 2 separate nodes, i.e., 2 GPUs per node.

Currently, vLLM relies on Ray to manage splitting models over multiple nodes. The code example below contains the necessary steps to start a multi-node Ray cluster and run vLLM on top of it:

Where the script config_env.sh is:

The script launch_ray.sh is:

And finally, the script vllm_example.py is: