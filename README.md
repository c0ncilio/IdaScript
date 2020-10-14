# Description
Utility for running scripts from the command line.
Versions used:
- Python 2.7
- IDA 6.8
Example of script:
```python
import idascript
import idaapi

def run(arg1, arg2):
    print "Image Base:", hex(idaapi.get_imagebase())
        
if __name__ == "__main__":
    idascript.execute(run, 0, 1)
```
Example of run:
```
ida_runner.py -ida "C:\\Program Files (x86)\\IDA 6.8" -input "C:\test.exe"  -script "C:\test.py"
```
