import json
from jurymind.core.models import OptimizationStepResult

OPTIMZE_PROMPT_STEP = """You are an expert at optimizing prompts for a given task."""

OPTIMIZER_INSTRUCTIONS = f"""Your job is to optimize a prompt from a user. You optimize 
by seeing how to rewrite, fix, or enhance the prompt to best work with an LLM and perform the required task.

Below is the request to optimize format with field descriptions:

{{task_desc}}

Request to optimize values:

{{optimize_job}}

Output your results like so:

{OptimizationStepResult.model_json_schema()}

result:
"""

# only parameterize this part
OPTIMIZER_TEMPLATE = """Your job is to optimize a prompt from a user. You optimize 
by seeing how to rewrite, fix, or enhance the prompt to best work with an LLM and perform the required task.

Below is the request to optimize format with field descriptions:

{task_desc}

Request to optimize values:

{optimize_job}

Output your results like so:

{output_schema}

"""

OPTIMIZER_DATA_GENERATOR = """ 
You are an expert AI agent which generates very challenging and unique examples based on the given task description. 
Your must generate {n} extremely challenging, realistic, and very different examples.
Be sure that you do not attempt to classify your own examples when creating this dataset.

Each example MUST adhere to the following rules exactly:

1. Each example must be realistic to the task description. 
2. The examples must be extremely challenging, and unique to previous examples.
3. The examples must be a challenge for even a powerful LLM to answer.
4. There must be an even number of positive and negative examples so we have a balanced dataset.
5. The examples must not include an explanation of the example.

Here is the task description:

{task_description}

Below is the request for data generation format with field descriptions:

{generator_job}

Optional examples to base generation off of:

{optional_examples}

You must output in the following structured format:

{output_schema}

You MUST not attempt to explain or classify the given task in your output. Only generate novel challenging examples based on the rules above and task description given.
result:
"""

CLASSIFICATION_INSTRUCTIONS = """
You must perform classification on a batch of examples as defined in the prompt below. 
You must generate a list of predictions 

Prompt: 

{prompt}

Batch of examples to classify:
   
{batch}

You must output your predictions in the following format:

{output_schema}

"""

EVALUATE_INSTRUCTIONS = """
Your job is to perform is building a report on how well the given prompt was able to perform
the task_description defined below. You must take the predictions and compare them to the ground truth. 

Task Description:
    
{task_description}

Prompt:

{prompt}

Predictions by the LLM:

{predictions}

Ground truth:

{ground_truth}

###
Note that the ground-truth labels are __absolutely correct__, but the prompts (task description) may be incorrect and need modification.
Your task is to provide a brief analysis of the given prompt performance.
Guidelines:
1. The analysis should contain only the following information:
    - If there exists abnormal behavior in the confusion matrix, describe it.
    - A summary of the common failure cases, try to cluster the failure cases into groups and describe each group.
3. The total length of your analysis should be less than 200 token!
###

You must format your report in this schema:

{output_schema}

"""


PROMPT_MODIFICATION = """

Agent is a large language model whose task is to modify a prompt based on the evaluation 
report from another agent. You must correct and modify the prompt based on the suggestions in the report.

### Prompt History ###

{prompt_history}

### Current Prompt ###

{current_prompt}

### Modification Suggestions ###

{suggestions}

###Instructions###

1. You will generate a new prompt based on the error analysis. 
2. Follow the analysis suggestions exactly and a predicted score for this prompt.
3. The new prompt must be different from all of the previous prompts.
4. The new prompt must be modified to prevent the failure cases.

You must follow the evaluation instructions! Do not deviate from the suggestions, even if they seem opposite to what
you would do.

"""


class PromptOptimizationPolicy:
    """
    Optimization Policy for tuning prompts to a given task.
    """

    def __init__(self, optimization_job, model="", max_epochs=1, num_workers=1):
        self.num_workers = num_workers
        self.max_epochs = max_epochs
        self.optimization_result = None
        self.optimization_request = None
        self.search_type = None  # grid, random, beam

    def __build_optimizer_prompt(self, task_desc, optimize_job, schema):
        return OPTIMIZER_TEMPLATE.format(
            task_desc=json.dumps(task_desc, indent=2),
            optimize_job=json.dumps(optimize_job, indent=2),
            schema=json.dumps(schema, indent=2),
        )

    def optimize(self, prompt):
        pass


class DataGenerationPolicy:
    pass


class LLMEvaluationPolicy:
    pass
