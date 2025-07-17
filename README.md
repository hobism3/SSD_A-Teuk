## Command Parsing Rule
- Memory 주소 check
  - isdigit() + in range(0, 100)
- value
  - 무조건 10자리, 0x로 시작, 8자리는 0123456789ABCDEF
- address와 value는 ' '(space)로 분리

## ssd
- execute(*args)
- read, write는 private
- cmd
  - args[1]: 'R' or 'W'
  - args[2]: address
  - (WRITE) args[3]: value
  
