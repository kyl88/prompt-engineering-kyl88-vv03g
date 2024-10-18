from .zero_shot import ZERO_SHOT_PROMPT
from .few_shot import FEW_SHOT_PROMPT
from .chain_of_thought import CHAIN_OF_THOUGHT_PROMPT
from .tree_of_thought import TREE_OF_THOUGHT_PROMPT
from .examples import EXAMPLES_PROMPT

PROMPT_TECHNIQUES = {
    "Zero-Shot": ZERO_SHOT_PROMPT,
    "Few-Shot": FEW_SHOT_PROMPT,
    "Chain of Thought": CHAIN_OF_THOUGHT_PROMPT,
    "Tree of Thought": TREE_OF_THOUGHT_PROMPT,
    "Examples": EXAMPLES_PROMPT
}