# Java Basic Cheat Sheet

## Java Basic Concept

### Start From HelloWorld

```java
public class HelloWorld{
	static void main(String[] args){
		System.out.println("Hello, world!");
	}
}
```
Questions:
1. What's the name of this java file?
2. How to use java and javac in command line?
3. What should you do if you want to output "Hi, world!"?

### Variable, Method, Statement and Comment

```java
public class Demo{
	static void main(String[] args){
		int a = 1; // assign 1 to variable a
		System.out.println(a);
	}
}
```

Questions:
1. What does **void**, **int**, **double** stand for?
2. Why a is a variable, System.out.println() is a method?
3. How can you tell if one single line is a statement or not?
4. How should you name a class, a variable and a method?
5. What's the difference between int and Integer? How to tell if a variable type is reference or primitive?
6. When shoule we use comment?

### Define a Method

```java
public class Demo{
	static Integer sumTwo(int a, int b){
		return a+b;
	}

	public static void main(String[] args){
		System.out.println(sumTwo(1,2));
	}
}
```

Questions:
1. What does the key word **return** stand for?
2. Why we put **Integer** before sumTwo, **void** before main?
3. Can we difine a method in the body of another method?
4. Do we need to input the exact value of input variable when defining the method?

### Array

Questions:
1. What's the difference between static array and dynamic array?[click this](https://leetcode.com/explore/learn/card/array-and-string/201/introduction-to-array/)
2. How to create a static array?
3. What does **String[] args** stand for in main method?
4. Please write a java file, every time we put two integers in argument, the sum will be printed out.

### Boolean and Condition Control

```java
public class Demo{
	public static void main(String[] args) {
		for (int i = 1; i < 10; i=i+1){
			System.out.println(i);
		}
	}
}
```

Questions:
1. What's the difference between **=** and **==**?
2. Must **else** occur in pair with **if**?
3. What it would be if **for (int i = 1; true; i=i+1)**? What if **for (int i = 1; false; i=i+1)**
4. How to use key word **for**?
5. What does **!**, **<=** and **!=** stand for?

### Algorithm Basic

Questions:
1. How many integers from 1 to 100 can be divided by 3?
2. How many integers from 1 to 1000 can be divided by 7 or contains 7 in its digits(e.g. 17, 172, 765)?
3. [Find Pivot Index](https://leetcode.com/explore/learn/card/array-and-string/201/introduction-to-array/1144)
4. [Plus One](https://leetcode.com/explore/learn/card/array-and-string/201/introduction-to-array/1148)

### Try and Catch

```java
public class Demo{
	public static void main(String[] args) {
		try {
			int[] myNumbers = {1,2,3};
			System.out.println(myNumbers[10]);
		} catch (Exception e) {
			System.out.println("Something went wrong.")
		} finally {
			System.out.println("The 'try catch' is finished.");
		}
	}
}
```

Questions:
1. Must **catch** occur in pair with **try**?
2. What does the key word **finally** stand for?

## Object Oriented Programming (OOP)

### Static and Object

```java
public class Demo{
	static Integer sumTwo(int a, int b){
		return a+b;
	}

	public static void main(String[] args){
		System.out.println(sumTwo(1,2));
	}
}
```

Questions:
1. What does the key word **static** before sumTwo method stand for?
2. If sumTwo is not a static method, then how should you use sumTwo in main method?

### Constructor

Questions:
1. How to tell if a method is a Constructor or not?
2. When will Constructor be executed?
3. How to input variable in Constructor?

### Inheritance

```java
class Superclass {
	Superclass(int i){
		System.out.println(i);
	}
}

public class Subclass extends Superclass {
	int index;

	Subclass(int i) {
		super(i);
		this.index = 1;
		System.out.println(index);
	}

	public static void main(String[] args) {
		Subclass a = new Subclass(1);
	}
}
```

Questions:
1. What does key word **this** and **super** stand for?
2. Both Superclass and Subclass have Constructor in definition, how will them be excuted when a new Subclass object is created?

### Overriding

```java
class Superclass {
	void sayHi(){
		System.out.println("Hi");
	}
}

public class Subclass extends Superclass {
	void sayHi(){
		System.out.println("Hello");
	}

	public static void main(String[] args) {
		Subclass a = new Subclass();
		a.sayHi();
	}
}
```

Question:
1. What is overriding in Java?
2. What's the key word **final** stand for?

### Overloading

```java
public class Demo{
	Integer sumTwo(int a, int b){
		return a+b;
	}

	Double sumTwo(double a, double b){
		return a+b;
	}

	public static void main(String[] args){
		Demo a = new Demo();
		System.out.println(a.sumTwo(1,2));
		System.out.println(a.sumTwo(1.0,2.0))
	}
}
```

Question:
1. What is overloading in Java?

### Abstract Class

Question:
1. Can you create an object from an abstract class?
2. Can you define a static method in abstract class?
3. Can a Subclass extend multiple different Superclasses?

### Interface

Questions:
1. Can you define a non-abstract method in interface?
2. Can a class implement multiple different interfaces?
3. [What's the difference between abstract class and interface?](https://www.geeksforgeeks.org/difference-between-abstract-class-and-interface-in-java/)

### Encapsulation

```java
public class Demo{
	public static void main(String[] args) {
		Student a = new Student();
		System.out.println(a.getAge());
	}
}

class Student{
	private int age = 18;

	public int getAge(){
		return this.age;
	}
}
```

Questions:
1. Why we can't use **System.out.println(a.age)** in main method?
2. [What dose the key word **private**, **protected** and **public** stand for?](https://stackoverflow.com/questions/215497/what-is-the-difference-between-public-protected-package-private-and-private-in)
3. How to use class defined in another java file (under same directory)?

### Package

Questions:
1. How to use key word **package** and **import**?

### toSring method

```java
public class Demo {
	public String toSring(){
		return "Hi";
	}

	public static void main(String[] args) {
		Demo a = new Demo();
		System.out.println(a);
	}
}
```

Questions:
1. How does toString method work out?

### equals method

Question:
1. What's the difference between equals method and ==?

### Generics

```java
class Pen{
	String color;
}

class Pencil{
	String color;
}

class Box<T>{
	T obj;
	Box(T obj){
		this.obj = obj;
	}
	public T getObject(){
		return this.obj;
	}
}

public class Demo{
	public static void main(String[] args) {
		Pen a = new Pen();
		Box<Pen> box1 = new Box<Pen>(a);
	}
}
```

Question:
1. Explain the definition of class Box<T> line by line.

## Advanced Data Structure

### Dynamic Array

Questions:
1. [What is a dynamic array?](https://leetcode.com/explore/learn/card/array-and-string/201/introduction-to-array/1146/)

### Set

Questions:
1. Can Set have duplicate elements?

### Map

Questions:
1. What's stored in a Map?
2. Can Map have duplicate key or value?

### Queue and Stack
Questions:
1. Is Queue First-In-First-Out or Last-In-First-Out? How about Stack?
2. Describe some examples of the implementations on queue and stack?