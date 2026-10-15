"""Curated question bank for student placement & technical interviews.

Covers roles:
- Software Developer / General SDE
- Python Developer
- Java Developer
- AI/ML Engineer
- Web / Full Stack Developer
- HR & Behavioral Questions (STAR methodology)
"""

from typing import List, Dict, Any

INTERVIEW_QUESTION_DATASET: List[Dict[str, Any]] = [
    # ==========================================
    # SOFTWARE DEVELOPER / GENERAL SDE (Technical)
    # ==========================================
    {
        "id": "sde-tech-01",
        "role": "Software Developer",
        "category": "technical",
        "difficulty": "Beginner",
        "topic": "Data Structures",
        "question": "Can you explain the difference between an Array and a Linked List, and when you would choose one over the other in terms of time and space complexity?",
        "expected_key_points": [
            "Contiguous vs non-contiguous memory allocation",
            "O(1) random access for arrays vs O(n) traversal for linked lists",
            "O(1) insertion/deletion at head/pointer vs O(n) shifting for arrays",
            "Cache locality advantages of arrays",
            "Memory overhead of node pointers in linked lists",
        ],
        "reference_answer": "An Array stores elements in contiguous memory locations, allowing O(1) constant-time random access using an index. However, resizing and insertions/deletions in the middle take O(n) due to element shifting. A Linked List stores nodes scattered in memory linked by pointers; insertions and deletions at known pointer locations take O(1), but accessing an element by index requires O(n) sequential traversal. Use arrays when random access and cache locality are critical, and linked lists when frequent insertions and deletions occur without requiring random indexing.",
        "rubric": {
            "relevance_weight": 0.25,
            "technical_weight": 0.35,
            "clarity_weight": 0.20,
            "completeness_weight": 0.20,
        },
    },
    {
        "id": "sde-tech-02",
        "role": "Software Developer",
        "category": "technical",
        "difficulty": "Intermediate",
        "topic": "Object-Oriented Programming",
        "question": "What are the four pillars of Object-Oriented Programming (OOP)? Explain how polymorphism works with a practical software design example.",
        "expected_key_points": [
            "Encapsulation, Abstraction, Inheritance, Polymorphism",
            "Compile-time (method overloading) vs run-time polymorphism (method overriding)",
            "Interface or base class reference pointing to derived subclass",
            "Dynamic method dispatch via vtable",
        ],
        "reference_answer": "The four pillars are Encapsulation (bundling data and methods while restricting direct access), Abstraction (hiding implementation details and exposing simple interfaces), Inheritance (reusing code across parent-child hierarchies), and Polymorphism (the ability for different classes to respond to the same method call in class-specific ways). Polymorphism can be static (compile-time method overloading) or dynamic (runtime method overriding). For example, a PaymentProcessor interface with a processPayment() method can be implemented by CreditCardPayment, PayPalPayment, and CryptoPayment. The checkout service calls processor.processPayment() polymorphically without knowing the concrete payment gateway.",
        "rubric": {
            "relevance_weight": 0.25,
            "technical_weight": 0.35,
            "clarity_weight": 0.20,
            "completeness_weight": 0.20,
        },
    },
    {
        "id": "sde-tech-03",
        "role": "Software Developer",
        "category": "technical",
        "difficulty": "Intermediate",
        "topic": "Operating Systems & Concurrency",
        "question": "Explain the difference between a Process and a Thread, and what causes a deadlock in multithreaded systems.",
        "expected_key_points": [
            "Process has independent virtual memory space; threads share address space and heap",
            "Thread creation and context switching overhead is significantly lighter",
            "Deadlock definition: two or more threads permanently blocked waiting for resources held by each other",
            "Coffman conditions: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait",
        ],
        "reference_answer": "A process is an executing instance of a program with its own isolated address space, file descriptors, and OS resources. A thread is a lightweight unit of execution within a process that shares the process's code, data, and heap, but has its own stack and registers. Deadlock occurs when threads are unable to proceed because each holds a resource the other needs. The four Coffman conditions required for deadlock are: Mutual exclusion, Hold and wait, No preemption, and Circular wait. Deadlocks can be prevented by enforcing strict resource acquisition hierarchies or using timeouts on locks.",
        "rubric": {
            "relevance_weight": 0.25,
            "technical_weight": 0.35,
            "clarity_weight": 0.20,
            "completeness_weight": 0.20,
        },
    },
    {
        "id": "sde-tech-04",
        "role": "Software Developer",
        "category": "technical",
        "difficulty": "Advanced",
        "topic": "System Design & Databases",
        "question": "What is Database Indexing? How does a B-Tree index work under the hood, and what are the trade-offs of having too many indexes?",
        "expected_key_points": [
            "Index as an auxiliary search data structure to speed up reads from O(N) to O(log N)",
            "Balanced tree structure with high fan-out (B-Tree/B+ Tree)",
            "Leaf nodes contain sorted keys and row pointers (or clustered table rows)",
            "Trade-offs: write amplification (slower INSERT/UPDATE/DELETE) and extra disk storage",
        ],
        "reference_answer": "Database indexing creates an auxiliary data structure that allows the query engine to locate matching rows in logarithmic time O(log N) instead of scanning the full table sequentially O(N). Most relational databases use B-Trees or B+ Trees because their high branching factor minimizes disk I/O depth. In a B+ Tree, internal nodes store keys and page pointers guiding traversal, while leaf nodes store the ordered keys and record pointers connected in a doubly linked list for fast range scans. While indexes drastically accelerate SELECT queries, having too many indexes increases write amplification—every INSERT, UPDATE, or DELETE must maintain all affected index trees, slowing down write throughput and consuming significant disk storage.",
        "rubric": {
            "relevance_weight": 0.25,
            "technical_weight": 0.35,
            "clarity_weight": 0.20,
            "completeness_weight": 0.20,
        },
    },

    # ==========================================
    # PYTHON DEVELOPER (Technical)
    # ==========================================
    {
        "id": "py-tech-01",
        "role": "Python Developer",
        "category": "technical",
        "difficulty": "Beginner",
        "topic": "Python Core",
        "question": "What is the difference between mutable and immutable types in Python, and how does Python pass arguments to functions?",
        "expected_key_points": [
            "Mutable: lists, dicts, sets (modified in place)",
            "Immutable: ints, floats, strings, tuples, frozensets (new object created on change)",
            "Pass-by-assignment or pass-by-object-reference",
            "Modifying a mutable object inside a function mutates the caller's object; reassigning variable rebinding locally",
        ],
        "reference_answer": "In Python, immutable objects (integers, strings, tuples) cannot be altered after creation; modifications create a new object in memory. Mutable objects (lists, dictionaries, sets) can have their contents altered in place. Python uses 'call by object reference' (or pass-by-assignment). When passing an argument, the parameter receives a reference to the same object. If the object is mutable and modified in place (e.g., list.append), the caller observes the mutation. If you reassign the variable inside the function (e.g., x = [1, 2]), it merely rebinds the local name without affecting the caller.",
        "rubric": {
            "relevance_weight": 0.25,
            "technical_weight": 0.35,
            "clarity_weight": 0.20,
            "completeness_weight": 0.20,
        },
    },
    {
        "id": "py-tech-02",
        "role": "Python Developer",
        "category": "technical",
        "difficulty": "Intermediate",
        "topic": "Concurrency & Python Internals",
        "question": "What is Python's Global Interpreter Lock (GIL), how does it affect CPU-bound vs I/O-bound tasks, and how can you achieve true parallelism?",
        "expected_key_points": [
            "GIL is a mutex that prevents multiple native threads from executing Python bytecodes simultaneously",
            "Memory management safety for CPython's reference counting",
            "I/O-bound tasks release the GIL during network/disk operations (threading or asyncio is effective)",
            "CPU-bound tasks suffer under threading; multiprocessing or C extensions allow multi-core parallelism",
        ],
        "reference_answer": "The Global Interpreter Lock (GIL) is a synchronization mutex in CPython that ensures only one thread executes Python bytecode at any given moment, safeguarding CPython's reference-counting memory management against race conditions. For I/O-bound operations (network requests, database queries, file reads), the GIL is released during system calls, making threading or asyncio highly effective. For CPU-bound tasks (data processing, numerical calculations), standard Python threads cannot leverage multiple CPU cores simultaneously. To achieve true multi-core parallelism in Python, developers use the multiprocessing module, ProcessPoolExecutor, or native libraries like NumPy/C-extensions that release the GIL.",
        "rubric": {
            "relevance_weight": 0.25,
            "technical_weight": 0.35,
            "clarity_weight": 0.20,
            "completeness_weight": 0.20,
        },
    },
    {
        "id": "py-tech-03",
        "role": "Python Developer",
        "category": "technical",
        "difficulty": "Intermediate",
        "topic": "Python Features",
        "question": "Explain Python generators, the 'yield' keyword, and how they optimize memory consumption compared to standard list returns.",
        "expected_key_points": [
            "Generators are iterators that produce items lazily on demand",
            "The yield keyword suspends function execution state and returns a value to the caller",
            "Resumes from the exact saved frame on next() call",
            "O(1) memory footprint rather than allocating the entire sequence in memory at once",
        ],
        "reference_answer": "A generator is a special type of iterator that lazily produces values one at a time on demand rather than computing them all up front. When a function contains the 'yield' keyword, calling it returns a generator object instead of executing immediately. When next() is invoked on the generator, execution proceeds until it reaches yield, which yields the current value and pauses the function's execution state (local variables and instruction pointer). Generators optimize memory consumption because they operate with O(1) auxiliary memory space, making them ideal for processing massive datasets or unbounded data streams without risking out-of-memory errors.",
        "rubric": {
            "relevance_weight": 0.25,
            "technical_weight": 0.35,
            "clarity_weight": 0.20,
            "completeness_weight": 0.20,
        },
    },

    # ==========================================
    # JAVA DEVELOPER (Technical)
    # ==========================================
    {
        "id": "java-tech-01",
        "role": "Java Developer",
        "category": "technical",
        "difficulty": "Beginner",
        "topic": "Java Memory Management",
        "question": "What is the difference between Heap and Stack memory in Java, and how does Garbage Collection work at a high level?",
        "expected_key_points": [
            "Stack memory stores primitive types and method frame references; LIFO, fast allocation",
            "Heap memory stores all objects and class instances; shared across threads",
            "Garbage Collector automatically identifies and cleans unreferenced objects",
            "Generational GC hypothesis (Young Generation with Eden/Survivor spaces, and Old/Tenured Generation)",
        ],
        "reference_answer": "In Java, Stack memory is used for static memory allocation and thread execution. It stores primitive values and references to heap objects within local method frames, following a strict LIFO structure with automatic allocation and deallocation as methods return. Heap memory is used for dynamic memory allocation, holding all class instances and objects, accessible across multiple threads. Garbage Collection (GC) automatically frees heap memory occupied by unreferenced objects through mark-and-sweep algorithms, often organized into generations (Eden, Survivor, and Tenured) to optimize collection frequency based on object lifespans.",
        "rubric": {
            "relevance_weight": 0.25,
            "technical_weight": 0.35,
            "clarity_weight": 0.20,
            "completeness_weight": 0.20,
        },
    },
    {
        "id": "java-tech-02",
        "role": "Java Developer",
        "category": "technical",
        "difficulty": "Intermediate",
        "topic": "Java Collections & Concurrency",
        "question": "Explain the internal working of HashMap in Java, including collision resolution and changes introduced in Java 8.",
        "expected_key_points": [
            "Array of Node/Bucket entries using hashCode() modulo array length",
            "Collision resolution via separate chaining (linked list)",
            "Java 8 treeification: linked list converted to balanced Red-Black Tree when bucket exceeds TREEIFY_THRESHOLD (8)",
            "Improves worst-case lookup from O(N) to O(log N)",
            "Contract between equals() and hashCode()",
        ],
        "reference_answer": "In Java, HashMap is backed by an array of bucket nodes. When put(key, value) is called, it computes key.hashCode(), applies a bitwise hash function, and calculates the bucket index using index = (n - 1) & hash. If multiple keys hash to the same bucket, collisions are handled using separate chaining. Prior to Java 8, collisions formed a linked list with O(n) search time. Since Java 8, when a bucket contains more than 8 elements and the total capacity is at least 64, the linked list transitions into a self-balancing Red-Black Tree, reducing worst-case search and insertion time from O(n) to O(log n). If both keys match based on equals(), the existing value is replaced.",
        "rubric": {
            "relevance_weight": 0.25,
            "technical_weight": 0.35,
            "clarity_weight": 0.20,
            "completeness_weight": 0.20,
        },
    },

    # ==========================================
    # AI / ML ENGINEER (Technical)
    # ==========================================
    {
        "id": "aiml-tech-01",
        "role": "AI/ML Engineer",
        "category": "technical",
        "difficulty": "Beginner",
        "topic": "Machine Learning Fundamentals",
        "question": "Explain the Bias-Variance tradeoff, what overfitting vs underfitting looks like, and how you prevent overfitting in practice.",
        "expected_key_points": [
            "Bias is error from erroneous assumptions; high bias leads to underfitting",
            "Variance is error from sensitivity to training data fluctuations; high variance leads to overfitting",
            "Techniques to prevent overfitting: regularization (L1/L2), cross-validation, pruning, dropout, more data, early stopping",
        ],
        "reference_answer": "The Bias-Variance tradeoff is the central challenge in supervised machine learning. Bias measures how far model predictions are from the true values due to overly simplistic assumptions (leading to high training and test error, known as underfitting). Variance measures model sensitivity to fluctuations in the training set (performing exceptionally well on training data but poorly on unseen test data, known as overfitting). To mitigate overfitting: collect more diverse data, apply L1/L2 regularization to penalize large weights, use dropout and batch normalization in neural networks, apply early stopping during training, and tune hyper-parameters via k-fold cross-validation.",
        "rubric": {
            "relevance_weight": 0.25,
            "technical_weight": 0.35,
            "clarity_weight": 0.20,
            "completeness_weight": 0.20,
        },
    },
    {
        "id": "aiml-tech-02",
        "role": "AI/ML Engineer",
        "category": "technical",
        "difficulty": "Intermediate",
        "topic": "Deep Learning & NLP",
        "question": "What is the Self-Attention mechanism in the Transformer architecture, and why did it replace Recurrent Neural Networks (RNNs) for sequential data?",
        "expected_key_points": [
            "Queries (Q), Keys (K), Values (V) matrix projections",
            "Attention scores computed as Softmax(Q * K^T / sqrt(d_k)) * V",
            "Allows direct modeling of dependencies between any two tokens regardless of distance (resolving vanishing gradients)",
            "Parallel training across the entire sequence compared to RNN sequential step-by-step bottleneck",
        ],
        "reference_answer": "The Self-Attention mechanism allows a model to weigh the relevance of all tokens in an input sequence relative to each other simultaneously. It computes Query, Key, and Value vectors for each token via learned linear transformations. The attention weights are calculated by taking the dot product of Queries and Keys, scaling by the square root of the dimension (sqrt(d_k)), applying Softmax, and multiplying by the Values: Softmax(Q K^T / sqrt(d_k)) V. It replaced RNNs because RNNs process sequences sequentially (O(N) sequential steps), which creates a training bottleneck and suffers from vanishing gradients over long contexts. Self-Attention processes the entire sequence in parallel on GPUs and captures long-range dependencies with constant path length O(1).",
        "rubric": {
            "relevance_weight": 0.25,
            "technical_weight": 0.35,
            "clarity_weight": 0.20,
            "completeness_weight": 0.20,
        },
    },

    # ==========================================
    # PROJECT-BASED QUESTIONS (Technical / Practical)
    # ==========================================
    {
        "id": "proj-tech-01",
        "role": "General",
        "category": "project_based",
        "difficulty": "Intermediate",
        "topic": "Projects & Architecture",
        "question": "Describe a challenging technical project you worked on recently. What was the core problem, what architectural choices did you make, and what trade-offs did you encounter?",
        "expected_key_points": [
            "Clear problem statement and objectives",
            "Architectural breakdown (frontend, backend, database, caching, messaging)",
            "Specific technical decision with concrete rationale and alternative considered",
            "Quantifiable outcomes or lessons learned",
        ],
        "reference_answer": "A strong project explanation uses a structured approach: 1) Context & Problem: Describe the domain and why the project was built. 2) Architecture: Detail the tech stack, component interactions, and data flow. 3) Engineering Challenge: Highlight a specific non-trivial obstacle (e.g., latency, state management, concurrency, schema design). 4) Trade-offs: Explain why you chose technology X over Y (e.g., choosing PostgreSQL over MongoDB for ACID guarantees, or using Redis for caching vs querying on-demand). 5) Outcome: Conclude with measurable results, testing strategy, or production lessons.",
        "rubric": {
            "relevance_weight": 0.20,
            "technical_weight": 0.30,
            "clarity_weight": 0.25,
            "completeness_weight": 0.25,
        },
    },

    # ==========================================
    # HR & BEHAVIORAL QUESTIONS (STAR METHODOLOGY)
    # ==========================================
    {
        "id": "hr-behav-01",
        "role": "General",
        "category": "behavioral",
        "difficulty": "Beginner",
        "topic": "Conflict & Collaboration",
        "question": "Tell me about a time you had a technical disagreement with a team member or peer. How did you handle it and what was the outcome?",
        "expected_key_points": [
            "Situation: Context of the disagreement or differing technical opinions",
            "Task: The shared objective or deliverable at stake",
            "Action: Active listening, objective evaluation of trade-offs, proof of concept or data-driven discussion",
            "Result: Constructive resolution, professional relationship preserved, successful project delivery",
        ],
        "reference_answer": "Follow the STAR method: In our final year project (Situation), my teammate and I disagreed on whether to use REST or WebSockets for live notifications (Task). Instead of debating abstractly, I suggested we evaluate our actual requirements against both: WebSockets offered lower latency, but REST with long-polling had faster implementation and better serverless compatibility for our deadline (Action). We built a small benchmark, concluded REST polling satisfied our 2-second SLA with less operational risk, and agreed to proceed. We shipped on schedule and maintained strong mutual trust (Result).",
        "rubric": {
            "relevance_weight": 0.30,
            "technical_weight": 0.15,
            "clarity_weight": 0.25,
            "completeness_weight": 0.30,
        },
    },
    {
        "id": "hr-behav-02",
        "role": "General",
        "category": "behavioral",
        "difficulty": "Beginner",
        "topic": "Failure & Resilience",
        "question": "Can you share an experience where a project or task did not go as planned? What went wrong, and what did you learn from it?",
        "expected_key_points": [
            "Honest recognition of a setback without blaming others",
            "Root cause identification (e.g., scope creep, insufficient test coverage, unclear requirements)",
            "Corrective action taken immediately to mitigate the damage",
            "Systemic takeaway or improved process adopted for future projects",
        ],
        "reference_answer": "Use STAR format: During a college hackathon, we built a collaborative document editor. A few hours before submission, concurrent edits began wiping user changes because our backend lacked conflict resolution. I took ownership of the bug, quickly communicated the issue to the team, and implemented basic optimistic locking with timestamp checks to prevent overwrites, sacrificing full real-time syncing to deliver a stable MVP. We presented a functional system, and the experience taught me to prioritize end-to-end integration testing and concurrency edge-cases early in design rather than postponing them to the end.",
        "rubric": {
            "relevance_weight": 0.30,
            "technical_weight": 0.15,
            "clarity_weight": 0.25,
            "completeness_weight": 0.30,
        },
    },
    {
        "id": "hr-behav-03",
        "role": "General",
        "category": "hr",
        "difficulty": "Beginner",
        "topic": "Career Goals & Motivation",
        "question": "Why do you want to join our organization in this specific role, and where do you see your engineering skills evolving over the next 2-3 years?",
        "expected_key_points": [
            "Knowledge of company/role mission and tech challenges",
            "Alignment between current skill set and role responsibilities",
            "Concrete growth roadmap (mastering core stack, system design, architectural ownership)",
            "Enthusiasm for contributing to team success",
        ],
        "reference_answer": "A structured answer should: 1) Express alignment with the company's product domain and engineering challenges. 2) Connect your current foundation in computer science and modern frameworks to the day-to-day role. 3) Articulate a realistic 2-3 year growth trajectory: transitioning from mastering codebases and delivering reliable features under mentorship to independently leading component designs, mentoring junior peers, and optimizing system performance.",
        "rubric": {
            "relevance_weight": 0.35,
            "technical_weight": 0.10,
            "clarity_weight": 0.30,
            "completeness_weight": 0.25,
        },
    },
]
