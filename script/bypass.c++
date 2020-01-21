#include <stdint.h>
#include <Shlwapi.h>
#pragma comment(lib, "Shlwapi.lib")
 
#define BLACKCIPHER_EXE "BlackCipher.aes"
 
typedef BOOL(WINAPI* CreateProcessWPtr)(LPCWSTR, LPWSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES, BOOL, DWORD, LPVOID, LPCWSTR, LPSTARTUPINFO, LPPROCESS_INFORMATION);
CreateProcessWPtr _CreateProcessW = (CreateProcessWPtr)GetProcAddress(GetModuleHandleA("Kernel32.dll"), "CreateProcessW");
 
BOOL WINAPI CreateProcessW_Hook(LPCWSTR lpApplicationName, LPWSTR lpCommandLine, LPSECURITY_ATTRIBUTES lpProcessAttributes, LPSECURITY_ATTRIBUTES lpThreadAttributes, BOOL bInheritHandles, DWORD dwCreationFlags, LPVOID lpEnvironment, LPCWSTR lpCurrentDirectory, LPSTARTUPINFOW lpStartupInfo, LPPROCESS_INFORMATION lpProcessInformation)
{
	size_t chars_converted = 0;                             // used by wcstombs_s and mbstowcs_s
	char application_name_mb[512] = { "(nullptr)\0" };      // multibyte versions of the strings in the params
	char command_line_mb[512] = { "(nullptr)\0" };
	char current_directory_mb[512] = { "(nullptr)\0" };
	BOOL res;
	char buf[MAX_PATH] = { 0 };                             // used by GetModuleNameA
	PSTR cmd_line_end;                                      // pointer to the double quote after BlackCipher.aes in the cmd line
	size_t cmd_line_end_size;                               // size of the buffer after cmd_line_end
	int is_bc_executable = 0;                               // 1 if the call is related to BlackCipher.aes
	WCHAR replaced_cmd[512] = { 0 };                        // modified cmd line (BlackCipher.aes -> BlackCipher.aes2)
	
	do {
		if (lpApplicationName && wcstombs_s(&chars_converted, application_name_mb, 512, lpApplicationName, 512) == -1) {
			Log(L"wcstombs_s failed for lpApplicationName (%s)\n", lpApplicationName);
			break;
		}
 
		if (lpCommandLine && wcstombs_s(&chars_converted, command_line_mb, 512, lpCommandLine, 512) == -1) {
			Log(L"wcstombs_s failed for lpCommandLine (%s)\n", lpCommandLine);
			break;
		}
 
		if (lpCurrentDirectory && wcstombs_s(&chars_converted, current_directory_mb, 512, lpCurrentDirectory, 512) == -1) {
			Log(L"wcstombs_s failed for lpCurrentDirectory (%s)\n", lpCurrentDirectory);
			break;
		}
 
		is_bc_executable = StrStrIA(command_line_mb, BLACKCIPHER_EXE) != NULL;
 
		// replace BlackCipher.aes with BlackCipher.aes2
		if (is_bc_executable) 
		{
			cmd_line_end = StrStrIA(command_line_mb, BLACKCIPHER_EXE) + 15;
			cmd_line_end_size = MAX_PATH - (cmd_line_end - command_line_mb);
			memmove_s(cmd_line_end + 1, cmd_line_end_size - 1, cmd_line_end, cmd_line_end_size - 1);
			*cmd_line_end = '2';
 
			if (mbstowcs_s(&chars_converted, replaced_cmd, 512, command_line_mb, 512)) 
			{
				Log(L"mbstowcs_s failed for command_line_mb (%s)\n", command_line_mb);
				break;
			}
 
			lpCommandLine = replaced_cmd;
		}
 
	} while (0);
	
	res = _CreateProcessW(lpApplicationName, lpCommandLine, lpProcessAttributes, lpThreadAttributes, bInheritHandles, dwCreationFlags, lpEnvironment, lpCurrentDirectory, lpStartupInfo, lpProcessInformation);
 
	return res;
}
 
static uint32_t maple_pid = 0, maple_dump = 0, maple_base = 0, maple_size = 0;
 
