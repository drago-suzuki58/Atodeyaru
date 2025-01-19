# Atodeyaru

Atodeyaru(あとでやる) is a completely new task scheduling library.

Other Language README  
[Japanese](README.md)

## Features

- Deadlines:  
  Just like cramming for exams, set a deadline and make sure it gets done by then.
- Whimsical execution:  
  Sometimes you might feel a burst of motivation and get it done early, or you might procrastinate until the very last minute.
- Escapism:  
  Ever find yourself cleaning your room instead of studying? This feature mimics that behavior, letting you switch tasks to avoid the one you don't want to do.
- Background execution:  
  Runs seamlessly in the background, so it won't disrupt your main workflow.

## Installation

You can install it from the GitHub repository.

```sh
python -m pip install git+https://github.com/drago-suzuki58/Atodeyaru
```

## Usage

### Creating an `Atodeyaru` Instance

To use `Atodeyaru`, first create an instance.

```python
from atodeyaru import Atode

# Create a basic Atodeyaru instance
atode = Atode()

# Create an Atodeyaru instance that runs as a daemon thread
# When daemon=True, it continues to execute tasks in the background even after the main process ends.
atode_daemon = Atode(daemon=True)
```

When `daemon=True` is specified, the thread managed by `Atodeyaru` operates as a daemon thread. This is useful when you want to continue executing tasks in the background even after the main program ends. The default is `False`.  
For more details, refer to the `threading` library.

### Registering Tasks (`yaru` Method)

Use the `yaru` method to register the function you want to execute with `Atodeyaru`

```python
import time
from atodeyaru import Atode

atode = Atode()

def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")
    time.sleep(1)

# Register a task to greet 'Alice' within about 5 seconds
atode.yaru(greet, deadline_sec=5, args=("Alice",))

# Register a task to greet 'Bob' with "Good morning" (no deadline)
atode.yaru(greet, args=("Bob",), kwargs={"greeting": "Good morning"})

# You can also register other functions
def another_task():
    print("Another task is running...")

atode.yaru(another_task)

time.sleep(10)
atode.stop()
```

- **`func`**:  
  Specify the function object you want to execute.
- **`deadline_sec` (optional)**:  
  Specify the approximate number of seconds you want the task to be executed. If `None` is specified, it is registered as a task without a deadline.
- **`args` (optional)**:  
  Specify a tuple of positional arguments to pass to the function. In the example above, the `greet` function is passed the argument `"Alice"`.
- **`kwargs` (optional)**:  
  Specify a dictionary of keyword arguments to pass to the function. In the example above, the `greet` function is passed the keyword argument `greeting="Good morning"`.

### Stopping `Atodeyaru`

```python
atode = Atode()
# ... Register tasks ...

# Stop the background thread managed by Atodeyaru
atode.stop()

# To forcefully stop, specify force=True (ongoing tasks may be interrupted)
atode.stop(force=True)
```

The `stop()` method stops the background thread managed by `Atodeyaru`

.

- `force=False` (default):  
  `Atodeyaru` waits until there are no more pending tasks and then stops the thread.
- `force=True`:  
  Interrupts ongoing tasks and immediately stops the thread. Use with caution as it may cause data inconsistencies.

## Note

As you can see, this library is not suitable for precise or critical use cases.  
Please use it as a fun and playful tool.
