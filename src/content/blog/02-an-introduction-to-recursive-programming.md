---
title: An introduction to recursive programming
description: How to manage when a solution for a problem contains the problem itself
pubDate: 2022-02-27
heroImage: '/images/blog/headers/recursion.jpeg'
tags: ['algorithms']
---


>  _Recursion_ consists of a problem with a solution that contains a smaller version of the same problem. In programming, it allows solving the problem by applying the same function several times to a value until finally reaching the result.

Let's see some examples!

## 1. Factorial of a number

The factorial of a number is the function that multiplies the number by each natural number below it.

```js
5! = 5 * 4 * 3 * 2 * 1
4! =     4 * 3 * 2 * 1

5! = 5 * 4!
```

Here, if we pay attention, we can see that `5!` is `5 * 4!`, so the result is a smaller factorial!

```js
// If
5! = 5 * 4!
// Then
n! = n * n-1!

f(n): factorial of n
f(n) = n * f(n-1)
```

The problem is that this doesn't stop and continues to infinity

```js
f(2) = 2 * f(1)
f(1) = 1 * f(0)
f(0) = 0 * f(-1)
f(-1) = -1 * f(-2)
... ad infinitum
```

A recursive algorithm needs 2 cases:
-   Base case
-   Recursive case

In this case:
-   Base case: `n = 0`
-   Recursive case: `n > 0`

```python
# @param n >= 0
def f(n):
    if n == 0:
        return 1
    else:
        return n * f(n-1)

f(5) # out: 120
f(6) # out: 720  (120 * 6)
```

## 2. Fibonacci

Fibonacci sequence, in which each number is the sum of the two preceding ones. The sequence commonly starts from 0 and 1.

```js

f(n) = f(n-1) + f(n-2)
f(7) = 0 1 1 2 3 5 8 13 21
```

- Base case: `n <= 1`
- Recursive case: `n > 1`

```python
# Recursive
# f(n): returns the number for the n position in the sequence
def f(n):
    if n <= 1:
        return n
    else:
        return f(n-1) + f(n-2)

print( f(1), f(2), f(3), f(4), f(5), f(6))
# out: (1, 1, 2, 3, 5, 8)


# Interative
# f(n): fibonacci sequence with n iterations
def f(n):
	result = []
    a, b = 0, 1
    for i in range(n):
		result.append(a)
        a, b = b, a+b
    return result

print(f(8))
# out: [0, 1, 1, 2, 3, 5, 8, 13]
```


## Conclusion

Recursive programming is a way to solve problems that contain themselves. Is extremly useful for solving certain problems with a short implmementation, but they can be dangerous if we don't define the base case and the recursive case correctly, or we could end with infinite loop cases crashing our program.

So take care with recursive programming!

![code_gif_from_giphy](/images/blog/endings/2.gif)