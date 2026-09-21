# Gradient Tool

The Gradient Tool allows you to create smooth transitions between colors in your display.

Within the kernel, call until complete:

```nim
if not gradient.renderAll():
    kernelHalt.halt()
```