# AI-mini---project

## 🐍 Snake Game with A* Pathfinding (AI Mini Project)

### 📘 Project Overview

This project is an **AI-based Snake Game** developed in **Python** using **Pygame**.
It combines **classic snake gameplay** with an **A* pathfinding algorithm** that enables the snake to automatically find the optimal path to the food — simulating an intelligent AI-controlled agent.

You can toggle between **manual** and **AI auto-play** modes during gameplay.

---

### 🎯 **Aim**

To design and implement a **Snake game** integrated with the **A* pathfinding algorithm** that enables the snake to autonomously navigate the grid and collect food while avoiding obstacles (its own body).

---

### 🧠 **Algorithm Used**

#### A* (A-star) Pathfinding Algorithm

The A* algorithm is used to find the shortest path between the snake’s head and the food.

**Heuristic Function (h):**
Uses **Manhattan distance**:

```
h(x, y) = |x1 - x2| + |y1 - y2|
```

**Evaluation Function:**

```
f(n) = g(n) + h(n)
```

* `g(n)` → Cost from start to current node
* `h(n)` → Estimated cost from current node to goal

The algorithm avoids the snake’s body cells (treated as obstacles) while finding the best route.

---

### ⚙️ **Features**

✅ Classic Snake game using Pygame
✅ AI-powered movement using A* algorithm
✅ Toggle between Auto and Manual mode (`SPACE` key)
✅ Dynamic path visualization
✅ Smooth grid and UI design
✅ Restart and scoring system

---

### 💻 **Requirements**

Install Python and the required library:

```bash
pip install pygame
```

---

### 🚀 **How to Run**

1. **Open the project folder** in VS Code or any IDE
2. Make sure your file is named **`snake.py`**
3. Open terminal in that folder and run:

```bash
python snake.py
```

4. The game window will appear.

---

### 🎮 **Controls**

| Key                                 | Action                                   |
| ----------------------------------- | ---------------------------------------- |
| **SPACE**                           | Toggle between Auto (AI) and Manual mode |
| **W / A / S / D** or **Arrow Keys** | Move the snake (Manual mode)             |
| **R**                               | Restart the game                         |
| **ESC**                             | Quit the game                            |

---

### 🧩 **Game Logic**

* The grid is composed of cells (`CELL_SIZE = 24`).
* The snake’s body is stored as a deque (efficient head/tail manipulation).
* The AI uses A* to find the shortest path to food.
* When the path is blocked, a **safe random move** is chosen.
* Collision detection resets the game.

---

### 🖥️ **Output (Expected Result)**

* A game window appears titled **“Snake with A* Pathfinding”**
* The snake automatically moves towards the food in **Auto Mode** using the **A* algorithm**
* In **Manual Mode**, the user can control the snake with keys
* Score is displayed on screen
* Game restarts when collision occurs

---

### 🧾 **Result**

Successfully implemented a **Snake game** that demonstrates **A* pathfinding algorithm** for intelligent movement.
This project effectively shows how **AI algorithms** can be applied in **real-time game environments**.

---

### 👨‍💻 **Developed By**

**Name:** *Ananda Krishna*
**Reg no:**2117240070019
**Project Type:** *AI Mini Project*
**Language:** *Python (Pygame)*
**Algorithm Used:** *A* Pathfinding*

---

