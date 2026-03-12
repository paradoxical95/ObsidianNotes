**CPU has Arithmetic Logic Unit, Registers and Control Unit.** 
ALU connects to both CU and Regs. This contraption is called Von-neumann architecture for some reason.
CU handles the instructions, keeping the Instruction pointer (EIP in 32bit and RIP in 64bit) which knows which instruction to execute next.
ALU is the one obtaining instructions from mem, executing it and then storing the result in either Mem or Regs.
Regs are just fast and easily accessible storage for CPU.

##### Register Types 
- **Instruction Pointer** : also called the Program counter, contains the addr of next instruction. In 32bit called Extended Instruction Pointer and in 64bit systems called Reg-Instruction Pointer.
- **Gen-Purpose Reg** : All 32-bit regs in x86 systems and 64-bit in x64 systems. [Here the 'E' prefix is for 32-bit and 'R' for 64-bit. Suffix 'X' is usually used for standard-reg and 'P' for pointer-reg usually and 'I' for index-reg].
	Has the following in it.-> 
	- ***Accumulator Reg*** : often stores the **results of Arithmetic Operations**.
	  32-bit has `EAX`, 64-bit has `RAX`. Inside these, last 16-bits can be addressed using `AX` and within it, you can address as as two 8-bits, `AL` for lower and `AH` for higher respectively.
	- ***Base Regs*** : often used to **store the base address for referencing an offset**. Same sub-categorization with 64-bit `RBX`, 32-bit `EBX`, 16-bit `BX`, 8-bit `BH` and `BL` regs.
	- ***Counter Regs*** : often **used in counting ops** such as loops etc. Same stuff with 64-`RCX`, 32-`ECX`, 16-`CX`, 8-`CH` and 8-`CL`.
	- ***Data Regs*** : often **used in multiplication/division ops**. 64-`RDX`, 32-`EDX`, 16-`DX`, 8-`DH` and 8-`DL`.
	- ***Stack Pointer*** : This reg **points at the top of the stack** and is used in conjunction with Stack Segment Reg. 64-`RSP`, 32-`ESP` and 16-`SP`. Cannot be addressed smaller than this.
	- ***Base Pointers*** : Used to **access parameters passed by the stack** and is also used in conjunction with 'Stack Segment' Reg. 64-`RBP`, 32-`EBP` and 16-`BP` (nothing smaller).
	- ***Source Index Reg*** : **Used for string ops**. Used with 'Data Segment' (DS) reg as an offset. 64-`RSI`, 32-`ESI` and 16-`SI` (nothing smaller).
	- ***Destination Index Reg*** : **Also for string ops**. Used with 'Extra Segment' (ES) reg as an offset. 64-`RDI`, 32-`EDI` and 16-`DI` (nothing smaller).
	- ***R8-R15*** : Also Gen-purpose but not present in 32-bit systems. Inherently 64-bit. Also addressable in 32,16,8-bit modes. Eg: `R8D` for lower 32-bit addressing and `R8W` for lower 16-bit addressing and R8B for lower 8-bit addressing. Here, D means 'double word' and W means 'word' and B is for Byte.
	- 
- **Status Flag Reg** : Usually a status is needed for the execution. **`EFLAGS`** register for 32-bit system and **`RFLAGS`** for 64-bit. Some necessary flags are :
	- **Zero Flag** : ZF , denotes the status of the last executed instruction was 0. Eg: RAX subtracted from itself, result 0 hence ZF is set to 1.
	- **Carry Flag** : CF indicates when the last executed instruction resulted in a number too big/small for destination, setting CF to 1. Eg: `0xFFFFFFFF` added with `0x00000001` but the result is too big for a 32-bit reg.
	- **Sign Flag** : SF indicates if the result of an op is -ve OR the most significant bit it set to 1. If this is met then SF is set to 1, else 0.
	- **Trap Flag** : TF indicates if the processor is in debug-mode. When TF is set, CPU executes one instruction at a time for debugging purpose. CAN be used my malware to see if they're being run in a debugger.
- **Segment Reg** : 16-bit regs that convert flat mem space into different segments for easier addressing.
	- **Code Segment** : CS -- points to code section in mem.
	- **Data Segment** : DS -- points to program's data section in mem.
	- **Stack Segment** : SS -- points to program's stack in mem.
	- **Extra Segments** : ES, FS and GS -- point to different data sections. These and the DS regs divide the program's mem into 4 distinct data sections.

##### Memory Overview
