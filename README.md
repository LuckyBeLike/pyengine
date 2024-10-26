# PyEngine

**PyEngine** is a Python library targeting to make game creation easier, especially for developers familiar with Unity or Godot. It provides a component-based architecture and a set of tools that simplify game development, allowing you to focus on building your game's unique features.


## Features

- **Component-Based Architecture**: Utilize a system similar to Unity and Godot, making it intuitive to create and manage game objects and their behaviors.
- **Simplified Game Loop**: Built-in game loop handling, event processing, and rendering to streamline your development process.
- **Easy Input Handling**: Convenient methods for capturing keyboard/mouse input and managing events.
- **Built-in Physics**: Basic collision detection and gravity components ideal for most types of games.
- **Extensibility**: Easily extend components to suit the specific needs of your game.
- **Lightweight and Minimalistic**: Focused on simplicity without unnecessary complexity, ideal for beginners and small projects.


## Installation

Since PyEngine is not yet available on PyPI, you can install it directly from the GitHub repository:

```bash
pip install git+https://github.com/yourusername/pyengine.git
```


## Getting Started

After installing, import the library:

```python
import pyengine as pe
```

Setup your game:

```python
# Set window title and size
pe.setTitle("PyEngine example game")
pe.setSize(1280, 720)
```

Create main loop function and add it as an update listener:

```python
def update():
  # Your looping code here...

# Mark the function above as the main loop
pe.addUpdateListener(update)
```

Finally run PyEngine:

```python
pe.run()
```

The full starting code should look like this:

```python
import pyengine as pe

pe.setTitle("Game Name")
pe.setSize(1280, 720)

def update():
  pass

pe.addUpdateListener(update)
pe.run()
```
