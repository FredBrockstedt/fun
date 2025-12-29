package main

import (
  "fmt"
  "testing"
)

func Hello(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}

func TestHello(t *testing.T) {
    output := Hello("Fred")
    if output != "Hello, Fred!" {
      t.Fatal("unexpected output: " + output)
    }
}

func main() {
    fmt.Println(Hello("World"))
}

