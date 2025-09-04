# Prototyping an Autonomous Agent: From Concept to Python Implementation

This notebook documents the architecture of an autonomous agent. The objective is to establish a conceptual system capable of operating continuously, making decisions, and executing actions in a perpetual cycle. The architecture outlined here serves as the foundation for an autonomous operating system, programmed by states and capable of performing system functions without interruption, such as self-evaluation and self-improvement.

## 1. The Theoretical Foundation: LLMs and Agent Autonomy

An autonomous agent is an AI system with the capacity to operate with a degree of independence, processing information and making decisions to achieve predefined goals. In this project, the Large Language Model (LLM) is not just a component, but the cognitive core of the agent, responsible for interpreting and generating systemic actions based on sequential pages containing a set of decisive instructions and available outputs to be navigated in a graph and state model, inspired by self-guided RPG books, by the LLM. These instructions are special commands containing semantic meaning (the textual instructions we will send via RAG), with the instructions, technically speaking, being representations of regions on the model's vector map.

Two key approaches to empowering the LLM for our proto-system could be explored:

* **Fine-tuning:** A costly and time-consuming training process that adjusts the parameters of a language model with a specific dataset. The resulting accuracy is high, but the computational cost makes it unsuitable for the initial prototyping phase, where flexibility is a priority.
* **RAG (Retrieval-Augmented Generation):** A more flexible and cost-efficient methodology. The agent retrieves information from an external knowledge base (simulated by a dictionary) and injects it into the LLM's prompt, replacing the semantic commands that could be embedded in a fine-tuning layer. This approach allows us to prototype the command logic and system behavior without the need to retrain the model, facilitating iteration and the development of the core architecture.

The prototype presented here employs RAG logic to demonstrate the feasibility of an agent capable of querying a knowledge base and executing commands dynamically, establishing a foundation for its future autonomy.

## 2. The Agent's Architecture: The Perpetual Feedback Loop

The mechanics of an autonomous agent are based on a continuous feedback loop, known as the *OODA Loop (Observe, Orient, Decide, Act)*. This four-stage cycle defines the operational logic of our system, ensuring its ability to be always active.

* **Observe:** The agent collects information from the environment and its own state. In our model, this includes the narrative of a "page" and logs of previous command executions.
* **Orient:** The agent processes the observed information, contextualizes it, and updates its internal state. It uses its knowledge (inventory, skills, etc.) to interpret the environment and available options.
* **Decide:** Based on its purpose and current state, the agent formulates a decision. This stage involves selecting an action or generating a command for the next cycle.
* **Act:** The agent executes the decided action. The output of the action is the input for the next iteration of the OODA loop, creating an uninterrupted flow of command and response.

This cyclic loop architecture is what allows for the agent's continuous operation, analogous to the cycle of a processor in a physical computer, where the result of one instruction determines the next.

## 3. The Conceptual System: Command Language and State Machine

To materialize the *OODA Loop*, we employ a state machine over a graph model. Each state is represented by a "page" from an RPG book, and the transitions between states are the logical choices the agent makes. This system establishes the foundation for more complex systemic functions.

* **Nodes:** Each page is a node in the graph, containing a narrative and available commands.
* **Edges:** The choices on each page are the edges that lead to other nodes, representing state transitions.
* **State:** The agent's state is defined by the current page and its "inventory" (internal data, such as skills or status).

The page architecture is fundamental for the future implementation of advanced functions. It allows the agent to execute background system tasks, such as self-evaluation and self-improvement. The agent can have an idle state (*idle state*), in which, instead of just waiting for external input, it triggers internal commands to:

* **Self-evaluation:** Analyze past execution logs to identify inefficiencies.
* **Self-improvement:** Generate new commands or optimize existing logic.

In a future phase, this architecture will support more functionalities with active context monitoring, the creation of an identity and purpose module, and a module for the self-incremental generation of action graphs for problem-solving with graph memory for best solution, so that it is possible to remember paths already taken without the need to re-discover them and incorporating some gradient of personality like gambling tendency to define it’s behavior, for example. This would allow the agent to pursue long-term goals, like an autonomous purchasing system that researches, negotiates, buys, re-evaluates the process, and restarts the cycle for a new item from its task backlog, and in an idle state, re-evaluates the used graphs and proposes changes, on GitHub as a PR, for example, based on its own analysis using external tools like the web search and other sources.

## 4. The Implementation: A Python Prototype

The code below defines the "world" (the state graph) and the agent class. The agent navigates the "book" autonomously, choosing the optimal path to complete its mission, demonstrating the functionality of the OODA loop.