typedef BOOL(WINAPI* ReadProcessMemoryPtr)(HANDLE, LPCVOID, LPVOID, SIZE_T, SIZE_T *);
ReadProcessMemoryPtr _ReadProcessMemory = (ReadProcessMemoryPtr)GetProcAddress(GetModuleHandleA("KernelBase.dll"), "ReadProcessMemory");
 
BOOL WINAPI ReadProcessMemory_Hook(HANDLE hProcess, LPCVOID lpBaseAddress, LPVOID lpBuffer,SIZE_T nSize, SIZE_T *lpNumberOfBytesRead)
{
	BOOL res;
	int spoofed = 0;
	uint32_t pid = (uint32_t)GetProcessId(hProcess);
	uint32_t current_pid = (uint32_t)GetCurrentProcessId();
	LPCVOID original_base = lpBaseAddress;
 
	if (pid == maple_pid || pid == current_pid)
	{
		if (GetProcessId(hProcess) == maple_pid && (uint32_t)lpBaseAddress >= maple_base && (uint32_t)lpBaseAddress < maple_base + maple_size) {
			lpBaseAddress = (LPCVOID)((uint32_t)lpBaseAddress - maple_base + maple_dump);
			spoofed = 1;
		}
 
		if (GetProcessId(hProcess) == GetCurrentProcessId() && (uint32_t)lpBaseAddress >= MS_Memory_Start && (uint32_t)lpBaseAddress < MS_Memory_End) 
		{
			lpBaseAddress = (LPCVOID)((uint32_t)lpBaseAddress - MS_Memory_Start + MS_Memory);
			Log(L"!!!BC tried to check its own memory!!!");
			spoofed = 1;
		}
	}
 
	res = _ReadProcessMemory(hProcess, lpBaseAddress, lpBuffer, nSize, lpNumberOfBytesRead);
 
	return res;
}
 
typedef LPVOID PCLIENT_ID;
#define STATUS_ACCESS_DENIED 0xC0000022
 
typedef NTSYSAPI NTSTATUS(NTAPI* NtOpenProcessPtr)(PHANDLE ProcessHandle, ACCESS_MASK AccessMask, POBJECT_ATTRIBUTES ObjectAttributes, PCLIENT_ID ClientId);
NtOpenProcessPtr _NtOpenProcess = (NtOpenProcessPtr)GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtOpenProcess");
 
NTSTATUS NTAPI NtOpenProcess_Hook(PHANDLE ProcessHandle, ACCESS_MASK AccessMask, POBJECT_ATTRIBUTES ObjectAttributes, PCLIENT_ID ClientId)
{
	NTSTATUS res;
	uint32_t pid;
	AccessMask |= PROCESS_QUERY_INFORMATION; // Ensures that we'll have permission to get PID
	res = _NtOpenProcess(ProcessHandle, AccessMask, ObjectAttributes, ClientId);
 
	pid = (uint32_t)GetProcessId(*ProcessHandle);
	if (!res && pid != maple_pid) 
	{
		Log(L"Blocking NtOpenProcess for pid %.08X\n", pid);
		res = STATUS_ACCESS_DENIED;
		*ProcessHandle = NULL;
	}
 
	return res;
}
 
typedef NTSYSAPI NTSTATUS(NTAPI* NtReadVirtualMemoryPtr)(HANDLE ProcessHandle, PVOID BaseAddress, PVOID Buffer, ULONG NumberOfBytesToRead, PULONG NumberOfBytesReaded);
NtReadVirtualMemoryPtr _NtReadVirtualMemory = (NtReadVirtualMemoryPtr)GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtReadVirtualMemory");
 
NTSTATUS NTAPI NtReadVirtualMemory_Hook(HANDLE ProcessHandle, PVOID BaseAddress, PVOID Buffer, ULONG NumberOfBytesToRead, PULONG NumberOfBytesReaded)
{
	if (GetProcessId(ProcessHandle) == maple_pid)
	{
		Log(L"Blocking NtReadVirtualMemory for address %.08X\n", BaseAddress);
		return STATUS_ACCESS_DENIED;
	}
 
	return _NtReadVirtualMemory(ProcessHandle, BaseAddress, Buffer, NumberOfBytesToRead, NumberOfBytesReaded);
}